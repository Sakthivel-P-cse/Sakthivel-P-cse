#!/usr/bin/env python3
import argparse
import datetime as dt
import html
import json


PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]
BG_TOP = "#111722"
BG_BOTTOM = "#0a0e14"
FRAME = "#1f6feb"
MUTED = "#7d8590"
TEXT = "#e6edf3"
CYAN = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"
CELL = 11
GAP = 3
STEP = CELL + GAP


def level(count):
    if count == 0:
        return 0
    if count <= 5:
        return 1
    if count <= 15:
        return 2
    if count <= 30:
        return 3
    if count <= 50:
        return 4
    return 5


def grid_for(days):
    values = {dt.date.fromisoformat(day["date"]): day["count"] for day in days}
    first = min(values)
    last = max(values)
    first_sunday = first - dt.timedelta(days=(first.weekday() + 1) % 7)
    last_sunday = last - dt.timedelta(days=(last.weekday() + 1) % 7)
    columns = []
    cursor = first_sunday
    while cursor <= last_sunday:
        column = []
        for row in range(7):
            date = cursor + dt.timedelta(days=row)
            if date in values:
                column.append((date, values[date]))
            else:
                column.append(None)
        columns.append(column)
        cursor += dt.timedelta(days=7)
    return columns


def render(data, output, static):
    columns = grid_for(data["days"])
    width = 820
    grid_left = 44
    grid_top = 66
    grid_width = len(columns) * STEP
    grid_height = 7 * STEP
    footer_top = grid_top + grid_height + 28
    height = footer_top + 92
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        "<defs>"
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/>'
        "</linearGradient>"
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="12" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="{FRAME}" stroke-opacity="0.6"/>',
        '<line x1="0" y1="34" x2="820" y2="34" stroke="#1f6feb" stroke-opacity="0.35"/>',
        '<circle cx="26" cy="17" r="5" fill="#ff5f56"/>',
        '<circle cx="42" cy="17" r="5" fill="#ffbd2e"/>',
        '<circle cx="58" cy="17" r="5" fill="#27c93f"/>',
        f'<text x="410" y="21" fill="{MUTED}" font-size="12" text-anchor="middle">sakthi@github: ~/contributions --graph</text>',
    ]

    month_labels = []
    seen = set()
    for index, column in enumerate(columns):
        for cell in column:
            if cell is None:
                continue
            month = (cell[0].year, cell[0].month)
            if month not in seen and cell[0].day <= 7:
                seen.add(month)
                month_labels.append((index, cell[0].strftime("%b")))
            break
    for index, label in month_labels:
        parts.append(f'<text x="{grid_left + index * STEP}" y="52" fill="{MUTED}" font-size="10">{label}</text>')
    for row, label in [(1, "Mon"), (3, "Wed"), (5, "Fri")]:
        parts.append(f'<text x="14" y="{grid_top + row * STEP + 10}" fill="{MUTED}" font-size="9">{label}</text>')

    serial = 0
    for column_index, column in enumerate(columns):
        for row, cell in enumerate(column):
            if cell is None:
                continue
            date, count = cell
            x = grid_left + column_index * STEP
            y = grid_top + row * STEP
            delay = (column_index * 0.018) + (row * 0.045)
            plural = "" if count == 1 else "s"
            label = html.escape(f"{date.isoformat()}: {count} contribution{plural}")
            parts.append(
                f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2.5" fill="{PALETTE[level(count)]}">'
                f'<title>{label}</title>'
            )
            if not static:
                parts.extend([
                    f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.3f}s" dur="0.35s" fill="freeze"/>',
                    f'<animateTransform attributeName="transform" type="translate" from="0 -6" to="0 0" '
                    f'begin="{delay:.3f}s" dur="0.35s" fill="freeze"/>',
                ])
            parts.append("</rect>")
            serial += 1

    legend_y = grid_top + grid_height + 8
    legend_x = width - 188
    parts.append(f'<text x="{legend_x}" y="{legend_y + 10}" fill="{MUTED}" font-size="10" text-anchor="end">Less</text>')
    for index, color in enumerate(PALETTE):
        parts.append(
            f'<rect x="{legend_x + 10 + index * 15}" y="{legend_y}" width="11" height="11" rx="2" fill="{color}"/>'
        )
    parts.append(f'<text x="{legend_x + 105}" y="{legend_y + 10}" fill="{MUTED}" font-size="10">More</text>')
    parts.extend([
        f'<line x1="0" y1="{footer_top}" x2="{width}" y2="{footer_top}" stroke="{FRAME}" stroke-opacity="0.3"/>',
        f'<text x="22" y="{footer_top + 28}" fill="{GREEN}" font-size="14"><tspan font-weight="700">{data["total_contributions"]:,}</tspan><tspan fill="{MUTED}"> contributions in the last year</tspan></text>',
        f'<text x="{width - 22}" y="{footer_top + 28}" fill="{MUTED}" font-size="11" text-anchor="end">{data["range"]["start"]} &#8594; {data["range"]["end"]}</text>',
        f'<text x="22" y="{footer_top + 56}" fill="{MUTED}" font-size="13">current streak <tspan fill="{CYAN}" font-weight="700">{data["current_streak"]} days</tspan><tspan fill="{MUTED}"> · longest </tspan><tspan fill="{CYAN}" font-weight="700">{data["longest_streak"]} days</tspan></text>',
        f'<text x="{width - 22}" y="{footer_top + 56}" fill="{MUTED}" font-size="11" text-anchor="end">best day <tspan fill="{GOLD}" font-weight="700">{data["best_day"]["count"]}</tspan> on {data["best_day"]["date"]}</text>',
        "</svg>",
    ])
    with open(output, "w", encoding="utf-8") as handle:
        handle.write("".join(parts))
    print(f"wrote {output}: {serial} cells")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default="data/contributions.json")
    parser.add_argument("output", nargs="?", default="contrib-heatmap.svg")
    parser.add_argument("--static", action="store_true")
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as handle:
        contribution_data = json.load(handle)
    render(contribution_data, args.output, args.static)
