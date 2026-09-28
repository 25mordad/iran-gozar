#!/usr/bin/env python3
"""Build PDF files of the plan documents from the already-built website.

For every plan document (a page with ``status`` in its front matter) this writes
``<out>/<lang>/<path>.pdf``, which is where the "Download PDF" button points.
It also writes one complete PDF of the whole plan per language:
``<out>/gozar-fa.pdf`` and ``<out>/gozar-en.pdf``, for sharing on Telegram and elsewhere.

Usage:
    mkdocs build
    python scripts/build_pdfs.py --site site --out site/pdf

Requires:  pip install -r requirements-pdf.txt && python -m playwright install chromium
Set PLAYWRIGHT_CHROMIUM_EXECUTABLE to use an existing Chromium instead.
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import html
import http.server
import json
import os
import re
import sys
import threading
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE_URL = "https://25mordad.github.io/iran-gozar/"
FRONT_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)

# Hide everything that is not the document itself.
PRINT_CSS = """
@font-face { font-family: "VazirmatnPrint"; font-weight: 400; src: url("/assets/fonts/print/Vazirmatn-Regular.woff2") format("woff2"); }
@font-face { font-family: "VazirmatnPrint"; font-weight: 600; src: url("/assets/fonts/print/Vazirmatn-SemiBold.woff2") format("woff2"); }
@font-face { font-family: "VazirmatnPrint"; font-weight: 700; src: url("/assets/fonts/print/Vazirmatn-Bold.woff2") format("woff2"); }
@font-face { font-family: "VazirmatnPrint"; font-weight: 800; src: url("/assets/fonts/print/Vazirmatn-ExtraBold.woff2") format("woff2"); }
/* Static fonts embed far more compactly in PDFs than the variable font used on the site. */
:root, body, .md-typeset, .gozar-fallback { --md-text-font: "VazirmatnPrint"; font-family: "VazirmatnPrint", sans-serif !important; }
@page { size: A4; margin: 16mm 15mm 18mm 15mm; }
html, body { background: #fff !important; }
.md-header, .md-tabs, .md-sidebar, .md-footer, .md-top, .md-dialog, .md-search,
.gozar-actions, .gozar-share-menu, .md-content__button, .md-source-file, .headerlink,
.gozar-status__sources, .md-banner, .md-announce { display: none !important; }
.md-main__inner, .md-grid { margin: 0 !important; max-width: none !important; }
.md-content { max-width: none !important; margin: 0 !important; }
.md-content__inner { margin: 0 !important; padding: 0 !important; }
.md-typeset { font-size: 10.5pt !important; line-height: 1.85 !important; }
[dir="ltr"] .md-typeset { line-height: 1.6 !important; }
.md-typeset h1 { font-size: 20pt !important; }
.md-typeset h2 { font-size: 14pt !important; break-after: avoid; }
.md-typeset h3 { font-size: 12pt !important; break-after: avoid; }
.md-typeset table, .md-typeset .admonition, .gozar-phase, .gozar-card { break-inside: avoid; }
.md-typeset a { color: #0b5563 !important; text-decoration: none; }
.md-typeset a.needs-source { border: 1px dashed #b07800 !important; color: #8a5d00 !important; }
.md-typeset__table { display: block; overflow: visible !important; }
.md-typeset table:not([class]) { font-size: 8.5pt !important; }
.gozar-doc { break-before: page; }
.gozar-doc:first-of-type { break-before: auto; }
"""

FOOTER = (
    '<div style="font-size:7px;width:100%;text-align:center;color:#888;'
    'font-family:Helvetica,Arial,sans-serif;">'
    'Gozar · <span class="pageNumber"></span> / <span class="totalPages"></span> · '
    "25mordad.github.io/iran-gozar · CC BY-SA 4.0</div>"
)


class _Loader(yaml.SafeLoader):
    """YAML loader that ignores the !!python tags used in mkdocs.yml."""


_Loader.add_multi_constructor("tag:yaml.org,2002:python/", lambda loader, suffix, node: None)
_Loader.add_multi_constructor("!", lambda loader, suffix, node: None)


def nav_order() -> list[str]:
    """Documentation files in navigation order (Persian/default names)."""
    config = yaml.load((ROOT / "mkdocs.yml").read_text(encoding="utf-8"), Loader=_Loader)
    order: list[str] = []

    def walk(items):
        for item in items or []:
            if isinstance(item, str):
                order.append(item)
            elif isinstance(item, dict):
                for value in item.values():
                    if isinstance(value, str):
                        order.append(value)
                    else:
                        walk(value)

    walk(config.get("nav"))
    if not order:  # no explicit nav: fall back to alphabetical order
        order = sorted(p.relative_to(DOCS).as_posix() for p in DOCS.rglob("*.md") if ".en." not in p.name)
    return order


def plan_documents(lang: str) -> list[dict]:
    docs = []
    for rel in nav_order():
        src = DOCS / (rel if lang == "fa" else rel.replace(".md", ".en.md"))
        if not src.exists():
            continue
        m = FRONT_RE.match(src.read_text(encoding="utf-8"))
        try:
            meta = yaml.safe_load(m.group(1)) if m else {}
        except yaml.YAMLError:
            print(f"warning: invalid front matter in {src}", file=sys.stderr)
            meta = {}
        if not meta or not meta.get("status"):
            continue
        stem = rel[:-3]
        page = stem[: -len("index")] if stem.endswith("index") else stem + "/"
        prefix = "" if lang == "fa" else "en/"
        docs.append({
            "rel": rel,
            "stem": stem,
            "title": meta.get("title", stem),
            "url_path": prefix + page,
            "anchor": "doc-" + re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-"),
        })
    return docs


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def stylesheets(site: Path) -> list[str]:
    """The site's stylesheet paths (Material's file names contain a content hash)."""
    index = (site / "index.html").read_text(encoding="utf-8")
    return re.findall(r'<link rel="stylesheet" href="([^"]+\.css)"', index)


def serve(site: Path) -> tuple[http.server.ThreadingHTTPServer, str]:
    handler = functools.partial(_QuietHandler, directory=str(site))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}/"


def launch(p):
    exe = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    return p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()


def open_page(browser, url: str):
    page = browser.new_page(color_scheme="light", viewport={"width": 1100, "height": 1400})
    page.goto(url, wait_until="networkidle")
    page.add_style_tag(content=PRINT_CSS)
    page.emulate_media(media="print", color_scheme="light")
    page.evaluate("document.fonts.ready")
    return page


def page_pdf(page, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    page.pdf(path=str(target), format="A4", print_background=True, display_header_footer=True,
             header_template="<div></div>", footer_template=FOOTER,
             margin={"top": "16mm", "bottom": "18mm", "left": "15mm", "right": "15mm"})


EXTRACT_JS = """
() => {
  const article = document.querySelector('article.md-content__inner');
  const clone = article.cloneNode(true);
  clone.querySelectorAll('.gozar-actions, .gozar-share-menu, .md-content__button, .md-source-file, .headerlink, .gozar-status__sources')
       .forEach(el => el.remove());
  clone.querySelectorAll('a[href]').forEach(a => a.setAttribute('href', a.href));
  clone.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
  return clone.innerHTML;
}
"""


def combined_html(lang: str, docs: list[dict], bodies: list[str], base: str, sha: str, css: list[str]) -> str:
    en = lang == "en"
    anchors = {d["url_path"]: d["anchor"] for d in docs}

    def fix_links(body: str) -> str:
        def repl(m):
            href = html.unescape(m.group(1))
            if not href.startswith(base):
                return m.group(0)
            path, _, frag = href[len(base):].partition("#")
            if path in anchors and not frag:
                return f'href="#{anchors[path]}"'
            return f'href="{html.escape(SITE_URL + path + ("#" + frag if frag else ""))}"'
        return re.sub(r'href="([^"]+)"', repl, body)

    today = dt.date.today().isoformat()
    title = "Gozar" if en else "گذار"
    subtitle = ("An open, critiqueable plan for Iran's transition to democracy — without collapse, without violence"
                if en else "برنامه‌ای باز و قابل‌نقد برای گذار ایران به دموکراسی: بدون فروپاشی، بدون خشونت")
    note = (
        "Drafted by an artificial intelligence, which says so openly. Every document is a draft, open to "
        "criticism and correction by anyone. Final decisions belong to the free vote of the people of Iran."
        if en else
        "پیش‌نویس این برنامه را یک هوش مصنوعی نوشته و خودش هم این را پنهان نمی‌کند. همه‌ی اسناد پیش‌نویس‌اند "
        "و هر کسی می‌تواند آن‌ها را نقد و اصلاح کند. تصمیم نهایی با رأی آزاد مردم ایران است."
    )
    if not en:
        today = today.translate(str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹"))
    version = (f"Version of {today}" if en else f"نسخه‌ی {today}") + (f" · {sha[:7]}" if sha else "")
    online = SITE_URL + ("en/" if en else "")
    toc = "\n".join(f'<li><a href="#{d["anchor"]}">{html.escape(str(d["title"]))}</a></li>' for d in docs)
    sections = "\n".join(
        f'<section class="gozar-doc" id="{d["anchor"]}">{fix_links(b)}</section>' for d, b in zip(docs, bodies)
    )
    direction = "ltr" if en else "rtl"
    links = "\n".join(f'<link rel="stylesheet" href="{base}{href}">' for href in css)
    return f"""<!doctype html>
<html lang="{lang}" dir="{direction}">
<head>
<meta charset="utf-8">
<title>{title}</title>
{links}
<style>
body {{ margin: 0; }}
.cover {{ height: 250mm; display: flex; flex-direction: column; justify-content: center; text-align: center; break-after: page; }}
.cover h1 {{ font-size: 48pt; color: #0b5563; margin: 0; }}
.cover .sub {{ font-size: 15pt; margin: 8mm 20mm; }}
.cover .note {{ font-size: 11pt; margin: 10mm 25mm; color: #444; line-height: 1.9; }}
.cover .meta {{ font-size: 9pt; color: #777; direction: ltr; }}
.toc {{ break-after: page; }}
.toc ol {{ font-size: 11pt; line-height: 2; }}
</style>
</head>
<body dir="{direction}" data-md-color-scheme="default" data-md-color-primary="custom" data-md-color-accent="custom">
<div class="md-typeset">
<div class="cover">
  <h1>{title}</h1>
  <div class="sub">{html.escape(subtitle)}</div>
  <div class="note">{html.escape(note)}</div>
  <div class="meta">{html.escape(version)}<br>{online}<br>CC BY-SA 4.0</div>
</div>
<div class="toc"><h2>{"Contents" if en else "فهرست"}</h2><ol>{toc}</ol></div>
{sections}
</div>
</body>
</html>"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--site", default="site", type=Path)
    parser.add_argument("--out", default=None, type=Path)
    parser.add_argument("--lang", choices=["fa", "en"], action="append")
    parser.add_argument("--only-full", action="store_true", help="only build the complete PDFs")
    args = parser.parse_args()
    site = args.site.resolve()
    out = (args.out or site / "pdf").resolve()
    langs = args.lang or ["fa", "en"]
    sha = os.environ.get("GITHUB_SHA", "")
    if not (site / "index.html").exists():
        print(f"error: {site} has no index.html; run `mkdocs build` first", file=sys.stderr)
        return 1

    server, base = serve(site)
    failures = 0
    manifest = {}
    try:
        with sync_playwright() as p:
            browser = launch(p)
            for lang in langs:
                docs = plan_documents(lang)
                bodies = []
                for d in docs:
                    try:
                        page = open_page(browser, base + d["url_path"])
                        if not args.only_full:
                            page_pdf(page, out / lang / f"{d['stem']}.pdf")
                        bodies.append(page.evaluate(EXTRACT_JS))
                        page.close()
                        print(f"ok   {lang} {d['stem']}")
                    except Exception as exc:  # keep going; report at the end
                        failures += 1
                        bodies.append(f"<p>{html.escape(str(d['title']))}: {html.escape(str(exc))}</p>")
                        print(f"FAIL {lang} {d['stem']}: {exc}", file=sys.stderr)
                if docs:
                    tmp = site / f"_gozar-full-{lang}.html"
                    tmp.write_text(combined_html(lang, docs, bodies, base, sha, stylesheets(site)), encoding="utf-8")
                    page = open_page(browser, base + tmp.name)
                    page_pdf(page, out / f"gozar-{lang}.pdf")
                    page.close()
                    tmp.unlink()
                    print(f"ok   {lang} complete plan -> gozar-{lang}.pdf ({len(docs)} documents)")
                manifest[lang] = [d["stem"] for d in docs]
            browser.close()
    finally:
        server.shutdown()
    (out / "index.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
