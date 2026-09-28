"""Render the repository's root documents (CONTRIBUTING, GOVERNANCE, ...) on the website.

The root files stay the single source of truth, because GitHub shows them in its own
interface. At build time this hook copies them into ``docs/project/`` (which is git-ignored),
rewrites their relative links so they work inside the site, and points the page's
"edit" link back to the original root file.
"""

from __future__ import annotations

import json
import posixpath
import re
from pathlib import Path

REPO_BLOB = "https://github.com/25mordad/iran-gozar/blob/main/"
REPO_TREE = "https://github.com/25mordad/iran-gozar/tree/main/"
REPO_EDIT = "https://github.com/25mordad/iran-gozar/edit/main/"

# root file -> path inside docs/
ROOT_DOCS = {
    "CONTRIBUTING.md": "project/contributing.md",
    "CONTRIBUTING.en.md": "project/contributing.en.md",
    "GOVERNANCE.md": "project/governance.md",
    "GOVERNANCE.en.md": "project/governance.en.md",
    "CODE_OF_CONDUCT.md": "project/code-of-conduct.md",
    "CODE_OF_CONDUCT.en.md": "project/code-of-conduct.en.md",
    "SECURITY-FOR-CONTRIBUTORS.md": "project/security.md",
    "SECURITY-FOR-CONTRIBUTORS.en.md": "project/security.en.md",
    "STATUS.md": "project/status.md",
}

GENERATED_DIR = "project"
LINK_RE = re.compile(r"(?<!!)\[([^\]]*)\]\(([^)\s]+)\)")
# "[English version](X.en.md)" style lines: the site has its own language switcher.
LANG_LINE_RE = re.compile(r"^\[(English version|نسخه‌ی فارسی)\]\([^)]*\)\s*$", re.M)
H1_RE = re.compile(r"^#\s+(.+)$", re.M)
CODE_RE = re.compile(r"(^[ \t]*```.*?^[ \t]*```|`[^`\n]+`)", re.M | re.S)


def _rewrite_target(target: str, dest: str, root: Path) -> str:
    if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
        return target
    path, _, fragment = target.partition("#")
    frag = f"#{fragment}" if fragment else ""
    path = posixpath.normpath(path)
    dest_dir = posixpath.dirname(dest)
    if path in ROOT_DOCS:
        new = posixpath.relpath(ROOT_DOCS[path], dest_dir)
    elif path.startswith("docs/"):
        new = posixpath.relpath(path[len("docs/"):], dest_dir)
    elif (root / path).is_dir():
        return REPO_TREE + path + frag
    else:
        return REPO_BLOB + path + frag
    return new + frag


def _render(src_path: str, dest: str, text: str, root: Path) -> str:
    text = LANG_LINE_RE.sub("", text)

    def repl(m: re.Match) -> str:
        return f"[{m.group(1)}]({_rewrite_target(m.group(2), dest, root)})"

    # Leave fenced code blocks and inline code untouched.
    parts = CODE_RE.split(text)
    text = "".join(p if CODE_RE.fullmatch(p) else LINK_RE.sub(repl, p) for p in parts)
    m = H1_RE.search(text)
    title = m.group(1).strip() if m else src_path
    front = (
        "---\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        f"gozar_source: {src_path}\n"
        "---\n"
        f"<!-- Generated from {src_path} by hooks/root_docs.py. Edit {src_path}, not this file. -->\n\n"
    )
    return front + text.lstrip()


def on_config(config, **kwargs):
    root = Path(config.config_file_path).parent
    docs = Path(config.docs_dir)
    out_dir = docs / GENERATED_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    expected = set()
    for src, dest in ROOT_DOCS.items():
        src_file = root / src
        if not src_file.exists():
            continue
        target = docs / dest
        expected.add(target.resolve())
        content = _render(src, dest, src_file.read_text(encoding="utf-8"), root)
        # Write only when changed, so `mkdocs serve` does not loop on its own output.
        if not target.exists() or target.read_text(encoding="utf-8") != content:
            target.write_text(content, encoding="utf-8")
    for stale in out_dir.glob("*.md"):
        if stale.resolve() not in expected:
            stale.unlink()
    return config


def on_page_markdown(markdown, page, config, files, **kwargs):
    source = page.meta.get("gozar_source")
    if source:
        page.edit_url = REPO_EDIT + source
    return markdown
