# -*- coding: utf-8 -*-
"""
Bronze Age Furniture — SVG art generator.

Each piece is drawn in real millimetres, origin at floor-centre, y negative
upwards. A wrapper transform scales it into whatever frame we need, so the
same drawing serves a 4:5 card and a 21:9 hero band.

These are placeholders with intent: line-drawn elevations that show the
joinery. Swap them for photography by replacing the <svg> with an <img>
inside the same .artframe element.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "img")
os.makedirs(OUT, exist_ok=True)

# --- palette ---------------------------------------------------------------
TOP   = "#E7CCA6"   # upward-facing surfaces (catching light)
FRONT = "#D9B78D"   # front faces
SIDE  = "#C29B6E"   # receding faces
DARK  = "#A87F53"   # deep shadow / far members
EDGE  = "#96703F"   # outline
SMK_F = "#8A6743"   # smoked oak front
SMK_S = "#6C4E32"   # smoked oak side
SMK_D = "#553D26"
LINEN = "#3B3835"
LINEN_L = "#4A4642"
CREAM = "#F2EDE2"
GLASS = "#CFE0DC"
CAVITY = "#E4D5BA"


def n(v):
    return ("%.1f" % v).rstrip("0").rstrip(".")


def rect(x, y, w, h, fill, stroke=EDGE, sw=1.6, extra=""):
    return ('<rect x="%s" y="%s" width="%s" height="%s" fill="%s" '
            'stroke="%s" stroke-width="%s" %s/>'
            % (n(x), n(y), n(w), n(h), fill, stroke, n(sw), extra))


def poly(points, fill, stroke=EDGE, sw=1.6):
    pts = " ".join("%s,%s" % (n(p[0]), n(p[1])) for p in points)
    return ('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="round"/>' % (pts, fill, stroke, n(sw)))


def ellipse(cx, cy, rx, ry, fill, stroke=EDGE, sw=1.6):
    return ('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" stroke="%s" '
            'stroke-width="%s"/>' % (n(cx), n(cy), n(rx), n(ry), fill, stroke, n(sw)))


def line(x1, y1, x2, y2, stroke=EDGE, sw=1.4, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s '
            'stroke-linecap="round"/>' % (n(x1), n(y1), n(x2), n(y2), stroke, n(sw), d))


def contact_shadow(halfwidth, ry=None):
    ry = ry or max(14, halfwidth * 0.085)
    return ('<ellipse cx="0" cy="6" rx="%s" ry="%s" fill="url(#g-shadow)" />'
            % (n(halfwidth * 1.02), n(ry)))


def cylinder(cx, top_y, bot_y, r, ry=None, front=FRONT, top=TOP):
    """Vertical oak column with an elliptical cap."""
    ry = ry or r * 0.26
    s = []
    s.append(ellipse(cx, bot_y, r, ry, front))
    s.append(rect(cx - r, top_y, r * 2, bot_y - top_y, front, stroke="none"))
    s.append(line(cx - r, top_y, cx - r, bot_y))
    s.append(line(cx + r, top_y, cx + r, bot_y))
    s.append(ellipse(cx, top_y, r, ry, top))
    # soft inner shading
    s.append('<rect x="%s" y="%s" width="%s" height="%s" fill="url(#g-cyl)" '
             'opacity="0.5"/>' % (n(cx - r), n(top_y), n(r * 2), n(bot_y - top_y)))
    return "".join(s)


# ===========================================================================
#  Pieces — each returns (svg_body, nominal_width, nominal_height)
# ===========================================================================

def art_round_table():
    s = [contact_shadow(360)]
    # back posts (recede, so their feet sit higher)
    for x in (-300, 210):
        s.append(rect(x, -700, 90, 620, SIDE))
    # stepped halving cross — the signature of the base
    s.append(rect(-230, -420, 240, 46, SIDE))          # upper rail, left half
    s.append(rect(-24, -420, 48, 168, DARK))           # the step
    s.append(rect(-10, -298, 240, 46, SIDE))           # lower rail, right half
    # front posts
    for x in (-330, 240):
        s.append(rect(x, -700, 90, 700, FRONT))
        s.append(line(x + 90, -700, x + 90, 0, EDGE, 1.1))
    # top slab
    s.append(ellipse(0, -700, 700, 112, SIDE))
    s.append(rect(-700, -740, 1400, 40, SIDE, stroke="none"))
    s.append(ellipse(0, -740, 700, 112, TOP))
    s.append(line(-700, -740, -700, -700))
    s.append(line(700, -740, 700, -700))
    # grain
    for i in range(1, 5):
        s.append('<ellipse cx="0" cy="-740" rx="%s" ry="%s" fill="none" '
                 'stroke="%s" stroke-width="1" opacity="0.16"/>'
                 % (n(700 - i * 118), n(112 - i * 18), EDGE))
    return "".join(s), 1400, 852


def art_trestle_table():
    s = [contact_shadow(820)]
    # far trestle hinted behind
    for x in (-830, 700):
        s.append(rect(x, -690, 130, 690, DARK))
    # through stretcher with wedges outside the posts
    s.append(rect(-940, -320, 1880, 62, SIDE))
    for x in (-946, 856):
        s.append(poly([(x, -336), (x + 90, -312), (x + 90, -266), (x, -242)], SMK_S))
    # near posts
    for x in (-790, 700):
        s.append(rect(x, -700, 90, 700, FRONT))
    # angled brackets under the top
    s.append(poly([(-700, -700), (-700, -610), (-610, -700)], SIDE))
    s.append(poly([(790, -700), (790, -610), (700, -700)], SIDE))
    # top
    s.append(rect(-1200, -700, 2400, 24, SIDE, stroke="none"))
    s.append(rect(-1200, -740, 2400, 40, TOP))
    for i in range(1, 6):
        s.append(line(-1160, -732 + i * 1.2, 1160, -732 + i * 1.2, EDGE, 0.8))
    return "".join(s), 2400, 760


def art_plank_table():
    s = [contact_shadow(720)]
    # housed rail between the slab legs
    s.append(rect(-740, -540, 1480, 90, DARK))
    # slab legs
    for x in (-880, 700):
        s.append(rect(x, -695, 180, 695, FRONT))
        s.append(rect(x + 180, -695, 26, 695, SIDE))
    # top slab
    s.append(rect(-1000, -695, 2000, 20, SIDE, stroke="none"))
    s.append(rect(-1000, -740, 2000, 45, TOP))
    for i in range(1, 4):
        s.append(line(-960, -736 + i * 2, 960, -736 + i * 2, EDGE, 0.7))
    return "".join(s), 2000, 760


def art_trestle_console():
    s = [contact_shadow(520)]
    for sgn in (-1, 1):
        cx = 480 * sgn
        s.append(poly([(cx - 150, 0), (cx - 105, 0), (cx - 18, -728), (cx - 58, -728)], FRONT))
        s.append(poly([(cx + 105, 0), (cx + 150, 0), (cx + 58, -728), (cx + 18, -728)], SIDE))
        s.append(rect(cx - 118, -250, 236, 34, SIDE))
    s.append(rect(-470, -200, 940, 30, DARK))
    s.append(rect(-700, -728, 1400, 12, SIDE, stroke="none"))
    s.append(rect(-700, -760, 1400, 32, TOP))
    return "".join(s), 1400, 780


def art_column_side_table():
    s = [contact_shadow(250)]
    s.append(cylinder(0, -470, -40, 45, front=SIDE, top=SIDE))       # rear column
    s.append(ellipse(0, -470, 250, 44, SIDE))
    s.append(rect(-250, -500, 500, 30, SIDE, stroke="none"))
    s.append(ellipse(0, -500, 250, 44, TOP))
    s.append(line(-250, -500, -250, -470))
    s.append(line(250, -500, 250, -470))
    s.append(cylinder(-125, -470, 0, 45))
    s.append(cylinder(125, -470, 0, 45))
    s.append('<ellipse cx="0" cy="-500" rx="170" ry="30" fill="none" stroke="%s" '
             'stroke-width="1" opacity="0.18"/>' % EDGE)
    return "".join(s), 500, 545


def art_glass_coffee_table():
    s = [contact_shadow(500)]
    s.append(cylinder(0, -368, -44, 80, front=SIDE, top=SIDE))
    s.append(cylinder(-235, -368, 0, 80))
    s.append(cylinder(235, -368, 0, 80))
    s.append('<ellipse cx="0" cy="-380" rx="500" ry="92" fill="%s" opacity="0.34" '
             'stroke="%s" stroke-width="2.2"/>' % (GLASS, "#8FB3AC"))
    s.append('<ellipse cx="0" cy="-392" rx="500" ry="92" fill="#FFFFFF" opacity="0.30" '
             'stroke="#A8C6C0" stroke-width="1.6"/>')
    s.append('<path d="M -330 -430 Q -120 -462 140 -444" fill="none" stroke="#FFFFFF" '
             'stroke-width="6" opacity="0.55" stroke-linecap="round"/>')
    return "".join(s), 1000, 500


def art_dining_chair():
    s = [contact_shadow(230)]
    # rear legs / stiles carry through to the back rail
    for x in (-182, 150):
        s.append(rect(x, -800, 32, 760, SIDE))
    # back rail with tenon ends showing outside the stiles
    s.append(rect(-214, -800, 428, 30, DARK))
    for x in (-214, 184):
        s.append(rect(x, -806, 30, 42, SMK_S))
    s.append(rect(-176, -770, 20, 300, SIDE))
    s.append(rect(156, -770, 20, 300, SIDE))
    # front legs
    for x in (-222, 190):
        s.append(rect(x, -470, 32, 470, FRONT))
    # stretchers
    s.append(rect(-200, -170, 400, 22, SIDE))
    s.append(rect(-200, -230, 400, 20, DARK))
    # seat
    s.append(ellipse(0, -450, 200, 40, SIDE))
    s.append(rect(-200, -472, 400, 22, SIDE, stroke="none"))
    s.append(ellipse(0, -472, 200, 40, TOP))
    return "".join(s), 480, 830


def art_armchair():
    s = [contact_shadow(310)]
    # rear stiles
    for x in (-208, 174):
        s.append(rect(x, -720, 34, 720, SIDE))
    s.append(rect(-242, -720, 484, 74, FRONT))            # wide shaped back rail
    s.append(rect(-236, -498, 472, 40, DARK))             # rear stretcher, low
    # arms bridging back stiles to front posts
    for x in (-286, 172):
        s.append(rect(x, -640, 114, 26, TOP))
    # front posts, continuous with the arms above
    for x in (-286, 252):
        s.append(rect(x, -640, 34, 640, FRONT))
    # floating seat panel in its grooved frame
    s.append(rect(-252, -444, 504, 22, SIDE))
    s.append(rect(-240, -422, 480, 20, TOP))
    # offset stretchers — mortises never meet inside the leg
    s.append(rect(-252, -186, 504, 22, SIDE))
    s.append(rect(-236, -236, 472, 18, DARK))
    return "".join(s), 620, 740


def art_folded_bench():
    """Three planes creased twice — the grain appears to turn each corner."""
    s = [contact_shadow(560)]
    # back plane, leaning
    s.append(poly([(-520, -700), (560, -655), (560, -372), (-520, -415)], FRONT))
    # seat plane — the first crease
    s.append(poly([(-520, -415), (560, -372), (620, -318), (-462, -358)], TOP))
    # front plane running to the floor — the second crease
    s.append(poly([(-462, -358), (620, -318), (620, 0), (-462, 0)], SIDE))
    # mitre lines: where grain turns the corner
    s.append(line(-520, -415, 560, -372, EDGE, 1.2))
    s.append(line(-462, -358, 620, -318, EDGE, 1.2))
    for i in range(1, 4):
        s.append(line(-440 + i * 8, -340, 600, -300 + i * 2, EDGE, 0.7))
    return "".join(s), 1140, 700


def art_angled_bench():
    s = [contact_shadow(600)]
    for sgn in (-1, 1):
        s.append(poly([(sgn * 560, 0), (sgn * 448, 0), (sgn * 372, -402),
                       (sgn * 476, -402)], FRONT if sgn > 0 else SIDE))
    s.append(rect(-700, -402, 1400, 12, SIDE, stroke="none"))
    s.append(rect(-700, -442, 1400, 40, TOP))
    return "".join(s), 1400, 460


def art_sofa():
    s = [contact_shadow(1000)]
    for sgn in (-1, 1):                                    # splayed legs
        s.append(poly([(sgn * 880, -330), (sgn * 950, -330), (sgn * 1010, 0),
                       (sgn * 946, 0)], SMK_S))
    s.append(poly([(-40, -330), (40, -330), (52, 0), (-52, 0)], SMK_D))
    s.append(rect(-1050, -440, 2100, 110, SMK_F))          # base rail
    # cushions — two back, two seat, with a legible gap between each pair
    for x in (-980, 16):
        s.append('<rect x="%s" y="-706" width="964" height="176" rx="30" fill="%s" '
                 'stroke="none"/>' % (n(x), LINEN_L))
        s.append('<path d="M %s -690 q 480 -22 940 0" fill="none" stroke="#5C5852" '
                 'stroke-width="5" opacity="0.65"/>' % n(x + 12))
    for x in (-980, 16):
        s.append('<rect x="%s" y="-548" width="964" height="128" rx="24" fill="%s" '
                 'stroke="none"/>' % (n(x), LINEN))
        s.append('<path d="M %s -536 q 480 -16 940 0" fill="none" stroke="#514D48" '
                 'stroke-width="4" opacity="0.6"/>' % n(x + 12))
    # oak side panels sit in front of the cushions — the frame is the furniture
    for x in (-1050, 966):
        s.append(rect(x, -730, 84, 366, SMK_F))
        s.append(rect(x + 84 if x < 0 else x - 18, -730, 18, 366, SMK_S))
    return "".join(s), 2100, 750


def art_bed():
    s = [contact_shadow(1020)]
    s.append(rect(-880, -800, 1760, 320, FRONT))          # headboard panel
    s.append(line(-880, -742, 880, -742, EDGE, 1))
    s.append('<rect x="-950" y="-540" width="1900" height="190" rx="18" fill="%s" '
             'stroke="%s" stroke-width="1.4"/>' % (CREAM, "#D8D0C0"))
    s.append('<path d="M -930 -498 Q -600 -540 -200 -502 T 500 -500 T 930 -518" '
             'fill="none" stroke="#DCD4C4" stroke-width="6"/>')
    s.append('<path d="M -600 -430 q 300 -30 700 -6" fill="none" stroke="#E2DBCC" '
             'stroke-width="5"/>')
    s.append(rect(-990, -350, 1980, 180, FRONT))          # side rail
    for x in (-1040, 990):                                 # posts + tenon ends
        s.append(rect(x, -400, 50, 400, SIDE))
        s.append(rect(x - 6, -330, 62, 44, DARK))
    s.append(line(-990, -290, 990, -290, EDGE, 1))
    return "".join(s), 2130, 810


def art_cube():
    s = [contact_shadow(215)]
    s.append(poly([(200, -450), (268, -486), (268, -36), (200, 0)], SIDE))
    s.append(poly([(-200, -450), (-132, -486), (268, -486), (200, -450)], TOP))
    s.append(rect(-200, -450, 400, 450, FRONT))
    s.append(rect(-176, -426, 352, 402, CAVITY))
    s.append('<rect x="-176" y="-426" width="352" height="402" fill="url(#g-cavity)"/>')
    for i in range(4):                                     # dovetail hints
        s.append(line(-200 + 12 + i * 100, -450, -200 + 12 + i * 100, -426, EDGE, 1))
    return "".join(s), 470, 500


def art_plank_stool():
    s = [contact_shadow(215)]
    s.append(poly([(-30, -405), (30, -405), (22, -40), (-22, -40)], SIDE))
    for sgn in (-1, 1):
        s.append(poly([(sgn * 130, -405), (sgn * 172, -405), (sgn * 205, 0),
                       (sgn * 160, 0)], FRONT))
    s.append(rect(-210, -405, 420, 14, SIDE, stroke="none"))
    s.append(rect(-210, -450, 420, 45, TOP))
    for x in (-151, 151):                                  # wedge lines in the seat
        s.append(line(x, -448, x, -407, EDGE, 2.2))
    return "".join(s), 440, 470


PIECES = {
    "round-table": art_round_table,
    "trestle-table": art_trestle_table,
    "plank-table": art_plank_table,
    "trestle-console": art_trestle_console,
    "column-side-table": art_column_side_table,
    "glass-coffee-table": art_glass_coffee_table,
    "dining-chair": art_dining_chair,
    "armchair": art_armchair,
    "folded-bench": art_folded_bench,
    "angled-bench": art_angled_bench,
    "sofa": art_sofa,
    "bed": art_bed,
    "cube": art_cube,
    "plank-stool": art_plank_stool,
}


# ===========================================================================
#  Frame assembly
# ===========================================================================
DEFS = """
<defs>
  <linearGradient id="g-wall" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#FCFAF6"/>
    <stop offset="1" stop-color="#F0EBE0"/>
  </linearGradient>
  <linearGradient id="g-floor" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#EFE9DC"/>
    <stop offset="1" stop-color="#E4DCCB"/>
  </linearGradient>
  <linearGradient id="g-cyl" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#000000" stop-opacity="0.13"/>
    <stop offset="0.32" stop-color="#FFFFFF" stop-opacity="0.30"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0.16"/>
  </linearGradient>
  <linearGradient id="g-cavity" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#7A5B38" stop-opacity="0.22"/>
    <stop offset="1" stop-color="#7A5B38" stop-opacity="0.03"/>
  </linearGradient>
  <radialGradient id="g-shadow">
    <stop offset="0" stop-color="#3A2E22" stop-opacity="0.20"/>
    <stop offset="1" stop-color="#3A2E22" stop-opacity="0"/>
  </radialGradient>
</defs>
"""


def frame(body, w, h, floor_y):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
        'width="%d" height="%d" role="img" preserveAspectRatio="xMidYMid slice">'
        '%s'
        '<rect width="%d" height="%d" fill="url(#g-wall)"/>'
        '<rect y="%s" width="%d" height="%s" fill="url(#g-floor)"/>'
        '<line x1="0" y1="%s" x2="%d" y2="%s" stroke="#D8CFBD" stroke-width="1.5"/>'
        '%s</svg>'
        % (w, h, w, h, DEFS, w, h, n(floor_y), w, n(h - floor_y),
           n(floor_y), w, n(floor_y), body)
    )


def render(key, w, h, fill_w=0.78, fill_h=0.68, floor_ratio=0.80, lift=0.0, title=""):
    body, nw, nh = PIECES[key]()
    floor_y = h * floor_ratio
    scale = min(w * fill_w / nw, h * fill_h / nh)
    g = ('<g transform="translate(%s,%s) scale(%s)">%s</g>'
         % (n(w / 2.0), n(floor_y - lift), n(scale), body))
    svg = frame(g, w, h, floor_y)
    if title:
        svg = svg.replace('role="img">', 'role="img" aria-label="%s">' % title, 1)
    return svg


def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    return path


# ===========================================================================
#  Joinery diagrams (craft page)
# ===========================================================================
def diagram_frame(body, w=900, h=520):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
            'width="%d" height="%d" role="img">%s'
            '<rect width="%d" height="%d" fill="#FAF8F3"/>%s</svg>'
            % (w, h, w, h, DEFS, w, h, body))


def label(x, y, text, anchor="middle", size=13, fill="#8A8073"):
    return ('<text x="%s" y="%s" text-anchor="%s" font-family="Inter, Helvetica, Arial, sans-serif" '
            'font-size="%s" letter-spacing="1.6" fill="%s">%s</text>'
            % (n(x), n(y), anchor, size, fill, text))


def diagram_kigumi():
    s = []
    # two members meeting in a stepped halving lap, exploded then joined
    s.append(label(230, 60, "APART"))
    s.append(poly([(70, 130), (330, 130), (330, 190), (200, 190), (200, 230),
                   (70, 230)], FRONT))
    s.append(poly([(120, 300), (380, 300), (380, 400), (250, 400), (250, 340),
                   (120, 340)], SIDE))
    s.append(line(200, 200, 250, 296, EDGE, 1.2, "5 5"))
    s.append(label(680, 60, "TOGETHER"))
    s.append(poly([(520, 200), (830, 200), (830, 260), (700, 260), (700, 330),
                   (520, 330)], FRONT))
    s.append(poly([(700, 260), (830, 260), (830, 360), (700, 360)], SIDE))
    s.append(line(700, 200, 700, 360, EDGE, 1.4))
    s.append(line(520, 260, 830, 260, EDGE, 1.4))
    s.append(label(675, 430, "LOAD PATH RUNS THROUGH THE WOOD, NOT ACROSS A FASTENER",
                   "middle", 11))
    return diagram_frame("".join(s))


def diagram_kigoroshi():
    s = []
    steps = [
        (150, "1 — OVERSIZE", 0),
        (450, "2 — CRUSH", 1),
        (750, "3 — RECOVER", 2),
    ]
    for cx, text, i in steps:
        s.append(label(cx, 70, text))
        # mortise block
        s.append(rect(cx - 95, 120, 190, 150, SIDE))
        s.append(rect(cx - 42, 120, 84, 150, "#EFE7D8"))
        # tenon
        tw = [96, 80, 92][i]
        fill = [FRONT, DARK, FRONT][i]
        s.append(rect(cx - tw / 2.0, 300, tw, 150, fill))
        if i == 1:
            s.append(line(cx - 74, 320, cx - 96, 300, EDGE, 2))
            s.append(line(cx + 74, 320, cx + 96, 300, EDGE, 2))
            s.append(label(cx, 486, "HAMMER", "middle", 11, "#DC4527"))
        if i == 2:
            s.append('<path d="M %s 330 l -18 0 M %s 330 l 18 0" stroke="%s" '
                     'stroke-width="2"/>' % (n(cx - 46), n(cx + 46), "#DC4527"))
            s.append(label(cx, 486, "FIBRES SWELL BACK — LOCKED", "middle", 11, "#A5794A"))
        if i == 0:
            s.append(label(cx, 486, "TENON CUT 0.4 MM PROUD", "middle", 11))
        s.append(line(cx - 42, 120, cx - 42, 270, EDGE, 1.2, "4 4"))
        s.append(line(cx + 42, 120, cx + 42, 270, EDGE, 1.2, "4 4"))
    return diagram_frame("".join(s))


def diagram_kusabi():
    s = []
    s.append(label(230, 60, "SLIT TENON ENTERS"))
    s.append(rect(60, 140, 130, 230, SIDE))               # post
    s.append(rect(60, 210, 130, 90, "#EFE7D8"))            # mortise
    s.append(rect(190, 215, 210, 80, FRONT))               # tenon
    s.append(line(300, 222, 396, 222, EDGE, 2))            # slit
    s.append(line(300, 288, 396, 288, EDGE, 2))
    s.append(label(680, 60, "WEDGE FLARES IT"))
    s.append(rect(520, 140, 130, 230, SIDE))
    s.append(rect(520, 210, 130, 90, "#EFE7D8"))
    s.append(poly([(650, 215), (830, 200), (830, 310), (650, 295)], FRONT))
    s.append(poly([(790, 214), (830, 206), (830, 304), (790, 296)], DARK))
    s.append(label(810, 380, "WEDGE", "middle", 11, "#DC4527"))
    s.append(label(450, 468,
                   "THE TENON CANNOT WITHDRAW — IT IS NOW WIDER THAN THE HOLE IT CAME THROUGH",
                   "middle", 11))
    return diagram_frame("".join(s))


# ===========================================================================
if __name__ == "__main__":
    made = []

    # card art (4:5)
    for key in PIECES:
        made.append(write("%s.svg" % key, render(key, 800, 1000, 0.80, 0.66, 0.80)))

    # wide bands
    made.append(write("hero.svg", render("trestle-table", 2000, 900, 0.72, 0.70, 0.86)))
    made.append(write("band-craft.svg", render("round-table", 1600, 900, 0.68, 0.72, 0.86)))
    made.append(write("band-bed.svg", render("bed", 2000, 760, 0.74, 0.74, 0.88)))
    made.append(write("intro.svg", render("round-table", 1800, 900, 0.58, 0.58, 0.84)))
    made.append(write("about.svg", render("plank-table", 1400, 1000, 0.80, 0.60, 0.80)))

    # square art — used as the second frame on every product page
    for key in PIECES:
        made.append(write("%s-sq.svg" % key, render(key, 1000, 1000, 0.92, 0.80, 0.86)))

    # 3:2 art — the lead frame for wide pieces (tables, beds, sofas, benches)
    for key in PIECES:
        made.append(write("%s-wide.svg" % key, render(key, 1500, 1000, 0.84, 0.74, 0.86)))

    # diagrams
    made.append(write("diagram-kigumi.svg", diagram_kigumi()))
    made.append(write("diagram-kigoroshi.svg", diagram_kigoroshi()))
    made.append(write("diagram-kusabi.svg", diagram_kusabi()))

    print("wrote %d files" % len(made))
