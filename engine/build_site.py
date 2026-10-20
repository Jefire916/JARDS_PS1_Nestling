"""
Builds the Nestling website (static files) from the product list and the engine output.

Run:  python3 engine/build_site.py
Out:  docs/   (GitHub Pages serves this folder: Settings > Pages > main > /docs)

Pages
  index.html                  the shop (product grid, Nest Helper chat bubble)
  shop/<slug>/index.html      one page per product (link target for every chat button)
  how-it-works/index.html     how Nest Helper decides: steps, today's decisions, what is real
"""
import csv, os, re, html, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA, OUT = os.path.join(ROOT, "data"), os.path.join(ROOT, "output")
SITE = os.path.join(ROOT, "docs")
GITHUB = "https://github.com/Jefire916/JARDS_PS1_Nestling"

def rd(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

products = rd(os.path.join(DATA, "products.csv"))
decisions = rd(os.path.join(OUT, "decisions.csv"))
messages = {r["customer_id"]: r for r in rd(os.path.join(OUT, "messages.csv"))}
e = html.escape

# ------------------------------------------------------------------ helpers
def slug(p):
    return p["url"].rstrip("/").split("/")[-1]

def short(p):
    n = re.sub(r"\s*\(\d+\)\s*$", "", p["name"])
    if p["category"] in ("formula_infant", "milk_growing_up"):
        n = re.sub(r"\s*\(fictional brand\)", "", n)
        n = re.sub(r"\s+800g$", "", n)
        n = re.sub(r"\s+\d+(-\d+)?[MY]$", "", n)
    return n

def pack_count(p):
    m = re.search(r"\((\d+)\)", p["name"])
    return m.group(1) if m else ""

CAT = {  # label, tile colour, shape colour
    "diapers": ("Diapers", "#CFE0FF", "#3B5BDB"),
    "wipes": ("Wipes", "#BDE7D3", "#1F8A5B"),
    "clothing": ("Clothing", "#FFCFD6", "#D6336C"),
    "bundle": ("Stage bundles", "#FFE49A", "#C77D00"),
    "toys": ("Toys", "#DCD3FF", "#6741D9"),
    "formula_infant": ("Formula and milk", "#E4E8F1", "#4A5578"),
    "milk_growing_up": ("Formula and milk", "#E4E8F1", "#4A5578"),
}
FILTERS = [("all", "All"), ("diapers", "Diapers"), ("wipes", "Wipes"), ("clothing", "Clothing"),
           ("bundle", "Stage bundles"), ("toys", "Toys"), ("formula", "Formula and milk")]

def filter_key(p):
    return "formula" if p["category"] in ("formula_infant", "milk_growing_up") else p["category"]

def age_text(p):
    lo, hi = int(p["min_age_m"]), int(p["max_age_m"])
    if lo == 0 and hi >= 24:
        return "all ages"
    if hi >= 36:
        return f"from {lo} months"
    if hi > 24:
        return f"{lo} months to {hi // 12} years"
    return f"{lo} to {hi} months" if lo else f"up to {hi} months"

def art(p):
    """Simple flat illustration per category, drawn in SVG (no image files needed)."""
    _, bg, fg = CAT[p["category"]]
    c = p["category"]
    size = p["size"]
    shapes = ""
    if c == "diapers":
        label = size if size != "NB" else "NB"
        shapes = f'''<rect x="52" y="48" width="96" height="108" rx="20" fill="#fff" stroke="{fg}" stroke-width="5"/>
        <path d="M52 88h96" stroke="{fg}" stroke-width="5"/>
        <path d="M100 118c-9-9-14-14-14-20a8 8 0 0 1 14-5 8 8 0 0 1 14 5c0 6-5 11-14 20z" fill="{fg}"/>
        <text x="100" y="146" text-anchor="middle" font-size="22" font-weight="800" fill="{fg}">{e(label)}</text>
        <rect x="64" y="58" width="72" height="14" rx="7" fill="{bg}"/>'''
    elif c == "wipes":
        shapes = f'''<rect x="50" y="78" width="100" height="78" rx="18" fill="#fff" stroke="{fg}" stroke-width="5"/>
        <rect x="58" y="56" width="84" height="26" rx="12" fill="{fg}"/>
        <path d="M100 98c-10 12-16 19-16 27a16 16 0 0 0 32 0c0-8-6-15-16-27z" fill="{bg}" stroke="{fg}" stroke-width="4"/>'''
    elif c == "clothing":
        shapes = f'''<path d="M70 52l-34 24 14 22 16-9v70h68V89l16 9 14-22-34-24c-4 12-14 18-30 18s-26-6-30-18z" fill="#fff" stroke="{fg}" stroke-width="5" stroke-linejoin="round"/>
        <circle cx="100" cy="112" r="9" fill="{fg}"/>'''
    elif c == "bundle":
        shapes = f'''<rect x="46" y="84" width="108" height="72" rx="10" fill="#fff" stroke="{fg}" stroke-width="5"/>
        <rect x="40" y="64" width="120" height="26" rx="8" fill="{fg}"/>
        <path d="M100 64v92" stroke="{bg}" stroke-width="12"/>
        <path d="M100 62c-8-24-34-22-30-8 3 10 20 8 30 8zm0 0c8-24 34-22 30-8-3 10-20 8-30 8z" fill="none" stroke="{fg}" stroke-width="5"/>'''
    elif c == "toys":
        shapes = f'''<rect x="62" y="122" width="76" height="30" rx="10" fill="#fff" stroke="{fg}" stroke-width="5"/>
        <rect x="72" y="88" width="56" height="30" rx="10" fill="{fg}"/>
        <rect x="82" y="56" width="36" height="28" rx="10" fill="#fff" stroke="{fg}" stroke-width="5"/>'''
    else:  # formula / milk tin
        label = size.replace("Stage ", "S") if size else ""
        shapes = f'''<rect x="62" y="56" width="76" height="102" rx="12" fill="#fff" stroke="{fg}" stroke-width="5"/>
        <rect x="58" y="44" width="84" height="20" rx="8" fill="{fg}"/>
        <rect x="74" y="88" width="52" height="40" rx="8" fill="{bg}"/>
        <text x="100" y="116" text-anchor="middle" font-size="20" font-weight="800" fill="{fg}">{e(label)}</text>'''
    return f'<svg viewBox="0 0 200 200" role="img" aria-label="{e(short(p))}" xmlns="http://www.w3.org/2000/svg"><rect width="200" height="200" fill="{bg}"/>{shapes}</svg>'

def describe(p):
    c, name = p["category"], short(p)
    if c == "diapers":
        return (f"{name}, for babies {age_text(p)}. One pack lasts most families about {p['pack_days']} days. "
                "If it leaks or leaves red marks, try the next size up.")
    if c == "wipes":
        return f"{name}. Gentle on skin, one pack lasts most families about {p['pack_days']} days."
    if c == "clothing":
        return f"{name}. Soft cotton, for babies {age_text(p)}. Between sizes? Pick the larger one."
    if c == "bundle":
        return (f"{name}: clothes, a sleepsuit and diapers in the right size, ready in one tap. "
                f"For babies {age_text(p)}.")
    if c == "toys":
        if p["collection_piece"]:
            return f"{name}. Piece {p['collection_piece']} of 4 in the Sensory Set, for babies {age_text(p)}."
        return f"{name}. For babies {age_text(p)}."
    return (f"{name}, 800g. Sold at our usual price. Nestling doesn't recommend brands or give feeding advice, "
            "so please ask your doctor or nurse.")

def perk(p):
    c = p["category"]
    if c in ("diapers", "wipes"):
        return "Buy 3 of the same pack and save 10%."
    if c == "bundle":
        return "Free delivery and free size exchange within 30 days."
    if c == "clothing":
        return "Free size exchange within 30 days, unworn with tags."
    return ""

# ------------------------------------------------------------------ page shell
LOGO = ('<svg viewBox="0 0 40 40" width="30" height="30" aria-hidden="true"><circle cx="20" cy="20" r="20" fill="#FFE49A"/>'
        '<path d="M7 22c3 9 23 9 26 0" fill="none" stroke="#1F2147" stroke-width="3.2" stroke-linecap="round"/>'
        '<circle cx="20" cy="14" r="5.5" fill="#1F2147"/></svg>')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40'%3E%3Ccircle cx='20' cy='20' r='20' fill='%23FFE49A'/%3E"
           "%3Cpath d='M7 22c3 9 23 9 26 0' fill='none' stroke='%231F2147' stroke-width='3.2' stroke-linecap='round'/%3E%3Ccircle cx='20' cy='14' r='5.5' fill='%231F2147'/%3E%3C/svg%3E")

def page(title, body, depth, desc, active=""):
    b = "../" * depth
    nav = f'''<header class="top"><div class="wrap bar">
  <a class="brand" href="{b or './'}">{LOGO}<span>Nestling</span></a>
  <nav aria-label="Main">
    <a href="{b}#shop"{' aria-current="page"' if active == 'shop' else ''}>Shop</a>
    <a href="{b}how-it-works/"{' aria-current="page"' if active == 'how' else ''}>How it works</a>
    <a class="basket" href="{b}#shop" id="basket-link" aria-label="Basket">Basket <b id="basket-count">0</b></a>
  </nav></div></header>'''
    foot = f'''<footer class="foot"><div class="wrap">
  <div><div class="brand small">{LOGO}<span>Nestling</span></div>
  <p>Baby essentials for Singapore families, from newborn to three years.</p></div>
  <div><p>Free size exchange on clothing and bundles within 30 days. Delivery 2 to 4 working days.</p>
  <p>Nestling follows Singapore's SIFECS code: no offers, reminders or brand advice for infant formula.</p></div>
  <p class="fine">Nestling is a fictional shop created by Team JARDS for AI-GNITION 2026. Nest Helper is an AI assistant. <a href="{GITHUB}">Source code</a></p>
</div></footer><div class="toast" id="toast" role="status" aria-live="polite"></div>'''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Figtree:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{b}assets/style.css">
</head><body>
<a class="skip" href="#main">Skip to content</a>
{nav}
<main id="main">{body}</main>
{foot}
<script src="{b}assets/site.js" defer></script>
<script src="{b}assets/chat.js" defer></script>
</body></html>'''

def card(p):
    return f'''<a class="pcard" href="shop/{slug(p)}/" data-cat="{filter_key(p)}">
  <div class="art">{art(p)}</div>
  <div class="pbody"><h3>{e(short(p))}</h3><p class="meta">{e(p['size'] + ' · ' if p['size'] else '')}{e(age_text(p))}</p>
  <p class="price">S${e(p['price_sgd'])}</p></div></a>'''

# ------------------------------------------------------------------ home
def home():
    chips = "".join('<button class="chip" data-filter="%s" aria-pressed="%s">%s</button>' % (k, "true" if k == "all" else "false", v) for k, v in FILTERS)
    order = ["diapers", "wipes", "bundle", "clothing", "toys", "formula_infant", "milk_growing_up"]
    grid = "".join(card(p) for p in sorted(products, key=lambda p: order.index(p["category"])))
    why = ("We predicted when your Size 3 diapers run out from how often you reorder them, and checked the size against your "
           "baby's age (10 months). You said yes to reminders. I don't use your name, photos or address. Type STOP any time.")
    body = f'''
<section class="hero"><div class="wrap hero-grid">
  <div class="hero-copy">
    <h1>Right size,<br>right time,<br>one tap.</h1>
    <p class="lede">Nestling remembers what your little one needs next: diapers before the pack runs out, the next size before the last one gets tight. Nest Helper, our AI assistant, sends one useful nudge when it matters and a real person is always one word away.</p>
    <div class="cta-row"><a class="btn primary" href="#shop">Shop Nestling</a><a class="btn" href="how-it-works/">See how Nest Helper decides</a></div>
    <p class="hint">Say hi to Nest Helper in the chat bubble, bottom right.</p>
  </div>
  <div class="thread" aria-label="Example reminder from Nest Helper">
    <div class="who">Example: a reminder Nest Helper sends to a parent of a 10-month-old. Tap “Why this message?”</div>
    <div class="bub b1">Hi! It's Nest Helper from Nestling 🐣</div>
    <div class="bub b2">Your Size 3 diapers should be running out around now. At 10 months, lots of babies move up to Size 4, so I've put both below.</div>
    <div class="msgcard b3"><div class="mc-art">{art(next(p for p in products if p["item_id"] == "DP-4"))}</div>
      <div class="mc-body"><b>Diapers Size 4 · S$18</b><span>Next size up. Buy 3, save 10%.</span>
      <a class="mbtn" href="shop/diapers-4/?utm_source=livechat&amp;utm_medium=refill&amp;utm_campaign=nestling_ai&amp;utm_content=DP-4">Reorder Size 4</a>
      <a class="mbtn ghost" href="shop/diapers-3/?utm_source=livechat&amp;utm_medium=refill&amp;utm_campaign=nestling_ai&amp;utm_content=DP-3">Keep Size 3</a></div></div>
    <div class="qr b4"><span>Remind me in 3 days</span><button type="button" id="why-btn" aria-expanded="false" aria-controls="why-panel">Why this message?</button><span>Stop messages</span></div>
    <div class="why" id="why-panel" hidden>{e(why)}</div>
  </div>
</div></section>

<section class="wrap shop" id="shop">
  <div class="shop-head"><h2>Shop</h2><div class="chips" role="group" aria-label="Filter products">{chips}</div></div>
  <div class="grid" id="grid">{grid}</div>
</section>

<section class="wrap promises">
  <div><h3>A free swap if it doesn't fit</h3><p>Exchange clothes and bundles for another size within 30 days. Unworn, with tags. Delivery is free both ways.</p></div>
  <div><h3>A person when you want one</h3><p>Type HUMAN in the chat and a Nestling team member picks up the conversation. They can see what you've already said.</p></div>
  <div><h3>Reminders only if you say yes</h3><p>Nest Helper uses your baby's age band and what you've bought. Never a name, photo or address. Type STOP and it goes quiet.</p></div>
</section>'''
    return page("Nestling | Baby essentials for Singapore families", body, 0,
                "Diapers, wipes, clothing and more for babies from newborn to 3 years. Chat with Nest Helper, Nestling's AI assistant.", "shop")

# ------------------------------------------------------------------ product pages
def product_page(p):
    perk_line = perk(p)
    formula = p["category"] in ("formula_infant", "milk_growing_up")
    extra = ""
    if formula:
        extra = '<p class="note">Usual price, no offers. We can\'t advise on feeding: please ask your doctor or nurse.</p>'
    body = f'''
<div class="wrap crumbs"><a href="../../">Shop</a> <span aria-hidden="true">/</span> <a href="../../#{filter_key(p)}" data-back="{filter_key(p)}">{CAT[p["category"]][0]}</a></div>
<div class="wrap pdp">
  <div class="pdp-art">{art(p)}</div>
  <div class="pdp-info">
    <div class="from" id="from" hidden></div>
    <h1>{e(p["name"])}</h1>
    <p class="meta">{e(p['size'] + ' · ' if p['size'] else '')}{e(age_text(p))}</p>
    <p class="big-price">S${e(p["price_sgd"])}</p>
    <p>{e(describe(p))}</p>
    {f'<p class="perk">{e(perk_line)}</p>' if perk_line else ''}
    {extra}
    <button class="btn primary add" id="add" data-name="{e(short(p))}">Add to basket</button>
    <p class="fine">Checkout is switched off because Nestling is a fictional shop.</p>
    <p class="help">Not sure about the size? Ask Nest Helper in the chat bubble, bottom right.</p>
  </div>
</div>'''
    return page(f"{short(p)} | Nestling", body, 2, f"{p['name']} at Nestling, S${p['price_sgd']}.")

# ------------------------------------------------------------------ how it works
def how():
    rows = ""
    for d in decisions:
        m = messages[d["customer_id"]]
        sent = d["action"].startswith("SEND")
        status = "Sends a reminder" if sent else "Stays quiet"
        text = e(m["message"]) if sent else e(m["why"])
        rows += (f'<tr class="{"sent" if sent else "held"}"><td data-l="Family">{d["customer_id"]}</td>'
                 f'<td data-l="Baby">{d["child_age_months"]} months</td>'
                 f'<td data-l="Decision"><span class="pill {"on" if sent else "off"}">{status}</span></td>'
                 f'<td data-l="What happens">{text}</td></tr>')
    sent_n = sum(d["action"].startswith("SEND") for d in decisions)
    body = f'''
<section class="wrap how-head"><h1>How Nest Helper decides</h1>
<p class="lede">Nest Helper doesn't blast everyone. For each family it asks: do we have permission, is there a real reason to message today, and is it safe to say? Only then does it write.</p></section>

<section class="wrap steps" aria-label="The five steps">
  <ol>
    <li><h3>Read the data</h3><p>Orders, products and each baby's age band. Birth month only, no names, photos or addresses.</p></li>
    <li><h3>Apply the rules</h3><p>A family gets at most one message: refill first, then size-up, milestone, win-back. Needs consent. Maximum one message every 7 days.</p></li>
    <li><h3>Write and answer with AI</h3><p>Nest Helper drafts the message for that baby and answers questions in the chat, in the language the parent writes in.</p></li>
    <li><h3>Check the guardrails</h3><p>Every message is blocked if it breaks a rule: no formula promotion, no pressure, no health advice, no personal data, must say it's an AI.</p></li>
    <li><h3>Hand over to a person</h3><p>HUMAN, a complaint, a refund or a safety question goes straight to the Nestling team with the chat attached.</p></li>
  </ol>
</section>

<section class="wrap table-sec"><div class="tab-head"><h2>Today's decisions for 20 families</h2>
<label class="toggle"><input type="checkbox" id="only-held"> Show only who stays quiet</label></div>
<p class="sub">{sent_n} of 20 families get a message. The other {20 - sent_n} are held back, and the reason is shown. This is the output of <code>segment_engine.py</code> and <code>compose_messages.py</code>.</p>
<div class="tbl-wrap"><table id="tbl"><thead><tr><th>Family</th><th>Baby</th><th>Decision</th><th>What happens</th></tr></thead><tbody>{rows}</tbody></table></div></section>

<section class="wrap real"><h2>What is real, and what is simulated</h2>
<div class="two">
<div><h3>Real</h3><ul><li>The decision engine and its rules</li><li>The chatbot, buttons and quick replies in MantaGO</li><li>The AI that answers questions, with its safety rules</li><li>Human handover</li><li>The tracking links on every button (you'll see "You came from Nest Helper" on a product page)</li></ul></div>
<div><h3>Simulated</h3><ul><li>The shop, customers and orders are invented</li><li>We run the engine by hand, and a reminder appears in the chat when you pick a family, because we aren't connected to a real messaging account</li><li>Checkout is switched off</li></ul></div>
</div></section>'''
    return page("How Nest Helper works | Nestling", body, 1,
                "How Nestling's AI assistant decides who to message, what to say and when to stay quiet.", "how")

# ------------------------------------------------------------------ assets
CSS = r'''
:root{--milk:#F7F8FC;--ink:#1F2147;--ink2:#4B4E78;--sky:#CFE0FF;--butter:#FFE49A;--mint:#BDE7D3;--rose:#FFCFD6;--lilac:#DCD3FF;--line:#DDE1EE;--white:#fff;--r:18px}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--milk);color:var(--ink);font:400 17px/1.6 "Figtree",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:"Bricolage Grotesque","Figtree",sans-serif;line-height:1.08;margin:0;letter-spacing:-.02em;font-weight:800}
h1{font-size:clamp(2.6rem,6.4vw,5rem)}h2{font-size:clamp(1.8rem,3.4vw,2.6rem)}h3{font-size:1.2rem;font-weight:700}
p{margin:0 0 1em}a{color:inherit}
.wrap{max-width:1160px;margin:0 auto;padding:0 20px}
.skip{position:absolute;left:-999px;top:8px;background:var(--ink);color:#fff;padding:8px 14px;border-radius:8px;z-index:99}.skip:focus{left:8px}
:focus-visible{outline:3px solid #3B5BDB;outline-offset:3px;border-radius:6px}
.top{position:sticky;top:0;background:rgba(247,248,252,.92);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);z-index:20}
.bar{display:flex;align-items:center;justify-content:space-between;height:66px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;font:800 1.45rem "Bricolage Grotesque",sans-serif;letter-spacing:-.02em}
.brand.small{font-size:1.2rem;margin-bottom:8px}
nav{display:flex;gap:22px;white-space:nowrap;align-items:center;font-weight:600;font-size:.98rem}
nav a{text-decoration:none;padding:6px 2px;border-bottom:2px solid transparent}nav a:hover,nav a[aria-current]{border-color:var(--ink)}
.basket b{display:inline-grid;place-items:center;min-width:24px;height:24px;border-radius:12px;background:var(--ink);color:#fff;font-size:.8rem;margin-left:4px;padding:0 6px}
.btn{display:inline-block;border:2px solid var(--ink);border-radius:999px;padding:12px 24px;font:700 1rem "Figtree",sans-serif;text-decoration:none;background:transparent;color:var(--ink);cursor:pointer;transition:transform .15s}
.btn:hover{transform:translateY(-2px)}.btn.primary{background:var(--ink);color:#fff}
.hero{padding:56px 0 70px;background:linear-gradient(180deg,var(--sky) 0,var(--milk) 100%)}
.hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:48px;align-items:center}
.lede{font-size:1.18rem;max-width:34em;margin:22px 0 28px;color:var(--ink2)}
.cta-row{display:flex;gap:12px;flex-wrap:wrap}.hint{margin-top:22px;font-size:.95rem;color:var(--ink2)}
.thread{background:var(--white);border-radius:28px;padding:22px;box-shadow:0 24px 60px -24px rgba(31,33,71,.35);max-width:460px;justify-self:end;width:100%}
.who{font-size:.85rem;font-weight:600;color:var(--ink2);margin-bottom:12px}
.bub{background:var(--milk);border-radius:6px 18px 18px 18px;padding:11px 15px;margin-bottom:8px;font-size:.98rem;max-width:92%}
.msgcard{display:grid;grid-template-columns:84px 1fr;gap:12px;background:var(--milk);border-radius:6px 18px 18px 18px;padding:10px;margin-bottom:10px}
.mc-art svg{width:84px;height:84px;border-radius:12px;display:block}
.mc-body{display:flex;flex-wrap:wrap;gap:6px;align-content:flex-start;font-size:.92rem}.mc-body b,.mc-body span{flex:0 0 100%}.mc-body span{color:var(--ink2);margin-bottom:4px}
.mbtn{background:var(--ink);color:#fff;text-decoration:none;border-radius:999px;padding:6px 14px;font-weight:700;font-size:.88rem}.mbtn.ghost{background:transparent;color:var(--ink);border:2px solid var(--ink);padding:4px 12px}
.qr{display:flex;gap:6px;flex-wrap:wrap}.qr span,.qr button{border:1.5px solid var(--ink);border-radius:999px;padding:5px 12px;font:600 .85rem "Figtree",sans-serif;background:transparent;color:var(--ink)}
.qr button{background:var(--butter);cursor:pointer}.qr button:hover{filter:brightness(.96)}
.why{margin-top:12px;background:var(--butter);border-radius:14px;padding:12px 14px;font-size:.92rem;line-height:1.5}
@media (prefers-reduced-motion:no-preference){.thread>*{animation:pop .5s both}.thread>.b1{animation-delay:.15s}.thread>.b2{animation-delay:.45s}.thread>.b3{animation-delay:.8s}.thread>.b4{animation-delay:1.1s}
@keyframes pop{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}}
.shop{padding-top:56px}.shop-head{display:flex;justify-content:space-between;align-items:end;gap:18px;flex-wrap:wrap;margin-bottom:24px}
.chips{display:flex;gap:8px;flex-wrap:wrap}.chip{border:1.5px solid var(--line);background:var(--white);border-radius:999px;padding:8px 16px;font:600 .92rem "Figtree",sans-serif;cursor:pointer;color:var(--ink)}
.chip[aria-pressed="true"]{background:var(--ink);color:#fff;border-color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:20px}
.pcard{background:var(--white);border-radius:var(--r);overflow:hidden;text-decoration:none;display:flex;flex-direction:column;border:1px solid var(--line);transition:transform .18s,box-shadow .18s}
.pcard:hover{transform:translateY(-4px);box-shadow:0 14px 30px -16px rgba(31,33,71,.4)}.pcard[hidden]{display:none}
.art svg{display:block;width:100%;height:auto}.pbody{padding:14px 16px 18px}.pbody h3{font-size:1.05rem}.meta{color:var(--ink2);font-size:.9rem;margin:4px 0 8px}.price{font-weight:700;margin:0}
.promises{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;padding-top:80px;padding-bottom:80px}.promises p{color:var(--ink2);margin-top:8px}
.crumbs{padding-top:22px;font-size:.92rem;color:var(--ink2)}.crumbs a{color:var(--ink2)}
.pdp{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:48px;padding-top:22px;padding-bottom:90px;align-items:start}
.pdp-art svg{width:100%;height:auto;border-radius:24px;display:block}.pdp-info h1{font-size:clamp(2rem,4vw,3rem)}
.big-price{font:800 2rem "Bricolage Grotesque",sans-serif;margin:6px 0 16px}.perk{background:var(--butter);display:inline-block;padding:6px 14px;border-radius:999px;font-weight:600;font-size:.95rem}
.note{background:var(--white);border:1px solid var(--line);border-radius:12px;padding:12px 14px;font-size:.95rem}
.add{margin:14px 0 6px}.fine{font-size:.85rem;color:var(--ink2)}.help{margin-top:20px;color:var(--ink2)}
.from{background:var(--mint);border-radius:12px;padding:9px 14px;font-weight:600;font-size:.95rem;margin-bottom:14px}
.foot{background:var(--ink);color:#E7E9F8;padding:44px 0 36px;margin-top:20px}.foot .wrap{display:grid;grid-template-columns:1fr 1fr;gap:28px}.foot .brand{color:#fff}.foot p{color:#C9CDEA;font-size:.95rem}.foot .fine{grid-column:1/-1;border-top:1px solid #3A3D6E;padding-top:18px;margin:0}.foot a{color:#fff}
.toast{position:fixed;left:50%;bottom:28px;transform:translate(-50%,30px);background:var(--ink);color:#fff;padding:12px 20px;border-radius:999px;opacity:0;pointer-events:none;transition:.25s;z-index:60;font-weight:600}.toast.on{opacity:1;transform:translate(-50%,0)}
.how-head{padding-top:56px}.how-head .lede{max-width:40em}
.steps ol{list-style:none;counter-reset:s;display:grid;grid-template-columns:repeat(5,1fr);gap:16px;padding:0;margin:48px 0}
.steps li{counter-increment:s;background:var(--white);border:1px solid var(--line);border-radius:var(--r);padding:20px 18px}
.steps li::before{content:counter(s);display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:var(--butter);font:800 1rem "Bricolage Grotesque",sans-serif;margin-bottom:12px}
.steps li:nth-child(2)::before{background:var(--sky)}.steps li:nth-child(3)::before{background:var(--mint)}.steps li:nth-child(4)::before{background:var(--rose)}.steps li:nth-child(5)::before{background:var(--lilac)}
.steps p{font-size:.95rem;color:var(--ink2);margin:8px 0 0}
.table-sec{padding-top:24px}.tab-head{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;align-items:end}.sub{color:var(--ink2);max-width:46em;margin-top:8px}
code{background:#E9ECF6;padding:1px 6px;border-radius:6px;font-size:.9em}.toggle{font-weight:600;cursor:pointer}
.tbl-wrap{overflow-x:auto;background:var(--white);border:1px solid var(--line);border-radius:var(--r)}
table{border-collapse:collapse;width:100%;min-width:640px}th,td{text-align:left;padding:13px 16px;border-bottom:1px solid var(--line);vertical-align:top;font-size:.95rem}th{font-size:.88rem;color:var(--ink2);font-weight:600}tr:last-child td{border-bottom:0}
td:first-child{font-weight:700;white-space:nowrap}.pill{display:inline-block;padding:3px 12px;border-radius:999px;font-weight:700;font-size:.85rem;white-space:nowrap}.pill.on{background:var(--mint)}.pill.off{background:var(--rose)}
tr.held td:nth-child(4){color:var(--ink2)}
.real{padding-top:70px;padding-bottom:90px}.two{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:20px}.two>div{background:var(--white);border:1px solid var(--line);border-radius:var(--r);padding:22px}.two ul{margin:10px 0 0;padding-left:1.1em}.two li{margin-bottom:6px}
@media (max-width:900px){.hero-grid,.pdp,.two,.promises,.foot .wrap{grid-template-columns:1fr}.thread{justify-self:start}.steps ol{grid-template-columns:1fr 1fr}.nav-hide{display:none}}
@media (max-width:560px){nav{gap:12px;font-size:.9rem}.steps ol{grid-template-columns:1fr}.hero{padding-top:36px}}
'''

JS = r'''
(function(){
  var $=function(s,r){return (r||document).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
  var mem=0;
  function getCount(){try{return parseInt(localStorage.getItem('nestling-basket')||'0',10)||0}catch(e){return mem}}
  function setCount(n){mem=n;try{localStorage.setItem('nestling-basket',String(n))}catch(e){}var c=$('#basket-count');if(c)c.textContent=n}
  setCount(getCount());
  var tt;function toast(t){var el=$('#toast');if(!el)return;el.textContent=t;el.classList.add('on');clearTimeout(tt);tt=setTimeout(function(){el.classList.remove('on')},2600)}
  // add to basket
  var add=$('#add');if(add)add.addEventListener('click',function(){setCount(getCount()+1);toast(add.dataset.name+' added. Checkout is switched off: Nestling is a fictional shop.')});
  // filters
  var chips=$$('.chip');
  function applyFilter(k){chips.forEach(function(c){c.setAttribute('aria-pressed',c.dataset.filter===k?'true':'false')});$$('.pcard').forEach(function(p){p.hidden=!(k==='all'||p.dataset.cat===k)})}
  chips.forEach(function(c){c.addEventListener('click',function(){applyFilter(c.dataset.filter)})});
  var h=(location.hash||'').replace('#','');if(chips.length&&h&&chips.some(function(c){return c.dataset.filter===h}))applyFilter(h);
  // "why this message" in the hero
  var wb=$('#why-btn');if(wb)wb.addEventListener('click',function(){var p=$('#why-panel'),o=p.hidden;p.hidden=!o;wb.setAttribute('aria-expanded',String(o))});
  // arrived from a Nest Helper link
  var from=$('#from');if(from){var q=new URLSearchParams(location.search),m=q.get('utm_medium'),s=q.get('utm_source');
    var map={refill:'a refill reminder',sizeup:'a size-up reminder',milestone:'a milestone message',winback:'a welcome-back message',reorder:'your reorder'};
    if(s==='livechat'&&m){from.hidden=false;from.textContent='You came from Nest Helper ('+(map[m]||m)+').'}}
  // only-held toggle
  var oh=$('#only-held');if(oh)oh.addEventListener('change',function(){$$('#tbl tbody tr.sent').forEach(function(r){r.hidden=oh.checked})});
})();
'''

def build():
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "assets"))
    # the MantaGO chat embed, taken unchanged from the original page
    src = open(os.path.join(ROOT, "demo", "demo_page.html"), encoding="utf-8").read()
    m = re.search(r"<script>(function b\(c,d\).*?)</script>", src, re.S)
    assert m, "chat embed not found in demo/demo_page.html"
    open(os.path.join(SITE, "assets", "chat.js"), "w", encoding="utf-8").write(m.group(1))
    open(os.path.join(SITE, "assets", "style.css"), "w", encoding="utf-8").write(CSS)
    open(os.path.join(SITE, "assets", "site.js"), "w", encoding="utf-8").write(JS)
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(home())
    os.makedirs(os.path.join(SITE, "how-it-works"))
    open(os.path.join(SITE, "how-it-works", "index.html"), "w", encoding="utf-8").write(how())
    for p in products:
        d = os.path.join(SITE, "shop", slug(p)); os.makedirs(d)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(product_page(p))
    open(os.path.join(SITE, ".nojekyll"), "w").close()
    print("Built", sum(len(fs) for _, _, fs in os.walk(SITE)), "files in", SITE)

if __name__ == "__main__":
    build()
