#!/usr/bin/env python3
"""Render a Persona red animated contribution heatmap."""
from __future__ import annotations

import calendar
import html
import json
from datetime import date
from pathlib import Path

SOURCE = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")
COLORS = ["#241419", "#591321", "#8d1428", "#c91335", "#ff224f"]


def main() -> None:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    days = data["days"]
    start = date.fromisoformat(days[0]["date"])
    start_sunday = start.toordinal() - ((start.weekday() + 1) % 7)
    cells = []
    month_positions: dict[str, int] = {}
    for item in days:
        day = date.fromisoformat(item["date"])
        offset = day.toordinal() - start_sunday
        col, row = divmod(offset, 7)
        x, y = 58 + col * 14, 58 + row * 14
        level = max(0, min(4, int(item["level"])))
        delay = 0.10 + (col + row) * 0.018
        label = html.escape(f"{item['date']}: {item['count']} contributions")
        cells.append(
            f'<rect class="cell" x="{x}" y="{y}" width="10" height="10" rx="2" fill="{COLORS[level]}" '
            f'style="animation-delay:{delay:.3f}s"><title>{label}</title></rect>'
        )
        month_key = day.strftime("%Y-%m")
        month_positions.setdefault(month_key, col)

    months = []
    last_x = -100
    for key, col in month_positions.items():
        x = 58 + col * 14
        if x - last_x >= 42:
            month_num = int(key[-2:])
            months.append(f'<text x="{x}" y="45" class="month">{calendar.month_abbr[month_num]}</text>')
            last_x = x

    total = data["total"]
    current = data["current_streak"]
    longest = data["longest_streak"]
    best = data["best_day"]
    best_text = f"BEST {best['count']} ON {best['date']}" if best["count"] else "FIRST COMMIT LOADING"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="860" height="205" viewBox="0 0 860 205" role="img" aria-labelledby="title desc">
<title id="title">Ren's live GitHub contribution grid</title>
<desc id="desc">An animated red contribution calendar generated from public GitHub activity.</desc>
<style>
  .label {{ fill:#ff224f; font:700 11px ui-monospace,SFMono-Regular,Consolas,monospace; letter-spacing:1px; }}
  .month,.day {{ fill:#8f7c82; font:10px ui-monospace,SFMono-Regular,Consolas,monospace; }}
  .stat {{ fill:#d9ced1; font:11px ui-monospace,SFMono-Regular,Consolas,monospace; }}
  .cell {{ animation:drop .38s cubic-bezier(.2,.8,.2,1) both; }}
  @keyframes drop {{ from {{ opacity:0; transform:translateY(-7px); }} to {{ opacity:1; transform:translateY(0); }} }}
</style>
<rect width="860" height="205" rx="18" fill="#0b0b0f" />
<path d="M0 0H205L167 18H0Z M860 205H655L693 187H860Z" fill="#d81035" />
<rect x="9" y="9" width="842" height="187" rx="13" fill="none" stroke="#47101d" />
<text x="27" y="31" class="label">CONTRIBUTIONS.SH // LIVE</text>
{''.join(months)}
<text x="27" y="69" class="day">M</text><text x="27" y="97" class="day">W</text><text x="27" y="125" class="day">F</text>
{''.join(cells)}
<path d="M27 163H833" stroke="#3b1720" />
<text x="27" y="183" class="stat">{total} TOTAL · {current} CURRENT STREAK · {longest} LONGEST · {best_text}</text>
</svg>'''
    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"rendered {len(cells)} cells -> {OUTPUT}")


if __name__ == "__main__":
    main()
