#!/usr/bin/env python3
"""Convert legacy `!!! simple "..."` admonitions to the portable blockquote form.

    > **خلاصه به زبان ساده**
    >
    > sentence one.
    > sentence two.

Usage: python scripts/convert_summary.py FILE [FILE ...]
"""
import re
import sys

RE = re.compile(r'^!!! simple "([^"]+)"\n((?:(?: {4}.*)?\n)+)', re.M)


def convert(text: str) -> str:
    def repl(m):
        title = m.group(1)
        body = [l[4:] if l.startswith("    ") else l for l in m.group(2).rstrip("\n").split("\n")]
        body = [l for l in body if l.strip()]
        out = [f"> **{title}**", ">"] + [f"> {l}" for l in body]
        return "\n".join(out) + "\n\n"
    return RE.sub(repl, text)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            src = f.read()
        new = convert(src)
        if new != src:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new)
            print(f"converted: {path}")
