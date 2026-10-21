"""
Builds the parts of the Nestling website that come from our data (JARDS, AI-GNITION 2026).

The look (styles.css, store.css, home page, store page) is Reyansh's design.
This script adds, in that same design:
  shop/<product>/index.html   one page per product (the Nest Helper bot links here)
  OurStory.html               how Nest Helper works, today's decisions, real vs simulated, contact
  how-it-works/index.html     old address, forwards to OurStory.html
  assets/product.js           cart + "You came from Nest Helper" banner on product pages

Reads : data/products.csv, output/decisions.csv, output/messages.csv
Run   : python3 engine/build_site.py <site folder>     (default: docs)
"""
import csv, os, sys, html, re
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(ROOT, "docs")
e = html.escape

def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

products = read(os.path.join(ROOT, "data", "products.csv"))
for p in products:
    p["slug"] = p["url"].rstrip("/").split("/")[-1]
    p["price"] = int(p["price_sgd"])
    p["name"] = re.sub(r" \d+-\d+[MY] 800g \(fictional brand\)", " (800g)", p["name"])

UNSPLASH = "https://images.unsplash.com/photo-{}?q=80&w=1000&auto=format&fit=crop"
PHOTO = {
    "clothing": (UNSPLASH.format("1622290319146-7b63df48a635"), "A white baby bodysuit laid flat"),
    "diapers": (UNSPLASH.format("1504151806752-5b3af8e39e4e"), "A baby in a diaper on a white blanket"),
    "wipes": (UNSPLASH.format("1504151806752-5b3af8e39e4e"), "A baby in a diaper on a white blanket"),
    "bundle": (UNSPLASH.format("1555252333-9f8e92e65df9"), "A baby's feet in a soft white towel"),
    "toys": (UNSPLASH.format("1596461404969-9ae70f2830c1"), "A wooden toy train set"),
    "playmat": (UNSPLASH.format("1593793373220-2e51e1c31385"), "A baby lying on a play mat"),
}
FORMULA_ART = {"FM-1": "formula-1.svg", "FM-2": "formula-2.svg", "GM-3": "milk-3.svg"}
WEIGHT = {"DP-NB": "up to 5 kg", "DP-1": "3 to 6 kg", "DP-2": "5 to 8 kg", "DP-3": "7 to 11 kg", "DP-4": "9 to 14 kg"}
STORE_CAT = {"clothing": "bodysuits", "bundle": "bundles", "diapers": "diapers", "wipes": "diapers",
             "toys": "toys", "formula_infant": "formula", "milk_growing_up": "formula"}
CAT_NAME = {"bodysuits": "Baby Clothing", "bundles": "Stage Bundles", "diapers": "Diapers & Water Wipes",
            "toys": "Toys", "formula": "Formula & Milk"}
LADDERS = [["DP-NB", "DP-1", "DP-2", "DP-3", "DP-4"],
           ["CL-NB", "CL-0-3", "CL-3-6", "CL-6-9", "CL-9-12", "CL-12-18"],
           ["BN-0-3", "BN-3-6", "BN-6-9", "BN-9-12", "BN-12-18"]]
by_id = {p["item_id"]: p for p in products}

def age_text(p):
    lo, hi = int(p["min_age_m"]), int(p["max_age_m"])
    if hi == 1:
        return "newborn, up to 1 month"
    if lo == 12 and hi == 36 and p["category"] == "milk_growing_up":
        return "1 to 3 years"
    if hi >= 36 and lo > 0:
        return f"from {lo} months"
    if hi >= 36:
        return "newborn to 3 years"
    if lo >= 12:
        return f"{lo // 12} to {hi // 12} years" if hi % 12 == 0 and hi > 12 else f"{lo} to {hi} months"
    return f"{lo} to {hi} months"

def is_mat(p): return p["item_id"] == "TY-PM"

def image(p):
    if p["item_id"] in FORMULA_ART:
        return "../../assets/" + FORMULA_ART[p["item_id"]], "Plain illustration of a milk tin"
    return PHOTO["playmat" if is_mat(p) else p["category"]]

def badge(p):
    c, s = p["category"], p["size"]
    if c == "diapers":
        return "Newborn" if s == "NB" else "Size " + s[1:]
    if c in ("clothing", "bundle"):
        return s
    if c == "toys" and p["collection_piece"]:
        return f"Set {p['collection_piece']} of 4"
    return ""

def desc(p):
    c = p["category"]
    if c == "diapers":
        return (f"Gentle, absorbent diapers for babies {age_text(p)} ({WEIGHT[p['item_id']]}). One pack lasts most "
                f"families about {p['pack_days']} days. If it leaks or leaves red marks, try the next size up.")
    if c == "wipes":
        return f"Soft water wipes, gentle on skin. One pack lasts most families about {p['pack_days']} days."
    if c == "clothing":
        return f"Soft cotton, for babies {age_text(p)}. Between sizes? Pick the larger one."
    if c == "bundle":
        return (f"Everything for the next stage in one tap: clothes, a sleepsuit and diapers in the right size, "
                f"for babies {age_text(p)}.")
    if is_mat(p):
        return f"A soft, cushioned, wipe-clean floor mat for tummy time and crawling, {age_text(p)}."
    if c == "toys":
        return f"Piece {p['collection_piece']} of 4 in our Sensory Set, for babies {age_text(p)}. Collect all 4!"
    return ("800g tin, fictional brand. Sold at our usual price. Nestling doesn't recommend brands, compare formulas "
            "or give feeding advice, so please ask your doctor or nurse.")

def perk(p):
    c = p["category"]
    if c in ("diapers", "wipes"):
        return '<p class="perk">Buy 3 of the same pack and save 10%.</p>'
    if c == "bundle":
        return '<p class="perk">Free delivery and free size exchange within 30 days.</p>'
    if c == "clothing":
        return '<p class="perk">Free size exchange within 30 days (unworn, with tags).</p>'
    if c in ("formula_infant", "milk_growing_up"):
        return '<p class="perk no-offer">No offers apply to formula or milk (Singapore SIFECS code).</p>'
    return ""

def next_size(p):
    for lad in LADDERS:
        if p["item_id"] in lad:
            i = lad.index(p["item_id"])
            if i + 1 < len(lad):
                n = by_id[lad[i + 1]]
                return f'<p class="next-size">Growing fast? Next size up: <a href="../{n["slug"]}/index.html">{e(n["name"])}</a></p>'
    return ""

def help_line(p):
    if p["category"] in ("formula_infant", "milk_growing_up"):
        return ('<p class="help-line">Questions about feeding? Please speak to a doctor, nurse or healthcare professional. '
                'For an order question, type <b>HUMAN</b> in the chat bubble to reach our team.</p>')
    return '<p class="help-line">Not sure about the size? Ask Nest Helper in the chat bubble, bottom right.</p>'

NAV = """    <div class="parent">
        <a class="btn child" href="{r}index.html">Home</a>
        <a class="btn child" href="{r}store.html"{cur_store}>Store (Cart: <span id="cart-count">0</span>)</a>
        <a class="btn child" href="{r}OurStory.html"{cur_how}>How it works</a>
        <a class="btn child" href="{r}OurStory.html#contact">Contact us</a>
    </div>"""
HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="icon" href="{r}assets/favicon.svg" type="image/svg+xml">
    <link rel="stylesheet" type="text/css" href="{r}{css}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&family=Sue+Ellen+Francisco&display=swap" rel="stylesheet">
</head>
<body>
"""
FOOT = """
    <div class="toast" id="toast" role="status" aria-live="polite"></div>
    <div class="LastPart">
        <div class="LinkDiv">
            <p class="copyright">Baby essentials for Singapore families, from newborn to three years.<br><br>Note: Nestling is a fictional shop created by team JARDS for AI-GNITION hackathon 2026. Nest Helper is an AI assistant. <a href="https://github.com/Jefire916/JARDS_PS1_Nestling">Source code</a></p>
        </div>
    </div>
{scripts}
</body>
</html>
"""

def product_page(p):
    r = "../../"
    img, alt = image(p)
    b = badge(p)
    cat = STORE_CAT[p["category"]] if not is_mat(p) else "toys"
    meta = [x for x in ([p["size"]] if p["category"] in ("clothing", "bundle") else []) + [age_text(p)] if x]
    if p["item_id"] in WEIGHT:
        meta.append(WEIGHT[p["item_id"]])
    stock = ""
    if p["category"] in ("diapers", "wipes"):
        stock = (f'<button class="store-btn add-btn" type="button" data-qty="3" data-id="{p["slug"]}" '
                 f'data-name="{e(p["name"])}" data-price="{p["price"]}">Add 3 packs (save 10%)</button>')
    body = f"""{NAV.format(r=r, cur_store=' aria-current="page"', cur_how='')}

    <nav class="crumbs" aria-label="Breadcrumb"><a href="{r}store.html">Store</a> / <a href="{r}store.html#{cat}">{e(CAT_NAME[cat])}</a> / {e(p["name"])}</nav>
    <div class="from-banner" id="from" hidden></div>

    <main class="pdp">
        <div class="pdp-img">
            <img src="{e(img)}" alt="{e(alt)}">
            {f'<span class="pdp-badge">{e(b)}</span>' if b else ''}
        </div>
        <div class="pdp-info">
            <h1>{e(p["name"])}</h1>
            <p class="pdp-meta">{e(" · ".join(meta))}</p>
            <p class="pdp-price">S${p["price"]}</p>
            <p>{e(desc(p))}</p>
            {perk(p)}
            <div class="pdp-actions">
                <button class="store-btn add-to-cart-btn add-btn" type="button" data-qty="1" data-id="{p["slug"]}" data-name="{e(p["name"])}" data-price="{p["price"]}">Add to Cart</button>
                {stock}
            </div>
            <p class="fine-print" style="text-align:left">Checkout is switched off: Nestling is a fictional shop.</p>
            {next_size(p)}
            {help_line(p)}
        </div>
    </main>
"""
    return (HEAD.format(title=f"{e(p['name'])} | Nestling", desc=f"{e(p['name'])} at Nestling, S${p['price']}.",
                        r=r, css="store.css") + body +
            FOOT.format(scripts=f'    <script src="{r}assets/product.js"></script>\n    <script src="{r}assets/chat.js" defer></script>'))

PRODUCT_JS = r"""(function () {
    // Cart (shared with the Store page)
    var mem = [];
    function readCart() { try { return JSON.parse(localStorage.getItem('nestling_cart')) || []; } catch (e) { return mem; } }
    function saveCart(c) { mem = c; try { localStorage.setItem('nestling_cart', JSON.stringify(c)); } catch (e) { } }
    function showCount() {
        var n = readCart().reduce(function (s, i) { return s + i.quantity; }, 0);
        var el = document.getElementById('cart-count'); if (el) el.textContent = n;
    }
    var t, toastEl = document.getElementById('toast');
    function toast(msg) { if (!toastEl) return; toastEl.textContent = msg; toastEl.classList.add('on'); clearTimeout(t); t = setTimeout(function () { toastEl.classList.remove('on'); }, 2600); }
    document.querySelectorAll('.add-btn').forEach(function (b) {
        b.addEventListener('click', function () {
            var qty = parseInt(b.dataset.qty, 10) || 1, cart = readCart(), id = b.dataset.id;
            var item = cart.filter(function (i) { return i.id === id; })[0];
            if (item) item.quantity += qty; else cart.push({ id: id, name: b.dataset.name, price: parseFloat(b.dataset.price), quantity: qty });
            saveCart(cart); showCount();
            toast((qty > 1 ? qty + ' x ' : '') + b.dataset.name + ' added to your cart!');
        });
    });
    showCount();

    // "You came from Nest Helper": shown when the page is opened from a button in the chat
    var q = new URLSearchParams(location.search), from = document.getElementById('from');
    var why = { refill: 'a refill reminder', sizeup: 'a size-up reminder', milestone: 'a milestone message', winback: 'a welcome-back message', reorder: 'your reorder' };
    if (from && q.get('utm_source') === 'livechat') {
        var m = q.get('utm_medium');
        from.textContent = 'You came from Nest Helper' + (m ? ' (' + (why[m] || m) + ')' : '') + '. Your cart is ready below.';
        from.hidden = false;
    }
})();
"""

def our_story():
    dec = read(os.path.join(ROOT, "output", "decisions.csv"))
    msg = {m["customer_id"]: m for m in read(os.path.join(ROOT, "output", "messages.csv"))}
    def hold_reason(r):
        s = r["reason"]
        if "consent" in s.lower():
            return "Never said yes to reminders"
        if "SIFECS" in s:
            return "Infant formula is due, but Nestling never starts a formula message (SIFECS). The parent can still reorder."
        if "Cooldown" in s:
            return "Already messaged this week (max one message every 7 days)"
        return "Nothing useful is due today"
    rows, sent = [], 0
    for r in dec:
        send = r["action"].startswith("SEND")
        sent += send
        age = f'{r["child_age_months"]} month' + ("" if r["child_age_months"] == "1" else "s") + (" (estimated)" if r["age_estimated"] == "Y" else "")
        what = e(msg[r["customer_id"]]["message"]) if send and r["customer_id"] in msg else e(hold_reason(r))
        tag = '<span class="tag send">Sends a reminder</span>' if send else '<span class="tag hold">Stays quiet</span>'
        rows.append(f'<tr class="{"sent" if send else "held"}"><td>{e(r["customer_id"])}</td><td>{age}</td><td>{tag}</td><td>{what}</td></tr>')
    held = len(dec) - sent
    body = f"""{NAV.format(r='', cur_store='', cur_how=' aria-current="page"')}

    <div class="title-container">
        <h1 class="site-name">How Nest Helper Works</h1>
        <p class="lead">Nest Helper doesn't message everyone. For each family it asks: do we have permission, is there a real reason to message today, and is it safe to say? Only then does it write.</p>
    </div>

    <div class="page-wrap">
        <div class="steps">
            <div class="step"><b>1</b><h3>Read the data</h3><p>Past orders, products, and each baby's birth month. No names, photos or addresses.</p></div>
            <div class="step"><b>2</b><h3>Apply the rules</h3><p>At most one message: refill first, then size-up, milestone, welcome-back. Only with consent, max one every 7 days.</p></div>
            <div class="step"><b>3</b><h3>Write the message</h3><p>A short message for that baby's stage, with the right product and a "Why this message?" button.</p></div>
            <div class="step"><b>4</b><h3>Check the guardrails</h3><p>Blocked if it promotes formula, pressures, gives health advice, uses personal data or hides that it's an AI.</p></div>
            <div class="step"><b>5</b><h3>Hand over to a person</h3><p>Type HUMAN, or ask about a complaint, refund or safety, and a Nestling team member joins the same chat.</p></div>
        </div>

        <div class="title-container"><h2 class="site-name">Today's decisions for {len(dec)} families</h2></div>
        <div class="table-tools">
            <span><b>{sent} of {len(dec)}</b> families get a message. The other <b>{held}</b> are held back, and the reason is shown. (Simulated families, 20 Oct 2026.)</span>
            <label><input type="checkbox" id="only-held"> Show only who stays quiet</label>
        </div>
        <div class="table-scroll">
            <table class="decisions" id="tbl">
                <thead><tr><th>Family</th><th>Baby</th><th>Decision</th><th>What happens</th></tr></thead>
                <tbody>
                {chr(10).join(rows)}
                </tbody>
            </table>
        </div>

        <div class="title-container"><h2 class="site-name">What's real, and what's simulated</h2></div>
        <div class="two-col">
            <div class="box real"><h3>Real</h3><ul>
                <li>The decision engine and its rules</li>
                <li>The Nest Helper chatbot, buttons and quick replies in MantaGO</li>
                <li>The AI that answers questions, with its safety rules</li>
                <li>Handover to a real person</li>
                <li>Every chat button opens the right product page, tagged so you see "You came from Nest Helper"</li>
            </ul></div>
            <div class="box sim"><h3>Simulated</h3><ul>
                <li>The shop, the customers and their orders are invented</li>
                <li>We run the engine by hand. In the chat, "Meet the families" shows the reminder a family would get, because we aren't connected to a real messaging account</li>
                <li>Checkout is switched off</li>
            </ul></div>
        </div>

        <div class="title-container" id="contact"><h2 class="site-name">Contact us</h2></div>
        <div class="box contact-box">
            <p>Open the chat bubble at the bottom right of any page and tap <b>Start Chat</b>.</p>
            <p>Ask Nest Helper about sizes, products or orders. To talk to a person, type <span class="kbd">HUMAN</span> and a Nestling team member will join the same chat (Mon to Fri, 9am to 6pm).</p>
            <p>Type <span class="kbd">STOP</span> at any time to stop reminders.</p>
        </div>
    </div>
"""
    js = """    <script>
        (function () {
            var oh = document.getElementById('only-held');
            if (oh) oh.addEventListener('change', function () {
                document.querySelectorAll('#tbl tbody tr.sent').forEach(function (r) { r.hidden = oh.checked; });
            });
            var n = 0; try { n = (JSON.parse(localStorage.getItem('nestling_cart')) || []).reduce(function (s, i) { return s + i.quantity; }, 0); } catch (e) { }
            var c = document.getElementById('cart-count'); if (c) c.textContent = n;
        })();
    </script>
    <script src="assets/chat.js" defer></script>"""
    return (HEAD.format(title="How it works | Nestling", desc="How Nest Helper decides who gets a reminder, and how to contact Nestling.",
                        r="", css="styles.css") + body + FOOT.format(scripts=js).replace('<div class="toast" id="toast" role="status" aria-live="polite"></div>\n', ''))

REDIRECT = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>How it works | Nestling</title>
<meta http-equiv="refresh" content="0; url=../OurStory.html"><link rel="canonical" href="../OurStory.html"></head>
<body><p>This page moved: <a href="../OurStory.html">How Nest Helper works</a>.</p></body></html>
"""

def write(rel, text):
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

for p in products:
    write(f"shop/{p['slug']}/index.html", product_page(p))
write("assets/product.js", PRODUCT_JS)
write("OurStory.html", our_story())
write("how-it-works/index.html", REDIRECT)
print(f"Built {len(products)} product pages, OurStory.html and how-it-works redirect in {SITE}")
