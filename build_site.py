# -*- coding: utf-8 -*-
"""
Bronze Age Furniture — static site generator.

Run:  python3 build_site.py
Out:  index.html, shop.html, craft.html, about.html, contact.html,
      product/<slug>.html

Everything it emits is plain HTML/CSS/JS. Once built you can delete this
script and edit the HTML by hand — nothing depends on it at runtime.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "data"))
from catalogue import BRAND, CATEGORIES, PRODUCTS, WOOD_GROUPS, STANDARD_WOOD, rupees  # noqa: E402
from build_art import PIECES  # noqa: E402


def art_aspect(key):
    """Nominal width / height of a drawn piece — decides the gallery crop."""
    _, w, h = PIECES[key]()
    return float(w) / float(h)

ROOT = os.path.dirname(os.path.abspath(__file__))

NAV = [
    ("Shop", "shop.html"),
    ("Craft", "craft.html"),
    ("About", "about.html"),
    ("Contact", "contact.html"),
]

ARROW = ('<svg viewBox="0 0 14 9" fill="none" aria-hidden="true">'
         '<path d="M0 4.5h12M8.5 1 12 4.5 8.5 8" stroke="currentColor" '
         'stroke-width="1.2"/></svg>')


# --- shared chrome ---------------------------------------------------------
def head(title, desc, rel="", page_css=""):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#F4F1EA">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300&family=Inter:wght@300;350;400;500&display=swap" rel="stylesheet">
<link rel="icon" href="{rel}assets/img/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{rel}assets/css/site.css">
{page_css}</head>
<body>
""".format(title=title, desc=desc, rel=rel, page_css=page_css)


def header(active, rel=""):
    links = "".join(
        '<a href="{rel}{href}"{cur}>{label}</a>'.format(
            rel=rel, href=href, label=label,
            cur=' aria-current="page"' if href == active else "")
        for label, href in NAV)
    return """<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="brandmark" href="{rel}index.html">Bronze <span>Age</span></a>
    <button class="nav-toggle" data-nav-toggle aria-expanded="false" aria-controls="primary-nav">Menu</button>
    <nav class="nav" id="primary-nav" aria-label="Primary">{links}</nav>
  </div>
</header>
<main>
""".format(rel=rel, links=links)


def signup_form(idp, placeholder="Your email address", cta="Join"):
    return """<form class="signup" data-signup novalidate>
  <label class="sr-only" for="{idp}-email">Email address</label>
  <input id="{idp}-email" type="email" name="email" placeholder="{ph}" autocomplete="email" required>
  <button type="submit">{cta}</button>
</form>
<p class="form-note" role="status"></p>""".format(idp=idp, ph=placeholder, cta=cta)


def footer(rel=""):
    shop_links = "".join(
        '<li><a href="{rel}shop.html#{slug}">{name}</a></li>'.format(rel=rel, slug=slug, name=name)
        for slug, name in CATEGORIES[1:])
    return """</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <p class="eyebrow">The Inner Circle</p>
        <h2 class="h2" style="margin:.75rem 0 1rem;max-width:14ch">New pieces, before anyone else.</h2>
        <p class="small" style="color:rgba(244,241,234,.7);max-width:34ch">
          A short letter every few weeks — new work leaving the bench, notes on
          joinery, and first access to limited runs.</p>
        {signup}
      </div>
      <div>
        <p class="eyebrow">Shop</p>
        <ul class="footer__links" style="margin-top:1rem">
          <li><a href="{rel}shop.html">Everything</a></li>
          {shop_links}
        </ul>
      </div>
      <div>
        <p class="eyebrow">Studio</p>
        <ul class="footer__links" style="margin-top:1rem">
          <li><a href="{rel}craft.html">The Craft</a></li>
          <li><a href="{rel}about.html">About</a></li>
          <li><a href="{rel}contact.html">Contact</a></li>
          <li><a href="{rel}contact.html#trade">Trade &amp; Projects</a></li>
        </ul>
      </div>
      <div>
        <p class="eyebrow">Reach us</p>
        <ul class="footer__links" style="margin-top:1rem">
          <li><a href="mailto:{email}">{email}</a></li>
          <li><a href="tel:{phone_raw}">{phone}</a></li>
          <li><span style="color:rgba(244,241,234,.72);font-size:.875rem">Made to order in {city}</span></li>
        </ul>
      </div>
    </div>
    <div class="footer__base">
      <span>&copy; 2026 {full}. {domain}</span>
      <span>Joined without metal. Finished by hand.</span>
    </div>
  </div>
</footer>
<script src="{rel}assets/js/site.js"></script>
</body>
</html>""".format(
        signup=signup_form("footer"),
        shop_links=shop_links, rel=rel,
        email=BRAND["email"], phone=BRAND["phone"],
        phone_raw=BRAND["phone"].replace(" ", ""),
        city=BRAND["city"], full=BRAND["full"], domain=BRAND["domain"])


# --- components ------------------------------------------------------------
def product_card(p, rel="", delay=0.0, tag=None, ratio="ratio-4x5"):
    img = p.get("photo") or (p["art"] + ".svg")
    return """<a class="card reveal" data-delay="{delay}" data-category="{cat}" href="{rel}product/{slug}.html">
  {tagmarkup}<div class="card__art artframe {ratio}">
    <img src="{rel}assets/img/{img}" alt="{name}" loading="lazy" width="800" height="1000">
  </div>
  <div class="card__body">
    <div>
      <h3 class="card__name">{name}</h3>
      <p class="card__kind">{kind}</p>
    </div>
    <span class="card__price">{price}</span>
  </div>
</a>""".format(
        delay=delay, cat=p["category"], rel=rel, slug=p["slug"], img=img,
        name=p["name"], kind=p["kind"], price="from " + rupees(p["price"]),
        ratio=ratio,
        tagmarkup='<span class="card__tag">%s</span>' % tag if tag else "")


def spec_rows(pairs):
    return "".join("<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % (k, v) for k, v in pairs)


def joint_notes(items):
    return "".join(
        '<div class="joint-note"><h4>%s</h4><p>%s</p></div>' % (k, v) for k, v in items)


def wood_optgroups():
    """<optgroup> markup for the timber families, shared by product pages and
    the enquiry form. STANDARD_WOOD (Walnut) lives inside its family group
    like every other species — it's just marked selected, so it's what shows
    by default."""
    parts = []
    for group_name, species in WOOD_GROUPS:
        parts.append('<optgroup label="%s">' % group_name)
        for s in species:
            if s == STANDARD_WOOD:
                parts.append('<option selected>%s &mdash; standard</option>' % s)
            else:
                parts.append('<option>%s</option>' % s)
        parts.append("</optgroup>")
    return "".join(parts)


def wood_select(select_id, name="timber"):
    """The timber picker used on every product page: STANDARD_WOOD
    pre-selected, every species grouped by family."""
    return ('<select class="wood-picker__select" id="{id}" name="{name}">{groups}</select>').format(
        id=select_id, name=name, groups=wood_optgroups())


# ===========================================================================
#  index.html
# ===========================================================================
def build_index():
    featured = [p for p in PRODUCTS if p.get("featured")][:4]
    cards = "".join(product_card(p, delay=i * 0.08) for i, p in enumerate(featured))

    intro = """<div class="intro" id="intro" hidden>
  <button class="intro__close" data-intro-close type="button" aria-label="Close and enter the site">
    <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M4 4l16 16M20 4L4 20" stroke="currentColor" stroke-width="1.6"/>
    </svg>
  </button>
  <div class="intro__stage">
    <div class="artframe">
      <img src="assets/img/maru-round-dining-table.png" alt="Maru Round Dining Table in solid walnut" width="1600" height="1000">
    </div>
  </div>
  <div class="intro__panel">
    <p class="eyebrow eyebrow--oak">Bronze Age Furniture</p>
    <h2 class="h2" style="margin-top:.6rem">Join the Inner Circle</h2>
    <p class="measure" style="margin-top:.5rem">Early access to new products, exclusive offers and more.</p>
    {signup}
    <button class="intro__skip" data-intro-close type="button">Enter the site</button>
  </div>
</div>
""".format(signup=signup_form("intro"))

    body = """<section class="hero wrap">
  <div class="split" style="align-items:end">
    <div class="stack">
      <p class="eyebrow eyebrow--oak">Solid timber &middot; joined without metal</p>
      <h1 class="display">Wood that<br>holds itself<br>together.</h1>
    </div>
    <div class="stack measure">
      <p class="lede">Every joint in every piece we make is wood into wood.
        No screws, no brackets, no plates, no dowels of any other material.</p>
      <p class="small">Bronze Age builds furniture using Japanese <em>kigumi</em> and
        <em>sashimono</em> joinery &mdash; interlocking geometry cut by hand measurement,
        designed so the timber can move with the season and lock itself tighter as it does.</p>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;padding-top:.5rem">
        <a class="btn" href="shop.html"><span>See the collection</span></a>
        <a class="link-arrow" href="craft.html" style="align-self:center">How it's joined {arrow}</a>
      </div>
    </div>
  </div>
  <div class="hero__art artframe ratio-21x9 reveal">
    <img src="assets/img/hero.svg" alt="Nuki dining table in solid oak with wedged through-tenons" width="2000" height="900">
  </div>
  <div class="hero__meta">
    <p class="small mute">Nuki Dining Table &middot; Walnut &middot; 2400 &times; 900 mm</p>
    <p class="small mute">Made to order &middot; 12&ndash;14 weeks</p>
  </div>
</section>

<section class="manifesto section">
  <div class="wrap">
    <div class="split" style="align-items:start">
      <h2 class="h1 measure-tight">Not a single screw.</h2>
      <p class="lede measure">It began as a constraint and turned out to be the whole design
        language. Take the metal away and the wood has to do the work &mdash;
        which means the geometry has to be right, and the geometry becomes the form.</p>
    </div>
    <div class="grid cols-3" style="margin-top:clamp(2.5rem,6vh,4.5rem)">
      <div class="pillar reveal" data-delay="0">
        <span class="manifesto__num">01</span>
        <h3 class="h3">Metal fails first</h3>
        <p>A screw holds by crushing wood fibres against a thread. As the timber
          moves through the year that grip loosens, and the loosening becomes a
          wobble, then a creak, then a repair. Wood joined to wood moves together.</p>
      </div>
      <div class="pillar reveal" data-delay="0.08">
        <span class="manifesto__num">02</span>
        <h3 class="h3">Load closes the joint</h3>
        <p>Our joints are laid out so the direction of everyday use presses them
          shut. Sitting on a chair, sleeping on a bed, leaning on a table &mdash;
          each of these tightens the structure rather than working it loose.</p>
      </div>
      <div class="pillar reveal" data-delay="0.16">
        <span class="manifesto__num">03</span>
        <h3 class="h3">Repairable forever</h3>
        <p>A wedged tenon can be re-driven in twenty years with a mallet. A
          bonded steel bracket cannot be repaired at all &mdash; only replaced,
          usually along with the piece it was holding.</p>
      </div>
    </div>
  </div>
</section>

<section class="section wrap">
  <div style="display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:1rem;margin-bottom:clamp(2rem,4vh,3rem)">
    <h2 class="h2">Selected pieces</h2>
    <a class="link-arrow" href="shop.html">All {count} pieces {arrow}</a>
  </div>
  <div class="grid cols-4">{cards}</div>
</section>

<section class="section--tight">
  <div class="wrap">
    <div class="artframe ratio-21x9 reveal">
      <img src="assets/img/maru-round-dining-table.png" alt="Maru Round Dining Table, base detail" width="1600" height="900">
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="split">
    <div class="stack">
      <p class="eyebrow eyebrow--oak">The craft</p>
      <h2 class="h1 measure-tight">Three ideas, five centuries old.</h2>
      <p class="measure">Japanese joinery solved the problem of building in solid
        timber without fasteners long before anyone had a reason to. We use three
        of its principles in almost everything we make.</p>
      <a class="link-arrow" href="craft.html">Read the full method {arrow}</a>
    </div>
    <dl class="applies">
      <div class="applies__row">
        <dt>Kigumi &amp; Sashimono</dt>
        <dd>Precise hand measurement and interlocking geometry, cut so the wood can
          expand and contract with humidity without ever splitting or binding.</dd>
      </div>
      <div class="applies__row">
        <dt>Kigoroshi</dt>
        <dd>Wood crushing. The tenon is cut deliberately larger than its mortise,
          its fibres compressed with a hammer, then driven home &mdash; where it
          swells back and locks itself permanently.</dd>
      </div>
      <div class="applies__row">
        <dt>Kusabi</dt>
        <dd>The wedged tenon. A slit is cut in the tenon's end; once through the
          mortise a small oak wedge is driven in, flaring the end like a dovetail
          so it cannot withdraw.</dd>
      </div>
    </dl>
  </div>
</section>

<section class="section--tight">
  <div class="wrap">
    <div class="artframe ratio-21x9 reveal">
      <img src="assets/img/band-bed.svg" alt="Nuki platform bed in solid oak" width="2000" height="760">
    </div>
    <div class="hero__meta">
      <p class="small mute">Nuki Platform Bed &middot; assembles with a mallet in fifteen minutes</p>
      <a class="link-arrow" href="product/nuki-platform-bed.html">See the bed {arrow}</a>
    </div>
  </div>
</section>

<section class="section wrap center">
  <p class="statement" style="margin-inline:auto">A joint you can <em>see</em> is a joint you can <em>trust</em>.</p>
</section>

<section class="section--tight wrap">
  <div class="grid cols-3">
    <div class="pillar reveal">
      <h3 class="h3">Made to order</h3>
      <p>Nothing sits in a warehouse. Each piece is cut, joined and finished for
        one customer, in the order the enquiries arrive.</p>
    </div>
    <div class="pillar reveal" data-delay="0.08">
      <h3 class="h3">Your timber, one finish</h3>
      <p>Walnut is our standard &mdash; and the starting point for twenty-seven
        more species, from teak to weather-ready thermo timbers. Whichever you
        choose, it is finished the same way: hardwax oil, matt.</p>
    </div>
    <div class="pillar reveal" data-delay="0.16">
      <h3 class="h3">Dimensions to suit</h3>
      <p>Every table, bench and bed can be cut to your room. Tell us the number
        and we will quote it.</p>
    </div>
  </div>
</section>
""".format(cards=cards, arrow=ARROW, count=len(PRODUCTS))

    html = (head("Bronze Age Furniture — solid timber, joined without metal",
                 "Minimalist solid-timber furniture made with Japanese kigumi and sashimono "
                 "joinery, in walnut or your choice of 27 more species. No screws, no "
                 "brackets, no metal of any kind. Made to order in India.")
            + intro + header("index.html") + body + footer())
    write("index.html", html)


# ===========================================================================
#  shop.html
# ===========================================================================
def build_shop():
    buttons = "".join(
        '<button type="button" data-filter="%s"%s>%s</button>'
        % (slug, ' class="is-active"' if slug == "all" else "", name)
        for slug, name in CATEGORIES)
    cards = "".join(product_card(p, delay=(i % 4) * 0.06) for i, p in enumerate(PRODUCTS))

    body = """<section class="wrap" style="padding-top:clamp(2.5rem,7vh,5rem)">
  <div class="split" style="align-items:end;margin-bottom:clamp(2rem,5vh,3.5rem)">
    <h1 class="h1">The collection</h1>
    <p class="measure small">Fourteen pieces, joined without metal and cut in the
      timber you choose &mdash; walnut as standard, or any of twenty-seven
      more species, from teak to weather-ready thermo boards. Prices
      are a starting point &mdash; every dimension can be cut to your room, and
      the quote follows the size.</p>
  </div>
  <div class="filters" data-filters>
    {buttons}
    <span class="filters__count">{count} pieces</span>
  </div>
  <div class="grid cols-4" style="margin-bottom:var(--section)">{cards}</div>
  <div class="notice" style="margin-bottom:2rem">
    <strong>Not seeing your size?</strong> Every table, bench and bed here is cut to
    order. Send us the dimensions of your room and we will come back with a drawing
    and a price. <a href="contact.html" style="border-bottom:1px solid currentColor">Start an enquiry</a>.
  </div>
</section>
""".format(buttons=buttons, cards=cards, count=len(PRODUCTS))

    html = (head("Shop — Bronze Age Furniture",
                 "Solid-timber tables, chairs, benches, beds and objects, in walnut "
                 "or your choice of 27 more species, joined without metal using Japanese "
                 "kigumi joinery. Made to order.")
            + header("shop.html") + body + footer())
    write("shop.html", html)


# ===========================================================================
#  craft.html
# ===========================================================================
def build_craft():
    principles = [
        {
            "n": "01",
            "name": "Kigumi &amp; Sashimono",
            "jp": "木組・指物",
            "sub": "Interlocking geometry, cut by hand measurement",
            "img": "diagram-kigumi.svg",
            "cap": "A stepped halving lap. Neither member is weakened at its "
                   "critical section, and the load travels through long grain "
                   "rather than across a fastener.",
            "body": [
                "<em>Kigumi</em> is the framing joinery of Japanese timber "
                "architecture; <em>sashimono</em> is its cabinetmaking cousin, where "
                "the same logic is worked at furniture scale and to furniture "
                "tolerances.",
                "Both depend on precise hand measurement rather than on adhesive or "
                "fastening. Members are cut so they interlock &mdash; each one "
                "capturing the next &mdash; and the assembly holds its geometry "
                "because of how the parts are shaped, not because of what has been "
                "driven through them.",
                "The reason this matters in practice is humidity. Oak moves. A board "
                "900mm wide can change 6&ndash;8mm across its width between a humid "
                "August and a dry February. A rigid metal fixing resists that "
                "movement until something gives &mdash; usually the wood, in the form "
                "of a split. Interlocking joinery is laid out to let the timber "
                "expand and contract along known paths while staying locked in the "
                "directions that matter structurally.",
            ],
        },
        {
            "n": "02",
            "name": "Kigoroshi",
            "jp": "木殺し",
            "sub": "Wood crushing &mdash; a joint that tightens after assembly",
            "img": "diagram-kigoroshi.svg",
            "cap": "Cut proud, crushed, driven, recovered. The final fit is made by "
                   "the timber returning to its own dimension inside the mortise.",
            "body": [
                "Literally &lsquo;killing the wood&rsquo;. The craftsman cuts the "
                "tenon deliberately larger than the mortise it has to enter &mdash; "
                "in our shop, around 0.4mm proud on each cheek.",
                "The tenon will not fit. So the fibres are compressed with a hammer, "
                "worked down until the tenon slides. It is driven home while still "
                "crushed, and then it is left alone.",
                "Over the following hours and days the compressed fibres take up "
                "ambient moisture and swell back towards their original dimension "
                "&mdash; but now they are inside the mortise, and the only place they "
                "can expand into is the mortise wall. The joint becomes tighter than "
                "it could ever have been cut. It is, in the most literal sense, a "
                "joint that finishes itself.",
            ],
        },
        {
            "n": "03",
            "name": "Kusabi",
            "jp": "楔",
            "sub": "The wedged tenon &mdash; mechanically impossible to withdraw",
            "img": "diagram-kusabi.svg",
            "cap": "Once the wedge is driven, the tenon's end is wider than the "
                   "mortise it passed through. Only removing the wedge releases it.",
            "body": [
                "Where a joint has to resist being pulled apart &mdash; a bed rail, a "
                "table stretcher, a stool leg &mdash; we use <em>kusabi</em>.",
                "The tenon passes right through its mortise and stands proud on the "
                "far side. Slits have been cut into that protruding end. A small "
                "tapered oak wedge is driven into each slit, flaring the end of the "
                "tenon outwards until it is wider than the hole it came through.",
                "The result behaves like a dovetail formed after assembly: the joint "
                "cannot withdraw in its principal direction. It is also completely "
                "serviceable. Two decades on, if the oak has settled at all, the "
                "wedge takes one more tap and the joint is new again. Knock the wedge "
                "back out and the piece comes apart for moving.",
            ],
        },
    ]

    blocks = []
    for i, pr in enumerate(principles):
        reverse = i % 2 == 1
        text = """<div class="stack">
        <span class="principle__index">{n}</span>
        <h2 class="h2">{name}<span class="principle__jp">{jp}</span></h2>
        <p class="eyebrow">{sub}</p>
        <div class="stack" style="--stack-gap:1rem;padding-top:.5rem">{paras}</div>
      </div>""".format(n=pr["n"], name=pr["name"], jp=pr["jp"], sub=pr["sub"],
                       paras="".join("<p>%s</p>" % b for b in pr["body"]))
        fig = """<figure class="diagram reveal" style="margin:0">
        <img src="assets/img/{img}" alt="{alt}" loading="lazy" width="900" height="520">
        <figcaption>{cap}</figcaption>
      </figure>""".format(img=pr["img"], alt=pr["sub"], cap=pr["cap"])
        inner = (fig + text) if reverse else (text + fig)
        blocks.append('<div class="principle section--tight"><div class="split">%s</div></div>' % inner)

    body = """<section class="wrap" style="padding-top:clamp(2.5rem,7vh,5rem)">
  <p class="eyebrow eyebrow--oak">The craft</p>
  <h1 class="h1 measure-tight" style="margin-top:1rem">How a Bronze Age piece is held together.</h1>
  <p class="lede measure" style="margin-top:1.5rem">There is no metal in any joint we
    cut. What follows is exactly how that is possible &mdash; the three principles we
    work to, and how each one is applied to a bed, a table and a chair.</p>
</section>

<section class="wrap">{blocks}</section>

<section class="section wrap">
  <div class="rule" style="padding-top:clamp(2rem,5vh,3rem)">
    <p class="eyebrow eyebrow--oak">Application</p>
    <h2 class="h1 measure-tight" style="margin:1rem 0 2rem">Where each principle goes.</h2>
    <dl class="applies">
      <div class="applies__row">
        <dt>Beds</dt>
        <dd>Platform frames use interlocking corner joints and notched cross-beams in
          the <em>nuki</em> style, where downward body weight forces the frame
          components to lock tighter into each other rather than wobble. The side
          rails pass through the posts and are wedged outside them; the load of a
          sleeping body presses on the bearing face of the through-mortise, which is
          precisely the surface that would have to fail for the joint to loosen.</dd>
      </div>
      <div class="applies__row">
        <dt>Tables</dt>
        <dd>Apron-to-leg connections use angled mortise-and-tenon configurations
          reinforced with hidden keys or pins, preventing the lateral wobble that
          comes from daily use &mdash; leaning, pushing back from the table, dragging
          it a few centimetres to sweep. Tops are never fixed rigidly: they are held
          on buttons or slotted keys that let the panel move across its width by up
          to 6mm a year without stressing the frame.</dd>
      </div>
      <div class="applies__row">
        <dt>Chairs</dt>
        <dd>The highest-stress joints in any chair are where the seat meets the
          backrest and the legs. These employ pinned or keyed blind tenons that
          withstand shifting pressure and tension without loosening. Where we can, we
          remove the joint altogether &mdash; the Kake armchair's arms and front legs
          are cut from a single blank, so the load path from armrest to floor never
          crosses a joint at all.</dd>
      </div>
    </dl>
  </div>
</section>

<section class="section wrap">
  <div class="split">
    <div class="stack">
      <p class="eyebrow eyebrow--oak">Material</p>
      <h2 class="h2">Every timber. One finish.</h2>
      <p class="measure">Walnut is our standard, kiln-dried to 8&ndash;10%
        moisture content and then rested in our shop for a further six weeks before
        it is cut. Quartersawn for tops where flatness matters most; through-and-through
        elsewhere, because the figure is worth having. Order in any of the twenty-seven
        further species we offer &mdash; teak, ash, cedar and more &mdash; and it is
        prepared to the same standard.</p>
      <p class="measure">Whatever the species, it is finished in hardwax oil, matt,
        applied in two coats and cut back by hand between them. Nothing sits on the
        surface as a film. You are touching timber, not lacquer &mdash; which is also
        why a scratch can be spot-repaired in ten minutes rather than requiring the
        whole panel to be stripped.</p>
    </div>
    <div class="stack">
      <p class="eyebrow eyebrow--oak">Care</p>
      <h2 class="h2">What it asks of you.</h2>
      <div class="accordion" style="margin-top:1.5rem">
        <details open><summary>Everyday</summary><div class="acc-body small">
          A dry or barely damp cloth. No solvents, no silicone polish, no
          &lsquo;wood feeding&rsquo; sprays &mdash; hardwax oil does not need them and
          silicone makes future repair difficult.</div></details>
        <details><summary>Spills and marks</summary><div class="acc-body small">
          Wipe promptly; oak reacts with iron and acidic liquids. A water ring will
          usually lift with a light re-oil of the area. We send a small bottle of the
          same oil with every piece.</div></details>
        <details><summary>Once a year</summary><div class="acc-body small">
          Re-oil surfaces that see daily use &mdash; a dining top, a desk. Ten minutes
          with a lint-free cloth, wiped back after twenty minutes.</div></details>
        <details><summary>Seasonal movement</summary><div class="acc-body small">
          Expect a few millimetres of change across wide panels between wet and dry
          months. This is the timber working as intended. Nothing needs tightening,
          because there is nothing to tighten.</div></details>
        <details><summary>If a joint ever moves</summary><div class="acc-body small">
          On wedged joints, one firm tap on the wedge with a mallet. That is the whole
          maintenance schedule. Send us a photograph if you would rather we talked you
          through it.</div></details>
      </div>
    </div>
  </div>
</section>

<section class="section wrap center">
  <p class="statement" style="margin-inline:auto">Cut it right and the wood <em>does the rest</em>.</p>
  <div style="margin-top:2.5rem"><a class="btn" href="shop.html"><span>See the collection</span></a></div>
</section>
""".format(blocks="".join(blocks))

    html = (head("The Craft — Kigumi, Kigoroshi and Kusabi | Bronze Age Furniture",
                 "How Bronze Age furniture is joined without metal: kigumi and sashimono "
                 "interlocking geometry, kigoroshi wood crushing, and kusabi wedged tenons.")
            + header("craft.html") + body + footer())
    write("craft.html", html)


# ===========================================================================
#  about.html
# ===========================================================================
def build_about():
    body = """<section class="wrap" style="padding-top:clamp(2.5rem,7vh,5rem)">
  <p class="eyebrow eyebrow--oak">About</p>
  <h1 class="h1 measure-tight" style="margin-top:1rem">A workshop with one rule.</h1>
  <p class="lede measure" style="margin-top:1.5rem">No metal in any joint. Everything
    else about Bronze Age &mdash; the proportions, the choice of timber, the way a
    piece arrives flat and goes together with a mallet &mdash; follows from that one
    decision.</p>
</section>

<section class="section--tight wrap">
  <div class="artframe ratio-3x2 reveal">
    <img src="assets/img/about.svg" alt="Ita plank table in solid walnut" width="1400" height="1000">
  </div>
</section>

<section class="section wrap">
  <div class="split" style="align-items:start">
    <div class="stack">
      <h2 class="h2">Why the rule exists</h2>
      <p>Most furniture that looks solid is not. A screw into end grain holds by
        crushing a few millimetres of fibre against a thread, and it is the weakest
        connection in the object from the day it is driven. Everything else &mdash;
        the timber, the finish, the design &mdash; outlives it.</p>
      <p>Take the metal out and there is nowhere to hide. The geometry has to carry
        the load, which means it has to be laid out properly, which means it becomes
        the thing you actually see. That is the whole aesthetic argument for this
        work, and we did not invent it. Japanese joiners settled it centuries ago.</p>
    </div>
    <div class="stack">
      <h2 class="h2">How we work</h2>
      <p>Hand measurement first. Every piece is set out full-size before anything is
        cut, because interlocking joinery has no tolerance for accumulated error &mdash;
        a millimetre out at the first mortise is four millimetres out at the last.</p>
      <p>Machines do the removal, hands do the fit. A hollow-chisel mortiser punches
        clean square sockets; a tenoner takes the halving notches in a single pass.
        The final half-millimetre &mdash; the part that decides whether the joint is
        good &mdash; is always a chisel, a hammer, and someone's judgement.</p>
    </div>
  </div>
</section>

<section class="manifesto section">
  <div class="wrap">
    <p class="eyebrow eyebrow--oak">Ordering</p>
    <h2 class="h1 measure-tight" style="margin:1rem 0 2.5rem">Four steps, ten to sixteen weeks.</h2>
    <div class="grid cols-4">
      <div class="pillar reveal"><span class="manifesto__num">01</span>
        <h3 class="h3">Enquire</h3>
        <p>Tell us the piece, the room and the dimensions. A photograph of the space
          helps more than you would think.</p></div>
      <div class="pillar reveal" data-delay="0.08"><span class="manifesto__num">02</span>
        <h3 class="h3">Drawing &amp; quote</h3>
        <p>We come back within two working days with a dimensioned drawing, a timber
          note and a fixed price. No obligation.</p></div>
      <div class="pillar reveal" data-delay="0.16"><span class="manifesto__num">03</span>
        <h3 class="h3">Cut &amp; joined</h3>
        <p>Fifty per cent to start. Your boards are selected, rested, cut and joined.
          We send progress photographs at the bench.</p></div>
      <div class="pillar reveal" data-delay="0.24"><span class="manifesto__num">04</span>
        <h3 class="h3">Delivered</h3>
        <p>Balance on completion. Larger pieces ship knocked-down and assemble with a
          mallet &mdash; no tools, no fixings, no allen key.</p></div>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="split">
    <div class="stack">
      <h2 class="h2">On sustainability, honestly</h2>
      <p>Our walnut is FSC-certified and responsibly sourced. The further
        species we offer are sourced from certified, legally verified
        suppliers to the same standard. We are a small shop, so we will not
        pretend our supply chain is a closed loop.</p>
      <p>What we can claim is more specific: a piece with no metal in it can be fully
        repaired, fully disassembled, and at the very end of its life it is one
        material. Nothing has to be separated before it can be recycled or returned to
        the ground. The most sustainable thing a piece of furniture can do is not need
        replacing, and joinery is how that is achieved.</p>
    </div>
    <div class="stack">
      <h2 class="h2">Where we are</h2>
      <p>Bronze Age is made to order in {city}. Visits to the workshop are by
        appointment &mdash; we would rather show you a joint than a photograph of one.</p>
      <p class="small mute">{email}<br>{phone}</p>
      <div style="padding-top:.5rem"><a class="btn" href="contact.html"><span>Start an enquiry</span></a></div>
    </div>
  </div>
</section>
""".format(city=BRAND["city"], email=BRAND["email"], phone=BRAND["phone"])

    html = (head("About — Bronze Age Furniture",
                 "A workshop with one rule: no metal in any joint. How and why Bronze Age "
                 "builds solid-timber furniture, in walnut and beyond, using Japanese "
                 "joinery.")
            + header("about.html") + body + footer())
    write("about.html", html)


# ===========================================================================
#  contact.html
# ===========================================================================
def build_contact():
    options = "".join('<option value="%s">%s</option>' % (p["name"], p["name"]) for p in PRODUCTS)
    body = """<section class="wrap" style="padding-top:clamp(2.5rem,7vh,5rem)">
  <div class="split" style="align-items:start">
    <div class="stack">
      <p class="eyebrow eyebrow--oak">Contact</p>
      <h1 class="h1" style="margin-top:.5rem">Start an enquiry</h1>
      <p class="measure">Every piece is made to order, so the conversation starts
        before the price does. Tell us what you are after and we will reply within two
        working days with a drawing and a fixed quote.</p>
      <div class="rule" style="padding-top:1.5rem;margin-top:1.5rem">
        <p class="eyebrow">Direct</p>
        <p class="small" style="margin-top:.75rem">
          <a href="mailto:{email}" style="border-bottom:1px solid var(--line)">{email}</a><br>
          <a href="tel:{phone_raw}" style="border-bottom:1px solid var(--line)">{phone}</a></p>
      </div>
      <div class="rule" style="padding-top:1.5rem;margin-top:1.5rem" id="trade">
        <p class="eyebrow">Trade &amp; projects</p>
        <p class="small" style="margin-top:.75rem">Architects, interior designers and
          hospitality projects &mdash; we work to drawings and hold trade terms. Mention
          the project scale in your message and we will send the trade sheet.</p>
      </div>
      <div class="rule" style="padding-top:1.5rem;margin-top:1.5rem">
        <p class="eyebrow">Workshop visits</p>
        <p class="small" style="margin-top:.75rem">By appointment, in {city}. Worth it
          if you are deciding between two pieces &mdash; joinery photographs badly and
          reads instantly in person.</p>
      </div>
    </div>

    <div>
      <form data-enquiry novalidate>
        <div class="field">
          <label for="c-name">Your name</label>
          <input id="c-name" name="name" type="text" autocomplete="name" required>
        </div>
        <div class="field">
          <label for="c-email">Email</label>
          <input id="c-email" name="email" type="email" autocomplete="email" required>
        </div>
        <div class="field">
          <label for="c-piece">Piece you're interested in</label>
          <select id="c-piece" name="piece">
            <option value="">Not sure yet / something else</option>
            {options}
          </select>
        </div>
        <div class="field">
          <label for="c-wood">Preferred timber (optional)</label>
          <select id="c-wood" name="timber">
            <option value="">No preference &mdash; recommend one</option>
            {wood_groups}
          </select>
        </div>
        <div class="field">
          <label for="c-dims">Room or dimensions (optional)</label>
          <input id="c-dims" name="dimensions" type="text" placeholder="e.g. 2200 mm max length, seats 8">
        </div>
        <div class="field">
          <label for="c-msg">Message</label>
          <textarea id="c-msg" name="message" rows="5" placeholder="Tell us about the space, the timing, anything you're unsure about."></textarea>
        </div>
        <button class="btn" type="submit"><span>Send enquiry</span></button>
        <p class="form-note" role="status"></p>
      </form>

      <div class="accordion" style="margin-top:clamp(2.5rem,6vh,4rem)">
        <details><summary>How long does an order take?</summary><div class="acc-body small">
          Between four and sixteen weeks depending on the piece &mdash; the lead time
          is listed on each product page. Larger dining tables and beds sit at the
          longer end.</div></details>
        <details><summary>Can you change the dimensions?</summary><div class="acc-body small">
          Almost always. Length, width and height are all adjustable on tables,
          benches and beds. Chair dimensions are fixed, because the joinery angles are
          set out for that geometry.</div></details>
        <details><summary>Do you ship outside India?</summary><div class="acc-body small">
          Yes, on request. Knocked-down pieces ship well because there are no fixings
          to lose. Ask us for a freight quote with your enquiry.</div></details>
        <details><summary>Is there really no metal at all?</summary><div class="acc-body small">
          No metal in any joint &mdash; that is the rule and we do not break it. The
          only exceptions anywhere in the catalogue are non-structural: the toughened
          glass top on the Hashira coffee table, and the jute webbing and linen on the
          Kura sofa. Both are removable without touching the frame.</div></details>
        <details><summary>What if something goes wrong?</summary><div class="acc-body small">
          Write to us. Wedged joints re-tighten with a mallet; oiled surfaces spot-repair
          in minutes. Anything structural inside the first ten years, we put right.</div></details>
      </div>
    </div>
  </div>
</section>
""".format(email=BRAND["email"], phone=BRAND["phone"],
           phone_raw=BRAND["phone"].replace(" ", ""), city=BRAND["city"], options=options,
           wood_groups=wood_optgroups())

    html = (head("Contact — Bronze Age Furniture",
                 "Start an enquiry for a made-to-order solid-timber piece, joined without metal.")
            + header("contact.html") + body + footer())
    write("contact.html", html)


# ===========================================================================
#  product pages
# ===========================================================================
def build_products():
    for i, p in enumerate(PRODUCTS):
        prev_p = PRODUCTS[i - 1]
        next_p = PRODUCTS[(i + 1) % len(PRODUCTS)]
        related = [q for q in PRODUCTS if q["category"] == p["category"] and q is not p][:3]
        if len(related) < 3:
            related += [q for q in PRODUCTS if q not in related and q is not p][:3 - len(related)]

        rel_cards = "".join(product_card(q, rel="../", delay=j * 0.08)
                            for j, q in enumerate(related))

        # a 2.4-metre table drowns in a portrait crop; wide pieces get a wide frame
        wide = art_aspect(p["art"]) >= 1.9
        lead_ratio = "ratio-3x2" if wide else "ratio-4x5"
        # a real photo (p["photo"]) stands in for both gallery frames, since
        # there's only one crop of it; drawn pieces still get their two
        # purpose-drawn SVG variants
        lead_img = p.get("photo") or (p["art"] + ("-wide" if wide else "") + ".svg")
        detail_img = p.get("photo") or (p["art"] + "-sq.svg")

        body = """<div class="wrap">
  <p class="breadcrumb"><a href="../index.html">Home</a> &nbsp;/&nbsp;
    <a href="../shop.html#{cat}">{catname}</a> &nbsp;/&nbsp;
    <span style="color:var(--ink)">{name}</span></p>
</div>

<section class="wrap">
  <div class="pdp">
    <div class="pdp__gallery">
      <div class="artframe {lead_ratio}">
        <img src="../assets/img/{lead_img}" alt="{name}" width="800" height="1000">
      </div>
      <div class="artframe ratio-1x1">
        <img src="../assets/img/{detail_img}" alt="{name}, detail" loading="lazy" width="1000" height="1000">
      </div>
      <figure class="diagram" style="margin:0">
        <img src="../assets/img/diagram-{dia}.svg" alt="Joinery diagram" loading="lazy" width="900" height="520">
        <figcaption>{diacap}</figcaption>
      </figure>
    </div>

    <div class="pdp__info">
      <p class="eyebrow eyebrow--oak">{kind}</p>
      <h1 class="h1" style="margin-top:.6rem">{name}</h1>
      <p class="pdp__price">from {price} &middot; made to order</p>
      <p class="lede" style="margin-top:1.5rem">{lede}</p>

      <div class="wood-picker" style="margin-top:1.75rem">
        <label class="eyebrow" for="wood-{slug}">Choose your timber</label>
        {wood_select}
        <p class="small mute" style="margin-top:.5rem">Shown in walnut, our
          standard. Every piece here can be ordered in any of the twenty-eight
          timbers above &mdash; species outside walnut may adjust price and
          lead time, confirmed when we send your drawing.</p>
      </div>

      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin:2rem 0">
        <a class="btn" href="../contact.html"><span>Enquire about this piece</span></a>
        <a class="link-arrow" href="../craft.html" style="align-self:center">The joinery {arrow}</a>
      </div>

      <table class="spec">
        <caption class="sr-only">Specification</caption>
        <tbody>
          {specs}
          <tr><th scope="row">Standard timber</th><td>{material}</td></tr>
          <tr><th scope="row">Finish</th><td>{finish}</td></tr>
          <tr><th scope="row">Metal content</th><td>None in any joint</td></tr>
          <tr><th scope="row">Lead time</th><td>{lead}</td></tr>
        </tbody>
      </table>

      <div class="accordion" style="margin-top:2.5rem">
        <details open>
          <summary>How it is joined</summary>
          <div class="acc-body">{joints}</div>
        </details>
        <details>
          <summary>Dimensions &amp; alterations</summary>
          <div class="acc-body small">
            <p>The dimensions above are our standard set-out. Length, width and height
              can be cut to your room on request &mdash; send us the constraint and we
              will return a dimensioned drawing and a revised price.</p>
            <p>Because the joinery is laid out full-size before cutting, a change in
              dimension is a change in set-out, not an adaptation of a standard part.
              Nothing is compromised by asking.</p>
          </div>
        </details>
        <details>
          <summary>Care</summary>
          <div class="acc-body small">
            <p>Dry or barely damp cloth. No solvents, no silicone polish. Re-oil
              surfaces in daily use about once a year &mdash; we send a bottle of the
              same hardwax oil with every piece.</p>
            <p>Expect a few millimetres of seasonal movement across wide panels. That
              is the joinery working as designed.</p>
          </div>
        </details>
        <details>
          <summary>Delivery &amp; assembly</summary>
          <div class="acc-body small">
            <p>Lead time {lead} from confirmed drawing. Fifty per cent deposit to
              start, balance on completion.</p>
            <p>Larger pieces ship knocked-down and assemble with a rubber mallet. There
              are no fixings to lose, no tools required, and no allen key taped inside
              the packaging.</p>
          </div>
        </details>
      </div>
    </div>
  </div>
</section>

<section class="section wrap">
  <div class="split" style="align-items:start">
    <h2 class="h1 measure-tight">The thinking</h2>
    <div class="stack measure">{story}</div>
  </div>
</section>

<section class="section--tight wrap">
  <h2 class="h2" style="margin-bottom:clamp(1.5rem,4vh,2.5rem)">Goes with</h2>
  <div class="grid cols-3">{rel_cards}</div>
  <div class="pagenav">
    <a class="link-arrow" href="{prev}.html" style="border:0">&larr; {prevname}</a>
    <a class="link-arrow" href="{next}.html" style="border:0">{nextname} &rarr;</a>
  </div>
</section>
""".format(
            cat=p["category"],
            catname=dict(CATEGORIES)[p["category"]],
            slug=p["slug"], wood_select=wood_select("wood-%s" % p["slug"]),
            name=p["name"], lead_img=lead_img, detail_img=detail_img, lead_ratio=lead_ratio,
            dia=("kusabi" if any("Kusabi" in k for k, _ in p["joinery"])
                 else "kigoroshi" if any("Kigoroshi" in k for k, _ in p["joinery"])
                 else "kigumi"),
            diacap="The principle this piece leans on hardest. See "
                   "<a href=\"../craft.html\" style=\"border-bottom:1px solid currentColor\">the craft</a> "
                   "for the full method.",
            kind=p["kind"], price=rupees(p["price"]), lede=p["lede"],
            specs=spec_rows(p["dims"]), material=p["material"], finish=p["finish"],
            lead=p["lead"], joints=joint_notes(p["joinery"]),
            story="".join("<p>%s</p>" % s for s in p["story"]),
            rel_cards=rel_cards, arrow=ARROW,
            prev=prev_p["slug"], prevname=prev_p["name"],
            next=next_p["slug"], nextname=next_p["name"])

        html = (head("%s — Bronze Age Furniture" % p["name"],
                     p["lede"][:155], rel="../")
                + header("shop.html", rel="../") + body + footer(rel="../"))
        write(os.path.join("product", "%s.html" % p["slug"]), html)


# ===========================================================================
def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)


def build_meta():
    base = "https://%s/" % BRAND["domain"]
    urls = ["index.html", "shop.html", "craft.html", "about.html", "contact.html"]
    urls += ["product/%s.html" % p["slug"] for p in PRODUCTS]
    entries = "".join(
        "  <url><loc>%s%s</loc><changefreq>monthly</changefreq>"
        "<priority>%s</priority></url>\n"
        % (base, "" if u == "index.html" else u, "1.0" if u == "index.html" else "0.7")
        for u in urls)
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n' % entries)
    write("robots.txt", "User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n" % base)


if __name__ == "__main__":
    build_index()
    build_shop()
    build_craft()
    build_about()
    build_contact()
    build_products()
    build_meta()
    print("built %d pages" % (5 + len(PRODUCTS)))
