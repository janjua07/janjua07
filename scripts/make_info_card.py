#!/usr/bin/env python3
"""Generate Ren's animated operator card."""
from pathlib import Path

ROWS = [
    ("IDENTITY", "Ren"),
    ("CLASS", "Creative operator"),
    ("BUILDING", "Mexasoft"),
    ("SYSTEMS", "Hermes · Figma · Shopify"),
    ("GITHUB", "The canvas, not the job"),
    ("AFTER HOURS", "Persona · JRPGs · long runs"),
    ("RULE", "Own the system. Skip the template."),
]


def make_svg() -> str:
    rendered = []
    for i, (key, value) in enumerate(ROWS):
        y = 118 + i * 43
        rendered.append(f'''<g class="line l{i}">
  <text x="34" y="{y}" class="key">{key}</text>
  <text x="164" y="{y}" class="value">{value}</text>
</g>''')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="490" height="470" viewBox="0 0 490 470" role="img" aria-labelledby="title desc">
<title id="title">Ren operator card</title>
<desc id="desc">An animated terminal card describing Ren as a creative operator building Mexasoft and owned systems.</desc>
<style>
  .eyebrow {{ fill:#ff224f; font:700 11px ui-monospace,SFMono-Regular,Consolas,monospace; letter-spacing:2px; }}
  .name {{ fill:#f7f2ee; font:800 31px ui-monospace,SFMono-Regular,Consolas,monospace; letter-spacing:1px; }}
  .key {{ fill:#ff224f; font:700 11px ui-monospace,SFMono-Regular,Consolas,monospace; letter-spacing:1px; }}
  .value {{ fill:#ddd5d0; font:500 14px ui-monospace,SFMono-Regular,Consolas,monospace; }}
  .line {{ animation:reveal .5s cubic-bezier(.2,.8,.2,1) both; }}
  .l0{{animation-delay:.25s}} .l1{{animation-delay:.40s}} .l2{{animation-delay:.55s}}
  .l3{{animation-delay:.70s}} .l4{{animation-delay:.85s}} .l5{{animation-delay:1s}} .l6{{animation-delay:1.15s}}
  @keyframes reveal {{ from {{ opacity:0; transform:translate(0 8px); }} to {{ opacity:1; transform:translate(0 0); }} }}
  @keyframes pulse {{ 0%,100%{{opacity:.35}} 50%{{opacity:1}} }}
  .pulse {{ animation:pulse 1.7s ease-in-out infinite; }}
</style>
<rect width="490" height="470" rx="18" fill="#0b0b0f" />
<path d="M0 0H180L145 18H0Z M490 470H310L345 452H490Z" fill="#d81035" />
<rect x="9" y="9" width="472" height="452" rx="13" fill="none" stroke="#47101d" />
<text x="30" y="42" class="eyebrow">WHOAMI // PUBLIC BUILD</text>
<text x="30" y="79" class="name">REN<tspan fill="#ff224f">_</tspan></text>
<circle class="pulse" cx="454" cy="39" r="5" fill="#ff224f" />
<path d="M30 94H460" stroke="#3b1720" />
{''.join(rendered)}
<path d="M30 426H460" stroke="#3b1720" />
<text x="30" y="449" class="eyebrow">STATUS: BUILDING THE NEXT VERSION</text>
</svg>'''


if __name__ == "__main__":
    target = Path("info-card.svg")
    target.write_text(make_svg(), encoding="utf-8")
    print(f"wrote {target}")
