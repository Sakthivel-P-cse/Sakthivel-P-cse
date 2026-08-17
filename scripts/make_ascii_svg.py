#!/usr/bin/env python3
import argparse
import html
import os

from PIL import Image, ImageEnhance


RAMP = " .`:-=+*cs#%@"
COLS = 74
ROWS = 64
CELL_W = 8
CELL_H = 13
PAD = 22
TITLE_H = 32
STATUS_H = 34
INK = "#c9d1d9"
MUTED = "#7d8590"
FRAME = "#30363d"
BG_TOP = "#111722"
BG_BOTTOM = "#0d1117"


def build(source, output, static):
    image = Image.open(source).convert("L").resize((COLS, ROWS), Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    pixels = image.load()
    art_width = COLS * CELL_W
    art_height = ROWS * CELL_H
    width = art_width + PAD * 2
    height = TITLE_H + art_height + STATUS_H + PAD
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        "<defs>"
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/>'
        "</linearGradient>"
        "</defs>",
        f'<rect width="{width}" height="{height}" rx="12" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="12" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="{TITLE_H}" x2="{width}" y2="{TITLE_H}" stroke="{FRAME}"/>',
    ]
    for index, color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + index * 16}" cy="{TITLE_H / 2}" r="5" fill="{color}"/>')
    parts.append(
        f'<text x="{width / 2}" y="{TITLE_H / 2 + 4}" fill="{MUTED}" font-size="12" '
        'text-anchor="middle">sakthi@github:~$ ./portrait.sh</text>'
    )

    for row in range(ROWS):
        characters = []
        for column in range(COLS):
            luminance = pixels[column, row] / 255
            if luminance >= 0.84:
                characters.append(" ")
                continue
            index = int((1 - pow(luminance, 1.15)) * (len(RAMP) - 1) + 0.5)
            characters.append(RAMP[max(0, min(len(RAMP) - 1, index))])
        line = html.escape("".join(characters))
        y = TITLE_H + row * CELL_H + CELL_H * 0.76
        if static:
            parts.append(
                f'<text xml:space="preserve" x="{PAD}" y="{y:.1f}" fill="{INK}" '
                f'font-size="{CELL_H * 0.86:.1f}" textLength="{art_width}" lengthAdjust="spacing">{line}</text>'
            )
            continue
        clip_y = TITLE_H + row * CELL_H
        delay = row * 0.095
        parts.append(
            f'<clipPath id="row{row}"><rect x="{PAD}" y="{clip_y}" width="0" height="{CELL_H}">'
            f'<animate attributeName="width" from="0" to="{art_width}" begin="{delay:.3f}s" '
            'dur="0.48s" fill="freeze"/></rect></clipPath>'
        )
        parts.append(
            f'<g clip-path="url(#row{row})"><text xml:space="preserve" x="{PAD}" y="{y:.1f}" '
            f'fill="{INK}" font-size="{CELL_H * 0.86:.1f}" textLength="{art_width}" '
            f'lengthAdjust="spacing">{line}</text></g>'
        )
        parts.append(
            f'<rect x="{PAD}" y="{clip_y + 1}" width="{CELL_W}" height="{CELL_H - 2}" fill="{INK}" opacity="0">'
            f'<animate attributeName="x" from="{PAD}" to="{PAD + art_width}" begin="{delay:.3f}s" '
            'dur="0.48s" fill="freeze"/>'
            f'<set attributeName="opacity" to="0.82" begin="{delay:.3f}s"/>'
            f'<set attributeName="opacity" to="0" begin="{delay + 0.48:.3f}s"/></rect>'
        )

    status_y = TITLE_H + art_height + 22
    parts.extend([
        f'<line x1="0" y1="{TITLE_H + art_height + 4}" x2="{width}" y2="{TITLE_H + art_height + 4}" stroke="{FRAME}"/>',
        f'<text x="{PAD}" y="{status_y}" fill="{MUTED}" font-size="12">sakthi@github:~$ whoami '
        f'<tspan fill="{INK}">Sakthivel P</tspan></text>',
    ])
    if not static:
        parts.append(
            f'<rect x="{PAD + 172}" y="{status_y - 11}" width="7" height="13" fill="{INK}">'
            '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" '
            'dur="1s" repeatCount="indefinite"/></rect>'
        )
    parts.append("</svg>")
    with open(output, "w", encoding="utf-8") as handle:
        handle.write("".join(parts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", default="source-prepped.png")
    parser.add_argument("output", nargs="?", default="avi-ascii.svg")
    parser.add_argument("--static", action="store_true")
    args = parser.parse_args()
    build(args.source, args.output, args.static)
    print(f"wrote {args.output}")
