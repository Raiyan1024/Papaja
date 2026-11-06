"""Papaja catalogue artwork generator.

Draws each garment as a smooth vector flat-lay on a deep studio backdrop and
renders PNGs into assets/catalog/ with resvg.

    pip install resvg-py
    python3 tools/gen_catalog.py

Filenames are stable, so a real photograph saved over any PNG of the same name
replaces the illustration on the website with no code changes.
"""
import pathlib, resvg_py

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "catalog"
W, H = 800, 1120
CX = 400.0


# --------------------------------------------------------------- geometry
def smooth(points, closed=True, tension=1.0):
    """Catmull-Rom through points -> cubic bezier path data."""
    pts = list(points)
    if closed:
        pts = [pts[-1]] + pts + [pts[0], pts[1]]
    else:
        pts = [pts[0]] + pts + [pts[-1]]
    d = f"M{pts[1][0]:.1f} {pts[1][1]:.1f}"
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6 * tension, p1[1] + (p2[1] - p0[1]) / 6 * tension)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6 * tension, p2[1] - (p3[1] - p1[1]) / 6 * tension)
        d += f" C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + " Z"


def mirror(points, axis=CX):
    return [(2 * axis - x, y) for x, y in points]


def body_path(left_points):
    """Closed outline = left silhouette + mirrored right silhouette (reversed)."""
    return smooth(left_points + mirror(left_points)[::-1])


# --------------------------------------------------------------- palettes
def pal(fabric, dark, light):
    return dict(fabric=fabric, dark=dark, light=light)

NAVY   = pal("#33526f", "#1b2c40", "#4d7096")
CHAR   = pal("#4e555d", "#2b3037", "#737d88")
CAMEL  = pal("#a67d50", "#6d4d2e", "#c69c6b")
STONE  = pal("#96958e", "#615f5a", "#b6b5ad")
WHITE  = pal("#e9edf0", "#b4bec7", "#ffffff")
SKY    = pal("#8fa9c3", "#5c7691", "#b3c8dd")
FOREST = pal("#365441", "#1f3228", "#52735b")
WINE   = pal("#63303a", "#3d1b22", "#85454f")
SLATE  = pal("#414b58", "#252d37", "#5d6a7a")
SAND   = pal("#b8a88d", "#87795f", "#d5c8b0")
BLACK  = pal("#2a2c30", "#151619", "#42464b")
GREY   = pal("#7d8a96", "#535e68", "#9dabb6")
CHAMB  = pal("#7f9dc0", "#4f6a8a", "#a3bcd8")
OLIVE  = pal("#5e6250", "#3b3f31", "#7c8169")


# --------------------------------------------------------------- scaffolding
def head(defs):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>
<radialGradient id="bg" cx="50%" cy="34%" r="78%">
  <stop offset="0" stop-color="#26374a"/><stop offset="50%" stop-color="#15212c"/><stop offset="100%" stop-color="#0a1017"/>
</radialGradient>
<radialGradient id="floor" cx="50%" cy="50%" r="50%">
  <stop offset="0" stop-color="#000000" stop-opacity=".5"/><stop offset="1" stop-color="#000000" stop-opacity="0"/>
</radialGradient>
<linearGradient id="gloss" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#ffffff" stop-opacity=".14"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
</linearGradient>
{defs}
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<ellipse cx="400" cy="986" rx="290" ry="54" fill="url(#floor)"/>
'''


def g(key, p, horiz=False):
    if horiz:
        return (f'<linearGradient id="{key}" x1="0" y1="0" x2="1" y2="0.1">'
                f'<stop offset="0" stop-color="{p["dark"]}"/>'
                f'<stop offset=".42" stop-color="{p["fabric"]}"/>'
                f'<stop offset="1" stop-color="{p["dark"]}"/></linearGradient>')
    return (f'<linearGradient id="{key}" x1=".12" y1="0" x2=".88" y2="1">'
            f'<stop offset="0" stop-color="{p["light"]}"/>'
            f'<stop offset=".38" stop-color="{p["fabric"]}"/>'
            f'<stop offset="1" stop-color="{p["dark"]}"/></linearGradient>')


def stroke(p, op=".12"):
    return f'stroke="{p["light"]}" stroke-opacity="{op}" stroke-width="1.8" stroke-linejoin="round"'


# --------------------------------------------------------------- jacket
JACKET_HEM = 700.0


def jacket(p, peak=False, two_button=False):
    """Torso + two sleeves drawn as overlapping shapes so there are no seams."""
    D = g("jf", p) + g("js", p, True) + g("jl", p)
    s = []
    sleeve = [(298, 216), (262, 230), (232, 274), (215, 360), (201, 470),
              (193, 582), (189, 660), (191, 702), (201, 728), (219, 734),
              (233, 726), (239, 688), (243, 620), (257, 520), (273, 420),
              (285, 320), (293, 252)]
    s.append(f'<path d="{smooth(sleeve)}" fill="url(#js)" {stroke(p,".07")}/>')
    s.append(f'<path d="{smooth(mirror(sleeve))}" fill="url(#js)" {stroke(p,".07")}/>')
    # cuff seams
    s.append('<path d="M191 700 C204 712 220 712 234 704" stroke="#000" stroke-opacity=".35" stroke-width="4" fill="none"/>')
    s.append('<path d="M609 700 C596 712 580 712 566 704" stroke="#000" stroke-opacity=".35" stroke-width="4" fill="none"/>')
    # torso
    torso = [(286, 244), (318, 216), (356, 202), (444, 202), (482, 216),
             (514, 244), (517, 330), (511, 414), (507, 496), (509, 590),
             (513, 716), (511, JACKET_HEM), (289, JACKET_HEM), (287, 716),
             (291, 590), (293, 496), (289, 414), (283, 330)]
    s.append(f'<path d="{smooth(torso)}" fill="url(#jf)" {stroke(p,".12")}/>')
    # shoulder sheen
    s.append(f'<path d="{smooth([(286,244),(318,216),(356,202),(352,244),(330,300),(300,330),(288,276)], closed=True)}" fill="url(#gloss)"/>')
    # shirt + tie inside the opening
    s.append('<path d="M362 202 L400 302 L438 202 L432 320 L400 640 L368 320 Z" fill="#d9e1e8"/>')
    s.append('<path d="M400 294 L400 612" stroke="#b0bcc7" stroke-width="2"/>')
    s.append('<path d="M400 308 L388 338 L400 562 L412 338 Z" fill="#1b2532"/>')
    # lapel bands following the V
    if peak:
        outer = [(352, 206), (310, 300), (372, 556), (400, 604)]
        inner = [(400, 604), (386, 548), (362, 300), (366, 204)]
    else:
        outer = [(356, 210), (322, 322), (374, 552), (400, 598)]
        inner = [(400, 598), (388, 546), (372, 322), (368, 208)]
    lap = [(352, 206), (310, 300), (372, 556), (400, 604), (386, 548), (362, 300), (366, 204)]
    s.append(f'<path d="{smooth(lap)}" fill="url(#jl)" {stroke(p,".18")}/>')
    s.append(f'<path d="{smooth(mirror(lap))}" fill="url(#jl)" {stroke(p,".18")}/>')
    # notch shadow
    s.append(f'<path d="{smooth([(352,206),(310,300),(344,270),(368,208)], closed=True)}" fill="{p["dark"]}" opacity=".4"/>')
    s.append(f'<path d="{smooth(mirror([(352,206),(310,300),(344,270),(368,208)]), closed=True)}" fill="{p["dark"]}" opacity=".4"/>')
    # collar stand
    s.append(f'<path d="M356 208 C376 232 424 232 444 208 L450 196 C420 214 380 214 350 196 Z" fill="{p["dark"]}" opacity=".95"/>')
    # pockets
    s.append('<path d="M314 676 C346 682 372 712 386 712 M414 712 C428 682 454 676 486 670" stroke="#000" stroke-opacity=".32" stroke-width="9" stroke-linecap="round" fill="none"/>')
    # closure + buttons
    for y in ([560, 612] if two_button else [566]):
        s.append(f'<circle cx="412" cy="{y}" r="9" fill="{p["dark"]}" stroke="{p["light"]}" stroke-opacity=".3"/>')
    s.append(f'<path d="M400 580 L400 {JACKET_HEM}" stroke="#000" stroke-opacity=".22" stroke-width="2.5"/>')
    s.append(f'<path d="M289 {JACKET_HEM} L511 {JACKET_HEM} L511 {JACKET_HEM+14} C450 {JACKET_HEM+26} 350 {JACKET_HEM+26} 289 {JACKET_HEM+14} Z" fill="#000" opacity=".3"/>')
    return D, "".join(s)


# --------------------------------------------------------------- shirt
SHIRT_HEM = 672.0


def shirt(p):
    D = g("sf", p) + g("ss", p, True)
    s = []
    sleeve = [(300, 224), (266, 238), (238, 280), (222, 364), (208, 466),
              (200, 566), (197, 626), (199, 664), (209, 688), (226, 694),
              (240, 686), (246, 650), (250, 590), (262, 500), (276, 410),
              (288, 318), (296, 258)]
    s.append(f'<path d="{smooth(sleeve)}" fill="url(#ss)" {stroke(p,".07")}/>')
    s.append(f'<path d="{smooth(mirror(sleeve))}" fill="url(#ss)" {stroke(p,".07")}/>')
    # cuffs
    s.append(f'<path d="M197 662 C210 674 226 674 240 666 L239 694 L199 690 Z" fill="{p["dark"]}" opacity=".45"/>')
    s.append(f'<path d="M603 662 C590 674 574 674 560 666 L561 694 L601 690 Z" fill="{p["dark"]}" opacity=".45"/>')
    # torso
    torso = [(294, 250), (324, 224), (360, 210), (440, 210), (476, 224),
             (506, 250), (509, 330), (505, 410), (503, 492), (504, 520),
             (508, 560), (506, SHIRT_HEM), (294, SHIRT_HEM), (292, 560),
             (296, 520), (297, 492), (295, 410), (291, 330)]
    s.append(f'<path d="{smooth(torso)}" fill="url(#sf)" {stroke(p,".12")}/>')
    # shoulder sheen
    s.append(f'<path d="{smooth([(294,250),(324,224),(360,210),(356,250),(332,300),(304,326),(294,282)], closed=True)}" fill="url(#gloss)" opacity=".8"/>')
    # collar: stand + two pointed leaves
    s.append(f'<path d="M352 216 C374 246 426 246 448 216 L456 206 C420 232 380 232 344 206 Z" fill="{p["dark"]}" opacity=".95"/>')
    s.append(f'<path d="M352 218 L400 300 L396 356 L336 272 Z" fill="{p["light"]}" opacity=".9" {stroke(p,".3")}/>')
    s.append(f'<path d="M448 218 L400 300 L404 356 L464 272 Z" fill="{p["fabric"]}" {stroke(p,".3")}/>')
    s.append('<path d="M400 300 L396 356 L404 356 Z" fill="#5d6a78" opacity=".55"/>')
    s.append(f'<path d="M400 300 L400 {SHIRT_HEM}" stroke="{p["dark"]}" stroke-opacity=".28" stroke-width="30"/>')
    s.append(f'<path d="M388 300 L388 {SHIRT_HEM}" stroke="{p["light"]}" stroke-opacity=".3" stroke-width="1.5"/>')
    for y in range(336, 664, 58):
        s.append(f'<circle cx="400" cy="{y}" r="6" fill="{p["dark"]}" opacity=".75"/>')
    s.append(f'<path d="M316 424 L372 424 L372 490 L342 506 L316 490 Z" fill="none" stroke="{p["dark"]}" stroke-opacity=".6" stroke-width="2.5"/>')
    s.append(f'<path d="M294 {SHIRT_HEM} L506 {SHIRT_HEM} L506 {SHIRT_HEM+14} C450 {SHIRT_HEM+27} 350 {SHIRT_HEM+27} 294 {SHIRT_HEM+14} Z" fill="#000" opacity=".28"/>')
    return D, "".join(s)


# --------------------------------------------------------------- trousers
def trousers(p):
    D = g("tf", p)
    s = []
    outline = smooth([(312, 148), (330, 140), (470, 140), (488, 148),
                      (492, 210), (494, 300), (494, 420), (492, 600),
                      (490, 780), (488, 900), (486, 940),
                      (416, 940), (410, 760), (400, 452),
                      (390, 760), (384, 940), (314, 940),
                      (312, 900), (310, 780), (308, 600), (306, 420),
                      (306, 300), (308, 210)])
    s.append(f'<path d="{outline}" fill="url(#tf)" {stroke(p)}/>')
    # waistband
    s.append(f'<path d="M308 152 L492 152 L493 222 L307 222 Z" fill="{p["dark"]}" opacity=".5"/>')
    s.append(f'<path d="M306 222 L494 222" stroke="{p["dark"]}" stroke-opacity=".85" stroke-width="3"/>')
    s.append(f'<path d="M348 152 L348 222 M452 152 L452 222" stroke="{p["dark"]}" stroke-opacity=".7" stroke-width="8"/>')
    # fly
    s.append(f'<path d="M400 226 L400 430" stroke="{p["dark"]}" stroke-opacity=".55" stroke-width="3"/>')
    s.append(f'<path d="M400 226 C380 280 378 340 384 398" stroke="{p["dark"]}" stroke-opacity=".4" stroke-width="2.5" fill="none"/>')
    # creases
    s.append(f'<path d="M352 232 C348 460 340 700 332 932" stroke="{p["light"]}" stroke-opacity=".2" stroke-width="5" fill="none"/>')
    s.append(f'<path d="M448 232 C452 460 460 700 468 932" stroke="{p["light"]}" stroke-opacity=".2" stroke-width="5" fill="none"/>')
    # pockets
    s.append(f'<path d="M308 246 C326 278 336 302 344 328 M492 246 C474 278 464 302 456 328" stroke="{p["dark"]}" stroke-opacity=".5" stroke-width="3" fill="none"/>')
    # inner-leg shading
    s.append('<path d="M384 540 L384 940 L400 940 L400 540 Z" fill="#000" opacity=".16"/>')
    s.append('<path d="M416 540 L416 940 L400 940 L400 540 Z" fill="#000" opacity=".08"/>')
    # turn-ups
    s.append(f'<path d="M312 898 L384 898 L384 940 L312 940 Z M416 898 L488 898 L488 940 L416 940 Z" fill="{p["dark"]}" opacity=".26"/>')
    return D, "".join(s)


# --------------------------------------------------------------- suit
def suit(p, peak=True):
    """Jacket on the left, matching trousers on the right."""
    dj, sj = jacket(p, peak=peak)
    dt, st = trousers(p)
    body = (f'<g transform="translate(-12,194) scale(0.78)">{sj}</g>'
            f'<g transform="translate(370,236) scale(0.60)">{st}</g>')
    return dj + dt, body


def compose(p, kind, **kw):
    if kind == "jacket":
        D, S = jacket(p, **kw)
        S = ('<path d="M362 196 L400 268 L438 196 L430 300 L400 646 L370 300 Z" fill="#dbe3ea"/>'
             '<path d="M400 276 L387 306 L400 552 L413 306 Z" fill="#1a2431"/>') + S
    elif kind == "shirt":
        D, S = shirt(p, **kw)
    elif kind == "trousers":
        D, S = trousers(p, **kw)
    else:
        D, S = suit(p, **kw)
    return head(D) + S + "</svg>"


if __name__ == "__main__":
    import json
    OUT.mkdir(parents=True, exist_ok=True)
    items = json.loads((ROOT / "tools" / "catalog.json").read_text())
    pals = {k: v for k, v in globals().items() if isinstance(v, dict) and k.isupper()}
    for it in items:
        svg = compose(pals[it["pal"]], it["art"], **it.get("opt", {}))
        (OUT / f"{it['file']}.png").write_bytes(bytes(resvg_py.svg_to_bytes(svg_string=svg)))
    print(f"rendered {len(items)} catalogue images into {OUT}")
