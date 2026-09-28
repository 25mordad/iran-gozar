"""Site-wide Markdown conventions for «گذار».

1. Plain-language summary: a blockquote that starts with ``> **خلاصه به زبان ساده**``
   (or ``> **In plain words**``) is rendered as a highlighted box. The blockquote form
   is used in the source files because it also looks right on GitHub.
2. ``[نیاز به منبع]`` / ``[citation needed]`` markers become links to the
   "sources needed" page, and are counted per page.
3. Pages shown in the English site that exist only in Persian get a notice and RTL layout.
4. The page ``needs-sources.md`` gets an automatically generated list of every marker.
5. Small placeholders (``<!-- gozar:doc-count -->`` ...) are filled with live numbers.
6. Every plan document (a page with ``status`` in its front matter) gets a PDF path.
"""

from __future__ import annotations

import json
import os
import posixpath
import re
from pathlib import Path

import yaml
from mkdocs.plugins import event_priority

SUMMARY_TITLES = ("خلاصه به زبان ساده", "In plain words")
SUMMARY_RE = re.compile(
    r"^> \*\*(" + "|".join(map(re.escape, SUMMARY_TITLES)) + r")\*\*[ \t]*\n(?:>[ \t]*\n)?((?:>.*(?:\n|$))+)",
    re.M,
)
MARKER_RE = re.compile(r"\[(نیاز به منبع|citation needed)(?::\s*([^\]\n]+))?\](?![(\[])")
CODE_RE = re.compile(r"(^[ \t]*```.*?^[ \t]*```|`[^`\n]+`)", re.M | re.S)
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
SKIP_FOR_LIST = ("needs-sources",)

_cache: dict[str, dict] = {}


# ---------------------------------------------------------------- helpers

def _lang(config) -> str:
    return config.theme.get("language", "fa") or "fa"


def _outside_code(text: str, func) -> str:
    parts = CODE_RE.split(text)
    return "".join(p if CODE_RE.fullmatch(p) else func(p) for p in parts)


def _num(n: int, lang: str) -> str:
    return str(n).translate(PERSIAN_DIGITS) if lang == "fa" else str(n)


def _file_lang(path: Path) -> str:
    return "en" if path.name.endswith(".en.md") else "fa"


def _front_matter(text: str) -> dict:
    m = FRONT_RE.match(text)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def _plain(line: str) -> str:
    """Strip the most common Markdown syntax from a line for a short excerpt."""
    line = re.sub(r"^[\s>*\-\d.|#]+", "", line)
    line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
    line = re.sub(r"[*_`|]", "", line)
    return line.strip()


def _scan(docs_dir: Path, lang: str) -> dict:
    """Collect documents and needs-source markers for one language."""
    if lang in _cache:
        return _cache[lang]
    docs, total = [], 0
    for path in sorted(docs_dir.rglob("*.md")):
        rel = path.relative_to(docs_dir).as_posix()
        if _file_lang(path) != lang or any(s in rel for s in SKIP_FOR_LIST):
            continue
        text = path.read_text(encoding="utf-8")
        meta = _front_matter(text)
        body = FRONT_RE.sub("", text)
        items = []
        stripped = CODE_RE.sub("", body)
        for line in stripped.splitlines():
            for m in MARKER_RE.finditer(line):
                excerpt = _plain(MARKER_RE.sub("", line))
                if len(excerpt) > 220:
                    # Keep the part of the sentence right before the marker.
                    before = _plain(MARKER_RE.sub("", line[: m.start()]))
                    excerpt = "… " + before[-200:] if before else excerpt[:200] + " …"
                items.append({"excerpt": excerpt, "detail": (m.group(2) or "").strip()})
        total += len(items)
        docs.append({"rel": rel, "title": meta.get("title") or rel, "status": meta.get("status"), "items": items})
    _cache[lang] = {"docs": docs, "total": total}
    return _cache[lang]


# ---------------------------------------------------------------- transforms

def _summary(markdown: str) -> str:
    def repl(m: re.Match) -> str:
        lines = [re.sub(r"^>[ \t]?", "", l) for l in m.group(2).rstrip("\n").split("\n")]
        body = "\n".join("    " + l if l.strip() else "" for l in lines)
        return f'!!! simple "{m.group(1)}"\n\n{body}\n\n'

    return SUMMARY_RE.sub(repl, markdown)


def _markers(markdown: str, page, lang: str) -> tuple[str, int]:
    count = 0
    src_dir = posixpath.dirname(page.file.src_uri)
    target = posixpath.relpath("needs-sources.md", src_dir or ".")
    label_default = "نیاز به منبع" if lang == "fa" else "citation needed"
    tip_default = (
        "این ادعا هنوز منبع ندارد. اگر منبع معتبری می‌شناسید، کمک کنید."
        if lang == "fa"
        else "This claim has no source yet. If you know a reliable source, please help."
    )

    def repl(m: re.Match) -> str:
        nonlocal count
        count += 1
        label = m.group(1) or label_default
        tip = (m.group(2) or tip_default).replace('"', "'")
        return f'[{label}]({target}){{ .needs-source title="{tip}" }}'

    return _outside_code(markdown, lambda t: MARKER_RE.sub(repl, t)), count


def _needs_sources_page(markdown: str, docs_dir: Path, lang: str) -> str:
    data = _scan(docs_dir, lang)
    out = []
    docs_with = [d for d in data["docs"] if d["items"]]
    if lang == "fa":
        out.append(
            f"در حال حاضر **{_num(data['total'], lang)} ادعا** در "
            f"**{_num(len(docs_with), lang)} سند** منتظر منبع است.\n"
        )
    else:
        out.append(f"There are currently **{data['total']} claims** in **{len(docs_with)} documents** waiting for a source.\n")
    for d in sorted(docs_with, key=lambda d: -len(d["items"])):
        n = _num(len(d["items"]), lang)
        link = d["rel"].replace(".en.md", ".md")
        out.append(f"\n### [{d['title']}]({link}) · {n}\n")
        for item in d["items"]:
            detail = f" — *{item['detail']}*" if item["detail"] else ""
            excerpt = item["excerpt"] or "…"
            out.append(f"- {excerpt}{detail}")
    return markdown.replace("<!-- gozar:needs-sources -->", "\n".join(out) + "\n")


SECTION_TITLES = {
    "fa": {"": "برنامه", "institutions": "نهادها", "topics": "موضوعات فرابخشی", "international": "نامه‌های سرگشاده"},
    "en": {"": "The plan", "institutions": "Institutions", "topics": "Topics", "international": "Open letters"},
}


def _pdf_list(markdown: str, docs_dir: Path, page, lang: str) -> str:
    """Replace <!-- gozar:pdf-list --> with links to every plan document's PDF."""
    if "<!-- gozar:pdf-list -->" not in markdown:
        return markdown
    data = _scan(docs_dir, lang)
    page_dir = _page_dir(page)
    groups: dict[str, list] = {}
    for d in data["docs"]:
        if not d["status"]:
            continue
        stem = re.sub(r"(\.en)?\.md$", "", d["rel"])
        folder = stem.split("/")[0] if "/" in stem else ""
        groups.setdefault(folder, []).append((stem, d["title"]))
    out = []
    for folder in ["", "institutions", "topics", "international"]:
        if folder not in groups:
            continue
        out.append(f'<h3>{SECTION_TITLES[lang][folder]}</h3>\n<ul class="gozar-pdf-list">')
        for stem, title in sorted(groups[folder], key=lambda x: x[0]):
            href = posixpath.relpath(f"pdf/{lang}/{stem}.pdf", page_dir or ".")
            out.append(f'<li><a href="{href}" download>{title}</a></li>')
        out.append("</ul>")
    return markdown.replace("<!-- gozar:pdf-list -->", "\n".join(out))


def _page_dir(page) -> str:
    url = page.url or ""
    return url.rstrip("/") if url.endswith("/") else posixpath.dirname(url)


def _site_root(markdown: str, page) -> str:
    """Replace %%ROOT%% with the relative path from this page to the site root.

    Used for links to files that exist only in the deployed site (PDFs, the offline ZIP),
    which MkDocs cannot validate as Markdown links.
    """
    if "%%ROOT%%" not in markdown:
        return markdown
    rel = posixpath.relpath(".", _page_dir(page) or ".")
    return markdown.replace("%%ROOT%%", "" if rel == "." else rel + "/")


def _placeholders(markdown: str, docs_dir: Path, lang: str) -> str:
    if "<!-- gozar:" not in markdown:
        return markdown
    data = _scan(docs_dir, lang)
    plan_docs = [d for d in data["docs"] if d["status"]]
    values = {
        "doc-count": _num(len(plan_docs), lang),
        "needs-source-count": _num(data["total"], lang),
        "institution-count": _num(len([d for d in plan_docs if d["rel"].startswith("institutions/")]), lang),
        "topic-count": _num(len([d for d in plan_docs if d["rel"].startswith("topics/")]), lang),
    }
    for key, value in values.items():
        markdown = markdown.replace(f"<!-- gozar:{key} -->", value)
    return markdown


# ---------------------------------------------------------------- MkDocs events

@event_priority(100)  # before Material's offline plugin, which would otherwise add a CDN script
def on_config(config, **kwargs):
    if os.environ.get("GOZAR_OFFLINE", "").lower() in ("1", "true", "yes"):
        # Offline search needs the iframe-worker shim; use the bundled copy, never unpkg.com.
        config.extra["polyfills"] = ["assets/js/vendor/iframe-worker-shim.js"]
    return config


_build = {"depth": 0, "root": None}


def on_pre_build(config, **kwargs):
    # mkdocs-static-i18n runs the English build *inside* the Persian build's post_build step,
    # so builds nest; remember the outermost site directory.
    _build["depth"] += 1
    if _build["depth"] == 1:
        _build["root"] = Path(config.site_dir)
    _cache.clear()


def on_page_markdown(markdown, page, config, files, **kwargs):
    lang = _lang(config)
    docs_dir = Path(config.docs_dir)
    file_locale = getattr(page.file, "locale", None) or ("en" if page.file.src_uri.endswith(".en.md") else "fa")

    if page.file.src_uri.startswith("needs-sources"):
        markdown = _needs_sources_page(markdown, docs_dir, lang)
    markdown = _placeholders(markdown, docs_dir, lang)
    markdown = _pdf_list(markdown, docs_dir, page, lang)
    markdown = _site_root(markdown, page)
    markdown = _summary(markdown)
    markdown, count = _markers(markdown, page, file_locale)
    page.meta["gozar_needs_source"] = count

    if file_locale != lang:
        page.meta["gozar_fallback"] = True
        if lang == "en":
            notice = (
                '!!! info "Not yet translated"\n\n'
                "    This page is currently available only in Persian. "
                "The original text is shown below. "
                "[Help translate it](https://github.com/25mordad/iran-gozar/issues/new?template=translation.yml"
                f"&document=docs/{page.file.src_uri}).\n\n"
            )
            markdown = notice + markdown

    if page.meta.get("status"):
        stem = re.sub(r"(\.en)?\.md$", "", page.file.src_uri)
        page.meta["gozar_pdf"] = f"pdf/{file_locale}/{stem}.pdf"
        page.meta["gozar_src"] = f"docs/{page.file.src_uri}"
    return markdown


@event_priority(-200)  # after the search, i18n and offline plugins have written the index
def on_post_build(config, **kwargs):
    """Make the search index smaller: compact UTF-8, and one index per language.

    MkDocs writes the index with every Persian letter escaped as \\uXXXX (about three
    times larger than necessary), and mkdocs-static-i18n puts both languages in one file.
    The Persian site keeps search/search_index.json with Persian pages only; the English
    site gets en/search/search_index.json (overrides/main.html points English pages to it).
    """
    _build["depth"] -= 1
    if _build["depth"] > 0:  # the merged index is complete only when the outermost build ends
        return
    site = _build["root"] or Path(config.site_dir)
    index = site / "search" / "search_index.json"
    if not index.exists():
        return
    data = json.loads(index.read_text(encoding="utf-8"))
    docs = data.get("docs", [])
    parts = {
        index: [d for d in docs if not d["location"].startswith("en/")],
        site / "en" / "search" / "search_index.json": [d for d in docs if d["location"].startswith("en/")],
    }
    for path, entries in parts.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        compact = json.dumps({**data, "docs": entries}, ensure_ascii=False, separators=(",", ":"))
        path.write_text(compact, encoding="utf-8")
    script = index.with_suffix(".js")
    if script.exists():  # offline build: one combined index inlined into a script
        combined = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        script.write_text(f"var __index = {combined}", encoding="utf-8")
