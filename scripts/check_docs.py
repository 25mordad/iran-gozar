#!/usr/bin/env python3
"""Check that the project's documents follow the conventions in CONTRIBUTING.md.

Errors (the check fails):
  - a document has no plain-language summary at the top, or it has more than 5 sentences;
  - a page in docs/ has no front matter title, or an unknown "status" value;
  - the old admonition syntax ("!!! simple") is used instead of the blockquote form.

Warnings (reported, but the check passes):
  - Arabic "ي" or "ك" in Persian text (should be Persian "ی" and "ک");
  - a plan document without "Sources" or "Open questions" sections.

Usage:  python scripts/check_docs.py [--strict-warnings]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
ROOT_DOCS = [
    "README.md", "README.en.md", "CONTRIBUTING.md", "CONTRIBUTING.en.md",
    "GOVERNANCE.md", "GOVERNANCE.en.md", "CODE_OF_CONDUCT.md", "CODE_OF_CONDUCT.en.md",
    "SECURITY-FOR-CONTRIBUTORS.md", "SECURITY-FOR-CONTRIBUTORS.en.md", "STATUS.md",
]
# Pages with a different layout (the home page explains the project in its own box).
NO_SUMMARY = {"docs/index.md", "docs/index.en.md"}
SKIP_DIRS = {"docs/project"}  # generated at build time from the root files
STATUSES = {"draft", "review", "reviewed"}

SUMMARY_TITLE = {"fa": "خلاصه به زبان ساده", "en": "In plain words"}
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
CODE_RE = re.compile(r"^[ \t]*```.*?^[ \t]*```|`[^`\n]+`", re.M | re.S)
SENTENCE_END = re.compile(r"[.!?؟](?=[\s»\")]|$)")
MAX_SENTENCES = 5


def lang_of(path: Path) -> str:
    return "en" if path.name.endswith(".en.md") else "fa"


def summary_block(text: str, lang: str) -> list[str] | None:
    lines = text.splitlines()
    header = f"> **{SUMMARY_TITLE[lang]}**"
    for i, line in enumerate(lines):
        if line.strip() == header:
            block = []
            for nxt in lines[i + 1:]:
                if not nxt.startswith(">"):
                    break
                content = nxt[1:].strip()
                if content:
                    block.append(content)
            return block
    return None


def check_file(path: Path, errors: list, warnings: list) -> None:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    lang = lang_of(path)
    body = FRONT_RE.sub("", text)

    if "!!! simple" in CODE_RE.sub("", body):
        errors.append(f"{rel}: uses '!!! simple'; use the blockquote form (python scripts/convert_summary.py {rel})")

    if rel.startswith("docs/"):
        m = FRONT_RE.match(text)
        meta = {}
        if not m:
            errors.append(f"{rel}: missing front matter (--- title: ... ---)")
        else:
            try:
                meta = yaml.safe_load(m.group(1)) or {}
            except yaml.YAMLError as exc:
                errors.append(f"{rel}: invalid front matter: {exc}")
            if not meta.get("title"):
                errors.append(f"{rel}: front matter has no 'title'")
            status = meta.get("status")
            if status and status not in STATUSES:
                errors.append(f"{rel}: unknown status '{status}' (use one of {sorted(STATUSES)})")

    if rel not in NO_SUMMARY:
        block = summary_block(body, lang)
        if block is None:
            errors.append(f"{rel}: missing plain-language summary ('> **{SUMMARY_TITLE[lang]}**')")
        else:
            joined = " ".join(block)
            sentences = len(SENTENCE_END.findall(joined))
            if sentences > MAX_SENTENCES:
                errors.append(f"{rel}: plain-language summary has {sentences} sentences (max {MAX_SENTENCES})")
            if not block:
                errors.append(f"{rel}: plain-language summary is empty")

    if lang == "fa":
        prose = CODE_RE.sub("", body)
        arabic = sorted(set(re.findall(r"[يك]", prose)))
        if arabic:
            warnings.append(f"{rel}: Arabic letters {arabic} found; use Persian ی and ک")

    if re.match(r"docs/(institutions|topics)/(?!index)", rel):
        heads = {"fa": ("## منابع", "## پرسش‌های باز"), "en": ("## Sources", "## Open questions")}[lang]
        for h in heads:
            if h not in body:
                warnings.append(f"{rel}: no section starting with '{h}'")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    files = [ROOT / f for f in ROOT_DOCS if (ROOT / f).exists()]
    for path in sorted(DOCS.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if any(rel.startswith(d + "/") for d in SKIP_DIRS):
            continue
        files.append(path)
    for path in files:
        check_file(path, errors, warnings)

    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"ERROR:   {e}")
    print(f"\nChecked {len(files)} files: {len(errors)} error(s), {len(warnings)} warning(s).")
    if "--strict-warnings" in sys.argv and warnings:
        return 1
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
