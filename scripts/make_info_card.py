#!/usr/bin/env python3
import argparse
import html


WIDTH = 900
HEIGHT = 1010
PAD = 42
FRAME = "#30363d"
MUTED = "#8b949e"
TEXT = "#e6edf3"
CYAN = "#22d3ee"
GREEN = "#39d353"
GOLD = "#f2cc60"
BG_TOP = "#111722"
BG_BOTTOM = "#0d1117"


def text(value):
    return html.escape(value)


def build(output, static):
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
        f'viewBox="0 0 {WIDTH} {HEIGHT}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace">',
        "<defs>"
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/>'
        "</linearGradient>"
        "</defs>",
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="12" fill="url(#bg)"/>',
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="12" fill="none" stroke="{FRAME}"/>',
        '<line x1="0" y1="64" x2="900" y2="64" stroke="#30363d"/>',
        f'<circle cx="{PAD}" cy="32" r="5" fill="#ff5f56"/>',
        f'<circle cx="{PAD + 16}" cy="32" r="5" fill="#ffbd2e"/>',
        f'<circle cx="{PAD + 32}" cy="32" r="5" fill="#27c93f"/>',
        f'<text x="450" y="37" fill="{MUTED}" font-size="13" text-anchor="middle">sakthi@github:~$ neofetch</text>',
    ]
    rows = [
        ("name", "Sakthivel P", CYAN),
        ("role", "Distributed Systems &amp; Backend Engineer", GREEN),
        ("focus", "AI infrastructure · observability · cloud-native systems", TEXT),
        ("stack", "Go · Python · TypeScript · Java · SQL", TEXT),
        ("systems", "Raft · CRDTs · gRPC · Temporal · Kubernetes", TEXT),
        ("storage", "PostgreSQL · Redis · Qdrant · FAISS", TEXT),
        ("now", "building durable systems that survive failure", GOLD),
        ("education", "Chennai Institute of Technology · 8.1 CGPA", TEXT),
    ]
    for index, (key, value, color) in enumerate(rows):
        y = 144 + index * 70
        group = [
            f'<g opacity="0" transform="translate(0 10)">',
            f'<animate attributeName="opacity" from="0" to="1" begin="{0.15 + index * 0.12:.2f}s" dur="0.32s" fill="freeze"/>',
            f'<animateTransform attributeName="transform" type="translate" from="0 10" to="0 0" '
            f'begin="{0.15 + index * 0.12:.2f}s" dur="0.32s" fill="freeze"/>',
            f'<text x="{PAD}" y="{y}" fill="{CYAN}" font-size="16">{text(key).ljust(12)}</text>',
            f'<text x="210" y="{y}" fill="{color}" font-size="16">{value}</text>',
            "</g>",
        ]
        if static:
            group = [
                f'<text x="{PAD}" y="{y}" fill="{CYAN}" font-size="16">{text(key).ljust(12)}</text>',
                f'<text x="210" y="{y}" fill="{color}" font-size="16">{value}</text>',
            ]
        parts.extend(group)

    parts.extend([
        '<line x1="42" y1="735" x2="858" y2="735" stroke="#30363d"/>',
        f'<text x="{PAD}" y="790" fill="{MUTED}" font-size="14">highlighted builds</text>',
        f'<text x="{PAD}" y="830" fill="{TEXT}" font-size="17">Viper · CAUSA · AUTOBUILD · TrustChain</text>',
        f'<text x="{PAD}" y="885" fill="{MUTED}" font-size="14">links</text>',
        f'<text x="{PAD}" y="925" fill="{CYAN}" font-size="16">sakthivel-portfolio-ecru.vercel.app</text>',
        f'<text x="{PAD}" y="965" fill="{MUTED}" font-size="14">linkedin.com/in/sakthivel-p-00152a317</text>',
        "</svg>",
    ])
    with open(output, "w", encoding="utf-8") as handle:
        handle.write("".join(parts))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", default="info-card.svg")
    parser.add_argument("--static", action="store_true")
    args = parser.parse_args()
    build(args.output, args.static)
    print(f"wrote {args.output}")
