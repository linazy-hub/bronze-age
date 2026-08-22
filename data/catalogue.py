# -*- coding: utf-8 -*-
"""Bronze Age Furniture — product catalogue.
Single source of truth for the shop grid, homepage features and product pages.
Prices are INR placeholders — edit freely.
"""

BRAND = {
    "name": "Bronze Age",
    "full": "Bronze Age Furniture",
    "domain": "bronzeagefurniture.in",
    "tagline": "Not a single screw.",
    "email": "hello@bronzeagefurniture.in",
    "phone": "+91 00000 00000",
    "city": "India",
}

# category slugs used by the shop filter
CATEGORIES = [
    ("all", "Everything"),
    ("tables", "Tables"),
    ("seating", "Seating"),
    ("beds", "Beds"),
    ("objects", "Small Objects"),
]

PRODUCTS = [
    {
        "slug": "maru-round-dining-table",
        "name": "Maru Round Dining Table",
        "category": "tables",
        "kind": "Dining table",
        "price": 168000,
        "art": "round-table",
        "lede": "A solid oak disc carried on four posts locked by a stepped halving cross. "
                "The base reads as a drawing — every line is a joint doing work.",
        "story": [
            "The Maru began as a question: how little structure can hold a 1400mm oak top "
            "flat for fifty years? The answer was not more material. It was better geometry.",
            "Four 90mm posts meet a pair of stepped rails that halve into each other at the "
            "centre. The step is not decorative. It transfers the top's load down through the "
            "long grain of each post rather than across the short grain of a fastener.",
            "The top is loose-laid on buttons that slide in a groove, so the oak breathes with "
            "the monsoon and shrinks back in February without ever splitting.",
        ],
        "joinery": [
            ("Kigumi", "Stepped halving lap at the base cross — the two rails interlock and "
                       "seat into the posts in one geometry, no adhesive needed to hold shape."),
            ("Kigoroshi", "Post tenons are cut 0.4mm oversize, the fibres crushed with a "
                          "shop hammer, then driven home. Ambient humidity swells them back "
                          "into the mortise walls and the joint tightens permanently."),
            ("Buttoned top", "Oak buttons in a sliding groove hold the top down while letting "
                             "it move up to 6mm across the grain seasonally."),
        ],
        "dims": [("Diameter", "1400 mm"), ("Height", "740 mm"),
                 ("Top thickness", "40 mm"), ("Post section", "90 × 90 mm"),
                 ("Seats", "5–6"), ("Weight", "48 kg approx.")],
        "material": "Solid European oak, quartersawn top",
        "finish": "Hardwax oil, matt — natural",
        "lead": "10–12 weeks",
    },
    {
        "slug": "nuki-dining-table",
        "name": "Nuki Dining Table",
        "category": "tables",
        "kind": "Dining table",
        "price": 224000,
        "art": "trestle-table",
        "lede": "A trestle table whose stretcher passes clean through both legs and is "
                "locked outside them with a tapered oak wedge you can knock out by hand.",
        "story": [
            "Nuki is the through-beam of a Japanese timber frame — the member that passes "
            "through a post and is wedged beyond it. The whole table is that one idea, at "
            "dining scale.",
            "Because the wedge sits proud on the outside face, the joint is legible. You can "
            "see the table holding itself together. You can also, ten years from now, tap the "
            "wedge out with a mallet, carry the table through a doorway in three pieces, and "
            "tap it back.",
            "The longer the table gets, the more the design earns its keep. At 2400mm there is "
            "no sag and no wobble, and still nothing in it that can rust.",
        ],
        "joinery": [
            ("Kusabi", "The through-tenon is slit at its end; a tapered wedge driven into the "
                       "slit flares the tenon beyond the mortise wall so it cannot withdraw."),
            ("Nuki through-tenon", "The stretcher passes fully through both leg frames, "
                                   "putting the whole span in compression against the legs."),
            ("Angled apron tenons", "Apron-to-leg joints run at a slight angle and are pinned "
                                    "with blind oak keys to kill lateral racking."),
        ],
        "dims": [("Length", "2400 mm"), ("Width", "900 mm"), ("Height", "740 mm"),
                 ("Top thickness", "40 mm"), ("Seats", "8"), ("Weight", "72 kg approx.")],
        "material": "Solid European oak",
        "finish": "Hardwax oil, matt — natural",
        "lead": "12–14 weeks",
        "featured": True,
    },
    {
        "slug": "ita-plank-table",
        "name": "Ita Plank Table",
        "category": "tables",
        "kind": "Dining table",
        "price": 196000,
        "art": "plank-table",
        "lede": "Two full-width oak slabs stand as legs; a third bridges them. Three planes, "
                "three joints, nothing else in the room.",
        "story": [
            "The Ita is the most reduced table we make. A slab top, two slab legs, and a "
            "single deep rail housed between them.",
            "Slab legs are unforgiving — a panel that wide will move, and a rigid connection "
            "will tear it apart within two seasons. So the rail is housed in a sliding dovetail "
            "that grips vertically and releases horizontally, letting each leg expand across "
            "its width without ever loosening its grip on the rail.",
            "It is the joint doing the thinking so the form doesn't have to.",
        ],
        "joinery": [
            ("Sliding dovetail", "The rail is tapered into a housed dovetail across each leg, "
                                 "drawn tight on assembly and free to move seasonally."),
            ("Kigoroshi", "Dovetail shoulders are compressed before assembly so the final "
                          "millimetre of fit is made by the wood recovering, not by force."),
            ("Draw-bored pins", "Oak pins offset by 1mm pull the shoulders permanently closed."),
        ],
        "dims": [("Length", "2000 mm"), ("Width", "900 mm"), ("Height", "740 mm"),
                 ("Slab thickness", "45 mm"), ("Seats", "6–8"), ("Weight", "86 kg approx.")],
        "material": "Solid European oak, wide-board",
        "finish": "Hardwax oil, matt — natural",
        "lead": "12–14 weeks",
    },
    {
        "slug": "uma-trestle-console",
        "name": "Uma Trestle Console",
        "category": "tables",
        "kind": "Console / desk",
        "price": 92000,
        "art": "trestle-console",
        "lede": "Two splayed A-frames under a narrow oak plane. Light enough to move alone, "
                "rigid enough to write on.",
        "story": [
            "Uma means horse — the sawhorse, the oldest structure in any workshop. We kept "
            "the honesty and refined the angles until it belonged in a hallway.",
            "Each trestle splays in two planes, so the frame resists racking from both the "
            "front and the side. The legs meet the head-beam in compound-angled tenons cut "
            "from a single setup on the tenoner.",
            "Works as a console against a wall, a desk in a window, or a narrow serving table.",
        ],
        "joinery": [
            ("Compound-angle tenons", "Legs meet the head-beam at a double bevel; the tenon "
                                      "shoulders are cut to match so the joint closes with no gap."),
            ("Kusabi", "The lower cross-rail is wedged through each trestle, tensioning the splay."),
            ("Knock-down top", "The top drops onto locating pins — no fixings, lifts off for moving."),
        ],
        "dims": [("Length", "1400 mm"), ("Depth", "400 mm"), ("Height", "760 mm"),
                 ("Top thickness", "32 mm"), ("Weight", "24 kg approx.")],
        "material": "Solid European oak",
        "finish": "Hardwax oil, matt — natural",
        "lead": "8–10 weeks",
    },
    {
        "slug": "hashira-side-table",
        "name": "Hashira Side Table",
        "category": "tables",
        "kind": "Side table",
        "price": 54000,
        "art": "column-side-table",
        "lede": "Three turned oak columns and a soft-edged disc. The columns are hollow-mortised "
                "into the top from beneath — the joint is felt, never seen.",
        "story": [
            "Hashira is the column, the structural post. Three of them is the minimum number "
            "that will stand level on any floor without shimming — a tripod cannot rock.",
            "Each column is turned from a solid block, then its head is cut to a round tenon "
            "that enters a bored mortise in the underside of the top. The fit is made by "
            "kigoroshi: the tenon is compressed, driven, and left to swell.",
            "Nothing enters the top face. There is no plug, no filler, no screw to bleed a "
            "dark ring into the oak over time.",
        ],
        "joinery": [
            ("Round tenon", "Each column head is a 45mm round tenon into a bored blind mortise."),
            ("Kigoroshi", "Tenon fibres are crushed to 44.6mm before driving, and recover "
                          "against the mortise wall to lock."),
            ("Splayed set-out", "Columns sit on a 120° triangle just inside the rim, so the "
                                "table cannot tip when leaned on at the edge."),
        ],
        "dims": [("Diameter", "500 mm"), ("Height", "500 mm"),
                 ("Top thickness", "30 mm"), ("Column diameter", "90 mm"),
                 ("Weight", "14 kg approx.")],
        "material": "Solid European oak",
        "finish": "Hardwax oil, matt — natural",
        "lead": "6–8 weeks",
        "featured": True,
    },
    {
        "slug": "hashira-glass-coffee-table",
        "name": "Hashira Glass Coffee Table",
        "category": "tables",
        "kind": "Coffee table",
        "price": 118000,
        "art": "glass-coffee-table",
        "lede": "Three oak columns carrying a 12mm float glass disc. The glass rests — it is "
                "not clamped, drilled or bonded.",
        "story": [
            "The problem with a glass top is that every conventional solution involves metal: "
            "a bracket, a bolt, a bonded steel pad. We removed all three.",
            "Each column is capped with a recessed oak seat and a soft cork gasket. The glass "
            "drops in and is held by its own weight and the lip of the seat. Lift it off with "
            "two hands to clean beneath it.",
            "Because the columns are free-standing under the glass, you can shift them to suit "
            "a sofa's line — the geometry tolerates a 40mm range in any direction.",
        ],
        "joinery": [
            ("Seated glass", "A shallow rebate turned into each column head captures the glass "
                             "edge; a cork gasket takes up any floor variation."),
            ("Laminated columns", "Columns are stave-built from eight oak segments with "
                                  "long-grain glue lines only, so they will not check."),
            ("No fixings", "Nothing mechanical touches the glass at any point."),
        ],
        "dims": [("Glass diameter", "1000 mm"), ("Glass thickness", "12 mm"),
                 ("Height", "380 mm"), ("Column diameter", "160 mm"),
                 ("Weight", "38 kg approx.")],
        "material": "Solid European oak, low-iron toughened glass",
        "finish": "Hardwax oil, matt — natural; polished glass edge",
        "lead": "10–12 weeks",
    },
    {
        "slug": "tsugi-dining-chair",
        "name": "Tsugi Dining Chair",
        "category": "seating",
        "kind": "Dining chair",
        "price": 46000,
        "art": "dining-chair",
        "lede": "A round seat between four uprights, with a back rail that passes through the "
                "stiles and shows its tenons on the outside.",
        "story": [
            "A chair is the hardest thing to build without metal. Every joint is loaded in a "
            "different direction each time somebody sits, leans back, or drags it in.",
            "The Tsugi answers with through-tenons where the loads are highest — seat rail to "
            "leg, and back rail to stile — each one pinned rather than glued alone. The exposed "
            "tenon ends on the back rail are the structure admitting what it is.",
            "It weighs 4.6kg. You can lift it with one finger under the seat.",
        ],
        "joinery": [
            ("Pinned through-tenon", "Back rail passes through both stiles and is pinned with "
                                     "riven oak dowel, visible on the outer face."),
            ("Blind keyed tenon", "Seat rails enter the legs on blind tenons locked by an "
                                  "internal oak key — invisible, and it will not creep."),
            ("Kigoroshi", "All chair tenons are compressed before assembly; a chair joint that "
                          "starts tight and swells will not develop the seasonal click."),
        ],
        "dims": [("Width", "480 mm"), ("Depth", "500 mm"), ("Height", "820 mm"),
                 ("Seat height", "450 mm"), ("Weight", "4.6 kg")],
        "material": "Solid European oak",
        "finish": "Hardwax oil, matt — natural",
        "lead": "8–10 weeks",
        "featured": True,
    },
    {
        "slug": "kake-armchair",
        "name": "Kake Armchair",
        "category": "seating",
        "kind": "Armchair",
        "price": 78000,
        "art": "armchair",
        "lede": "A low oak frame with a floating panel seat and a single wide back rail. "
                "Made to be sat in for an hour, not an evening.",
        "story": [
            "The Kake sits between a dining chair and a lounge chair — the chair at the end of "
            "a long table, or beside a window with a book.",
            "Its arms are continuous with the front legs, so the load path from armrest to "
            "floor never crosses a joint. The back rail is a single wide board tenoned into "
            "the rear stiles, shaped to meet the lumbar and nothing else.",
            "The seat panel floats in a groove on all four sides. It is not fixed anywhere.",
        ],
        "joinery": [
            ("Continuous arm-leg", "Arms and front legs are cut from one blank, eliminating "
                                   "the highest-stress joint in the chair entirely."),
            ("Floating seat panel", "Seat sits in a grooved frame with clearance on all sides "
                                    "for seasonal movement."),
            ("Twin stretcher", "Offset stretchers at differing heights so the mortises never "
                               "meet inside the leg and weaken it."),
        ],
        "dims": [("Width", "620 mm"), ("Depth", "560 mm"), ("Height", "720 mm"),
                 ("Seat height", "420 mm"), ("Weight", "8.2 kg")],
        "material": "Solid European oak",
        "finish": "Hardwax oil, matt — natural",
        "lead": "10–12 weeks",
    },
    {
        "slug": "ori-folded-bench",
        "name": "Ori Folded Bench",
        "category": "seating",
        "kind": "Bench / lounge",
        "price": 88000,
        "art": "folded-bench",
        "lede": "Three wide oak planes mitred into a single folded gesture. It reads as one "
                "piece of paper creased twice.",
        "story": [
            "Ori is to fold. The bench is an exercise in making three heavy boards behave like "
            "one continuous surface.",
            "Every corner is a long mitre reinforced with hidden loose tenons running the full "
            "width. You see an unbroken line of grain turning a corner; inside, there is 400mm "
            "of glue surface and eight oak splines taking the load.",
            "Low enough for a hallway, deep enough to actually sit in.",
        ],
        "joinery": [
            ("Long mitre", "Corners are mitred so grain appears to turn the corner unbroken."),
            ("Hidden loose tenon", "Full-width oak splines inside each mitre carry the load "
                                   "the mitre alone could not."),
            ("Panel-frame back", "The back plane is housed to allow the wide board to move "
                                 "without opening the mitre."),
        ],
        "dims": [("Width", "1200 mm"), ("Depth", "620 mm"), ("Height", "660 mm"),
                 ("Seat height", "380 mm"), ("Weight", "42 kg approx.")],
        "material": "Solid European oak, wide-board",
        "finish": "Hardwax oil, matt — smoked",
        "lead": "12–14 weeks",
    },
    {
        "slug": "watari-bench",
        "name": "Watari Bench",
        "category": "seating",
        "kind": "Bench",
        "price": 64000,
        "art": "angled-bench",
        "lede": "A plank seat on two canted slab legs. The lean is structural: it turns "
                "downward load into a joint that tightens.",
        "story": [
            "Watari — to cross over. The legs cant inward under the seat, so weight on the "
            "bench pushes each leg harder into its housing rather than levering it out.",
            "The housings are stopped dadoes cut across the underside of the seat, angled to "
            "match the lean exactly. Assembly is a hammer, a block, and no adhesive on the "
            "shoulders — the fit is mechanical.",
            "Pairs with the Nuki and Ita tables, or lives alone at the foot of a bed.",
        ],
        "joinery": [
            ("Angled housed dado", "Legs are housed into the seat underside at 8° so vertical "
                                   "load closes the joint."),
            ("Kigoroshi", "The housing shoulders are compressed and swell back tight."),
            ("Through-wedge option", "Available with wedged through-tenons exposed on the "
                                     "seat face on request."),
        ],
        "dims": [("Length", "1400 mm"), ("Depth", "360 mm"), ("Height", "440 mm"),
                 ("Seat thickness", "40 mm"), ("Weight", "22 kg approx.")],
        "material": "Solid European oak",
        "finish": "Hardwax oil, matt — natural",
        "lead": "8–10 weeks",
    },
    {
        "slug": "kura-sofa",
        "name": "Kura Sofa",
        "category": "seating",
        "kind": "Sofa",
        "price": 268000,
        "art": "sofa",
        "lede": "A smoked oak carcass on splayed legs, holding two deep linen cushions. "
                "The frame is the furniture; the cushions are removable.",
        "story": [
            "Most sofas are a steel and staple skeleton wearing fabric. The Kura inverts that: "
            "a visible oak carcass that would be worth having empty, with cushions set into it.",
            "The side panels are through-tenoned into the base rail and wedged from below, "
            "where the wedges are invisible in use but reachable with the sofa on its back.",
            "Cushion covers are washable and replaceable. When the linen has had its life, "
            "the frame is still at the beginning of its own.",
        ],
        "joinery": [
            ("Kusabi", "Side panels are through-tenoned into the base rail and wedged from "
                       "underneath — serviceable, never seen."),
            ("Splayed leg tenons", "Legs enter the base on compound-angle tenons; the splay "
                                   "widens the footprint without a metal bracket."),
            ("Webbed deck", "Cushion deck is jute-webbed onto an oak sub-frame, tensioned by "
                            "wedged rails rather than staples."),
        ],
        "dims": [("Length", "2100 mm"), ("Depth", "880 mm"), ("Height", "700 mm"),
                 ("Seat height", "420 mm"), ("Weight", "64 kg approx.")],
        "material": "Smoked European oak, washed linen upholstery",
        "finish": "Hardwax oil, matt — smoked; charcoal linen",
        "lead": "14–16 weeks",
        "featured": True,
    },
    {
        "slug": "nuki-platform-bed",
        "name": "Nuki Platform Bed",
        "category": "beds",
        "kind": "Bed",
        "price": 212000,
        "art": "bed",
        "lede": "A low oak platform whose side rails pass through the headboard posts and "
                "show their tenon ends. Sleep loads it tighter every night.",
        "story": [
            "A bed frame fails at the corner. Bolted frames loosen, the corner develops play, "
            "and the play becomes the creak everybody eventually accepts.",
            "The Nuki bed refuses the premise. Side rails pass through the posts and are "
            "wedged outside them. Downward load from the mattress and sleeper is carried on "
            "the bearing face of the through-mortise, which means the joint is being pressed "
            "closed by the very weight that would loosen a bolt.",
            "It arrives in five pieces and assembles with a rubber mallet in about fifteen "
            "minutes. No tools, no fixings, no allen key taped inside the packaging.",
        ],
        "joinery": [
            ("Nuki through-tenon", "Side rails pass fully through the head and foot posts, "
                                   "tenon ends visible on the outer face."),
            ("Kusabi", "Tapered wedges lock each through-tenon and can be re-driven in "
                       "twenty years if the oak ever settles."),
            ("Notched slat carrier", "Slats sit in notched cross-beams that lock into the "
                                     "rails — the deck stiffens the whole frame."),
        ],
        "dims": [("King", "1980 × 2030 mm overall"), ("Queen", "1780 × 2030 mm overall"),
                 ("Height", "320 mm"), ("Headboard height", "780 mm"),
                 ("Rail section", "180 × 40 mm"), ("Weight", "78 kg approx.")],
        "material": "Solid European oak",
        "finish": "Hardwax oil, matt — natural",
        "lead": "12–14 weeks",
        "featured": True,
    },
    {
        "slug": "hako-cube-table",
        "name": "Hako Cube Table",
        "category": "objects",
        "kind": "Side table / storage",
        "price": 38000,
        "art": "cube",
        "lede": "An open oak cube, dovetailed at every corner. Side table one way up, "
                "bookshelf the other.",
        "story": [
            "Hako is simply box. Four boards, four corners, and the oldest joint that has ever "
            "worked: the through dovetail.",
            "The corners are hand-cut and left proud by a hair, then pared flush after the glue "
            "has gone off, so the end grain reads as a series of fine lines rather than a seam.",
            "Turn it on its side and it holds books. Stack two and it holds more.",
        ],
        "joinery": [
            ("Through dovetail", "Every corner is a hand-cut through dovetail — the joint "
                                 "cannot pull apart in its principal direction."),
            ("Rebated back option", "Available with a housed oak back panel that floats in a "
                                    "groove."),
            ("Stackable", "Locating recesses in the top face register a second cube."),
        ],
        "dims": [("Width", "400 mm"), ("Depth", "400 mm"), ("Height", "450 mm"),
                 ("Board thickness", "24 mm"), ("Weight", "9 kg approx.")],
        "material": "Solid European oak",
        "finish": "Hardwax oil, matt — natural",
        "lead": "6–8 weeks",
    },
    {
        "slug": "fumi-stool",
        "name": "Fumi Stool",
        "category": "objects",
        "kind": "Stool",
        "price": 28000,
        "art": "plank-stool",
        "lede": "A thick oak plank on three splayed legs. The first thing we ever made and "
                "still the piece we judge the others against.",
        "story": [
            "Every workshop needs a stool. Ours became the test piece — if an apprentice can "
            "cut three compound-angle round tenons that all land flat on the floor, they can "
            "be trusted with a table.",
            "The legs splay outward on two axes. Getting them level is entirely a function of "
            "hand measurement and layout, which is exactly the skill the rest of the catalogue "
            "depends on.",
            "Use it as a stool, a plant stand, or a bedside table.",
        ],
        "joinery": [
            ("Compound round tenon", "Three legs enter the seat on compound-angled round "
                                     "tenons, wedged from the top face."),
            ("Kusabi", "Each tenon is slit and wedged through the seat — the visible line "
                       "across the end grain is the wedge."),
            ("Kigoroshi", "Tenons compressed to 0.4mm under before driving."),
        ],
        "dims": [("Width", "420 mm"), ("Depth", "300 mm"), ("Height", "450 mm"),
                 ("Seat thickness", "45 mm"), ("Weight", "5.4 kg")],
        "material": "Solid European oak",
        "finish": "Hardwax oil, matt — natural",
        "lead": "4–6 weeks",
    },
]


def rupees(n):
    s = str(n)
    if len(s) <= 3:
        return "₹" + s
    head, tail = s[:-3], s[-3:]
    parts = []
    while len(head) > 2:
        parts.insert(0, head[-2:])
        head = head[:-2]
    if head:
        parts.insert(0, head)
    return "₹" + ",".join(parts + [tail])
