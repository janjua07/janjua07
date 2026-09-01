#!/usr/bin/env python3
"""Convert the prepared portrait into a self typing SVG."""
from __future__ import annotations

import argparse
import html
from pathlib import Path

from PIL import Image

RAMP = " .`:-=+*cs#%@"
COLS = 74
ROWS = 42
SVG_W = 370
SVG_H = 470


def image_to_lines(path: Path) -> list[str]:
    image = Image.open(path).convert("L")
    image = image.resize((COLS, ROWS), Image.Resampling.LANCZOS)
    lines: list[str] = []
    for y in range(ROWS):
        chars = []
        for x in range(COLS):
            value = image.getpixel((x, y))
            index = round((255 - value) / 255 * (len(RAMP) - 1))
            chars.append(RAMP[index])
        lines.append("".join(chars).rstrip())
    return lines


def render(lines: list[str]) -> str:
    defs = []
    rows = []
    for i, line in enumerate(lines):
        delay = 0.20 + i * 0.045
        y = 62 + i * 8.45
        defs.append(
            f'<clipPath id="row{i}"><rect x="20" y="{y - 7:.2f}" width="330" height="10">'
            f'<animate attributeName="width" values="0;330" dur="0.44s" begin="{delay:.3f}s" fill="freeze" />'
            f'</rect></clipPath>'
        )
        safe = html.escape(line)
        rows.append(
            f'<text x="20" y="{y:.2f}" clip-path="url(#row{i})" class="art">{safe}</text>'
        )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="370" height="470" viewBox="0 0 {SVG_W} {SVG_H}" role="img" aria-labelledby="title desc">
<title id="title">Animated ASCII portrait of Ren</title>
<desc id="desc">A monochrome portrait prints itself row by row inside a red terminal frame.</desc>
<defs>{''.join(defs)}</defs>
<style>
  .art {{ fill:#f4f0eb; font: 7.25px ui-monospace,SFMono-Regular,Consolas,Liberation Mono,monospace; white-space:pre; }}
  .meta {{ fill:#ff224f; font: 700 11px ui-monospace,SFMono-Regular,Consolas,monospace; letter-spacing:1px; }}
  @keyframes blink {{ 0%,45%{{opacity:1}} 46%,100%{{opacity:0}} }}
  .cursor {{ animation:blink .8s steps(1) 7; }}
</style>
<rect width="370" height="470" rx="18" fill="#0b0b0f" />
<path d="M0 0H118L82 18H0Z M370 470H252L288 452H370Z" fill="#d81035" />
<rect x="9" y="9" width="352" height="452" rx="13" fill="none" stroke="#47101d" />
<circle cx="24" cy="28" r="4" fill="#ff224f"/><circle cx="38" cy="28" r="4" fill="#6f1427"/><circle cx="52" cy="28" r="4" fill="#35121a"/>
<text x="68" y="32" class="meta">PORTRAIT.EXE</text>
<path d="M20 43H350" stroke="#3b1720" />
{''.join(rows)}
<rect class="cursor" x="20" y="424" width="7" height="10" fill="#ff224f" />
<text x="20" y="452" class="meta">REN // PLAYER ONE</text>
</svg>'''


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", type=Path, default=Path("source-prepped.png"))
    parser.add_argument("-o", "--output", type=Path, default=Path("ascii-portrait.svg"))
    args = parser.parse_args()
    lines = image_to_lines(args.source)
    args.output.write_text(render(lines), encoding="utf-8")
    print(f"wrote {args.output} with {len(lines)} animated rows")


if __name__ == "__main__":
    main()
