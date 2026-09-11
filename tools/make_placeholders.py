#!/usr/bin/env python3
"""
Generates steampunk-styled SVG placeholder graphics for TheGateKeeper.art.

Run:  python3 tools/make_placeholders.py
Out:  assets/*.svg  (hero.svg + gallery-01..08.svg + og.svg + favicon.svg)

These are DROP-IN PLACEHOLDERS. Replace with real photos by either:
  a) overwriting the file at the same path with a .jpg/.png and updating the
     `src` in index.html, or
  b) keeping the same filename and saving a real image as the same path.
Aspect ratios to match when shooting/exporting:
  hero    -> 4:3 (1600x1200)
  gallery -> 4:3 (1200x900)
"""
import math
import os
import random

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
os.makedirs(OUT, exist_ok=True)

W, H = 1200, 900
COPPER = "#b87333"
BRASS = "#c8a45c"
STEEL = "#8a8f96"

TITLES = [
    ("Iron Widow", "creatures"),
    ("The Mincer", "machines"),
    ("Loom Raider", "machines"),
    ("Spanner Fish", "creatures"),
    ("The GateKeeper", "signature"),
    ("Rust & Rivets", "curiosities"),
    ("Gearling", "creatures"),
    ("The Gate", "curiosities"),
    ("Copper Moth", "creatures"),
]


def esc(s):
    """XML-escape text destined for markup (raw '&' breaks SVG parsing)."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def gear(cx, cy, r, teeth, rot, fill, opacity):
    """A simple gear silhouette as a path."""
    opacity = float(opacity)
    pts = []
    tooth = r * 0.22
    for i in range(teeth * 2):
        a = rot + i * math.pi / teeth
        rad = r + (tooth if i % 2 == 0 else -tooth * 0.35)
        pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + " Z"
    hole = r * 0.30
    return (
        f'<path d="{d}" fill="{fill}" fill-opacity="{opacity}"/>'
        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{hole:.1f}" fill="#0d0a08" '
        f'fill-opacity="{min(0.95, opacity + 0.25)}"/>'
    )


def placeholder(idx, title, category, hero=False):
    w, h = (1600, 1200) if hero else (W, H)
    rnd = random.Random(idx * 977 + (7 if hero else 0))
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="{w}" height="{h}" role="img" '
        f'aria-label="{esc(title)} - placeholder artwork">',
        "<defs>",
        '<linearGradient id="plate" x1="0" y1="0" x2="1" y2="1">',
        '<stop offset="0" stop-color="#2b2320"/><stop offset="0.45" stop-color="#1a1512"/>',
        '<stop offset="1" stop-color="#100c0a"/></linearGradient>',
        '<linearGradient id="copperg" x1="0" y1="0" x2="1" y2="1">',
        f'<stop offset="0" stop-color="{BRASS}"/><stop offset="0.5" stop-color="{COPPER}"/>',
        '<stop offset="1" stop-color="#6d3d1c"/></linearGradient>',
        '<pattern id="hatch" width="16" height="16" patternUnits="userSpaceOnUse" '
        'patternTransform="rotate(45)">',
        '<line x1="0" y1="0" x2="0" y2="16" stroke="#ffffff" stroke-opacity="0.035" stroke-width="6"/>',
        "</pattern>",
        '<radialGradient id="vig" cx="0.5" cy="0.45" r="0.75">',
        '<stop offset="0.55" stop-color="#000" stop-opacity="0"/>',
        '<stop offset="1" stop-color="#000" stop-opacity="0.65"/></radialGradient>',
        "</defs>",
        f'<rect width="{w}" height="{h}" fill="url(#plate)"/>',
        f'<rect width="{w}" height="{h}" fill="url(#hatch)"/>',
    ]

    # rivet border
    rx, ry, pad = w / 2, h / 2, 26
    parts.append(
        f'<rect x="{pad}" y="{pad}" width="{w - pad * 2}" height="{h - pad * 2}" rx="6" '
        f'fill="none" stroke="url(#copperg)" stroke-opacity="0.55" stroke-width="3"/>'
    )
    step_x = (w - pad * 2) / 12
    step_y = (h - pad * 2) / 8
    for i in range(13):
        x = pad + i * step_x
        for y in (pad, h - pad):
            parts.append(f'<circle cx="{x:.1f}" cy="{y}" r="5" fill="url(#copperg)" fill-opacity="0.7"/>')
    for j in range(1, 8):
        y = pad + j * step_y
        for x in (pad, w - pad):
            parts.append(f'<circle cx="{x}" cy="{y:.1f}" r="5" fill="url(#copperg)" fill-opacity="0.7"/>')

    # gear cluster background
    gears = 16 if hero else 11
    for i in range(gears):
        cx = rnd.uniform(-60, w + 60)
        cy = rnd.uniform(-40, h + 40)
        r = rnd.uniform(w * 0.05, w * 0.17)
        teeth = rnd.choice([10, 12, 14, 16, 20])
        fill = rnd.choice([STEEL, COPPER, BRASS])
        op = rnd.uniform(0.05, 0.16)
        parts.append(gear(cx, cy, r, teeth, rnd.uniform(0, 6.3), fill, round(op, 3)))

    # centre text block
    cy_text = h / 2
    parts += [
        f'<text x="{w/2}" y="{cy_text - 34:.0f}" text-anchor="middle" '
        f'font-family="Georgia, \'Times New Roman\', serif" font-size="{int(w*0.072)}" '
        f'fill="#e9e0d2" fill-opacity="0.92" letter-spacing="4">{esc(title)}</text>',
        f'<line x1="{w*0.30:.0f}" y1="{cy_text + 6:.0f}" x2="{w*0.70:.0f}" y2="{cy_text + 6:.0f}" '
        f'stroke="url(#copperg)" stroke-width="2"/>',
        f'<text x="{w/2}" y="{cy_text + 56:.0f}" text-anchor="middle" '
        f'font-family="Menlo, Consolas, monospace" font-size="{int(w*0.021)}" '
        f'fill="{BRASS}" fill-opacity="0.85" letter-spacing="6">PLACEHOLDER &#183; {esc(category).upper()}</text>',
        f'<text x="{w/2}" y="{h - pad - 26:.0f}" text-anchor="middle" '
        f'font-family="Menlo, Consolas, monospace" font-size="{int(w*0.016)}" '
        f'fill="#8a8f96" fill-opacity="0.7">replace with real photo &#183; {w}x{h}</text>',
    ]
    parts.append(f'<rect width="{w}" height="{h}" fill="url(#vig)"/>')
    parts.append("</svg>")
    return "".join(parts)


def favicon():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64">'
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{BRASS}"/><stop offset="1" stop-color="#6d3d1c"/></linearGradient></defs>'
        '<rect width="64" height="64" rx="12" fill="#14100d"/>'
        + gear(32, 32, 22, 12, 0.2, "url(#g)", "1")
        + '<circle cx="32" cy="32" r="6" fill="#14100d"/>'
        '<path d="M20 44 L32 22 L44 44" fill="none" stroke="#e9e0d2" stroke-opacity="0.85" '
        'stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
        "</svg>"
    )


def main():
    written = []
    hero = placeholder(0, "The GateKeeper", "signature", hero=True)
    p = os.path.join(OUT, "hero.svg")
    open(p, "w", encoding="utf-8").write(hero)
    written.append(p)

    for i, (title, cat) in enumerate(TITLES, start=1):
        svg = placeholder(i, title, cat)
        p = os.path.join(OUT, f"gallery-{i:02d}.svg")
        open(p, "w", encoding="utf-8").write(svg)
        written.append(p)

    p = os.path.join(OUT, "og.svg")
    open(p, "w", encoding="utf-8").write(placeholder(99, "The GateKeeper", "steel art", hero=True))
    written.append(p)

    p = os.path.join(OUT, "favicon.svg")
    open(p, "w", encoding="utf-8").write(favicon())
    written.append(p)

    for w in written:
        print("wrote", os.path.normpath(w))


if __name__ == "__main__":
    main()
