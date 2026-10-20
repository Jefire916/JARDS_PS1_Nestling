"""
Nestling message composer + guardrail checker (JARDS, AI-GNITION 2026).

Step 2 after segment_engine.py. For every customer the engine decided to message,
this writes the exact reminder text and a plain-words "why you got this" line,
then runs every message through the guardrails before it is allowed out.

Reads : output/decisions.csv, data/products.csv
Writes: output/messages.csv           one row per customer: message, why, guardrail result
        output/guardrail_tests.csv    bad messages the guardrails must catch (proof they work)

How it maps to production:
  - Today the wording comes from fixed templates filled with each customer's data.
  - In a live shop an LLM would draft the wording instead. The guardrail step below
    stays exactly the same, so a bad draft can never be sent.

Run:  python3 engine/compose_messages.py
"""
import csv, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA, OUT = os.path.join(ROOT, "data"), os.path.join(ROOT, "output")

with open(os.path.join(DATA, "products.csv"), newline="") as f:
    products = {r["item_id"]: r for r in csv.DictReader(f)}
with open(os.path.join(OUT, "decisions.csv"), newline="") as f:
    decisions = list(csv.DictReader(f))

def short(iid):
    """Product name without pack count or size noise, e.g. 'Diapers Size 3'."""
    p = products[iid]
    n = re.sub(r"\s*\(\d+\)\s*$", "", p["name"])
    if p["category"] in ("formula_infant", "milk_growing_up"):
        n = re.sub(r"\s*\(fictional brand\)", "", n)
        n = re.sub(r"\s+800g$", "", n)
        n = re.sub(r"\s+\d+(-\d+)?[MY]$", "", n)
    return n

def months(n):
    return f"{n} month" + ("" if n == 1 else "s")

# ------------------------------------------------------------------ guardrails
PRESSURE = r"last chance|hurry|only today|limited (time|stock)|don'?t miss|act now|urgent|expires? (soon|today)|running out fast|selling out"
OFFER_WORDS = r"save|discount|offer|free|%|bundle|promo|deal|voucher|coupon|reward"
PII = r"@|\d{6,}|born on|birthday is|\bmy name\b"

def guardrail(message, offer_items, journey):
    """Return list of problems. Empty list = pass."""
    problems = []
    m = message.lower()
    ids = [i for i in re.findall(r"[A-Z]{2}-[A-Z0-9]+(?:-[A-Z0-9]+)*", offer_items or "") if i in products]
    # 1. Infant formula and milk: we never start a message about infant formula,
    #    and milk is only ever a plain reorder reminder with no offer wording.
    for iid in ids:
        cat = products[iid]["category"]
        if cat == "formula_infant":
            problems.append("proactive infant formula message (SIFECS)")
        if cat in ("formula_infant", "milk_growing_up"):
            if journey != "REFILL":
                problems.append("formula/milk used outside a plain reorder reminder")
            if re.search(OFFER_WORDS, m):
                problems.append("offer wording next to formula/milk (SIFECS)")
    # 2. No pressure tactics
    if re.search(PRESSURE, m):
        problems.append("pressure wording")
    # 3. No personal data
    if re.search(PII, m):
        problems.append("looks like personal data")
    # 4. Must say who is talking, and stay short
    if "nest helper" not in m:
        problems.append("does not say it is Nest Helper")
    if len(message) > 320:
        problems.append("too long (over 320 characters)")
    # 5. No health or feeding advice
    if re.search(r"rash|allerg|safe to sleep|dose|feeding advice|should (feed|breastfeed)", m):
        problems.append("health or feeding advice")
    return problems

# ------------------------------------------------------------------ wording
def compose(row):
    j, age, offer = row["journey"], int(row["child_age_months"]), row["offer"]
    hi = "Hi! It's Nest Helper from Nestling."
    why_tail = "You said yes to reminders. I don't use your name, photos or address. Type STOP any time."
    if j == "REFILL":
        parts = [p.strip() for p in offer.split(",")]
        lines, why = [], []
        for p in parts:
            if "->" in p:
                old, new = p.split("->")
                lines.append(f"Your {short(old)} should be running out around now. At {months(age)}, lots of babies move up to {short(new)}, so I've put both below.")
                why.append(f"We predicted when {short(old)} runs out from how often you reorder it, and checked the size against your baby's age ({months(age)}).")
            else:
                cat = products[p]["category"]
                tail = " Same again, at the usual price?" if cat == "milk_growing_up" else " Want the same again?"
                lines.append(f"Your {short(p)} should be running out in the next few days.{tail}")
                why.append(f"We predicted when {short(p)} runs out from how often you reorder it.")
        text = hi + " " + (lines[0] if len(lines) == 1 else "Your " + " and ".join(short(p.split('->')[0]) for p in parts) + " should be running out around now. Want the same again?")
        return text, " ".join(why) + " " + why_tail
    if j == "SIZE_UP":
        nxt = short(offer)
        text = f"{hi} Your little one is about {months(age)}, and clothes in the last size usually get snug around now. How's the fit? The {nxt} has the next size ready."
        why = f"Your baby's age band ({months(age)}) and the clothing size you bought last tell us when the next size is usually needed. " + why_tail
        return text, why
    if j == "MILESTONE":
        nxt = short(offer)
        if age == 12:
            text = f"{hi} Happy first-birthday month to your little one! 🎂 Free delivery on your next order in the next 7 days, and the {nxt} is ready if you want it."
        else:
            text = f"{hi} Half a year already! 🎉 Free delivery on your next order in the next 7 days, and the {nxt} is ready if you want it."
        why = f"Your baby turns {months(age)} this month, so this is a milestone message. " + why_tail
        return text, why
    if j == "WIN_BACK":
        nxt = short(offer)
        text = f"{hi} It's been a while, and we've missed you! Your little one is probably in {products[offer]['size']} sizes by now. Free delivery on your next order in the next 14 days, and the {nxt} is ready."
        why = f"You've ordered before, but not for a while, and your baby's age band suggests new sizes. " + why_tail
        return text, why
    raise ValueError(j)

# ------------------------------------------------------------------ run
rows = []
for d in decisions:
    if not d["action"].startswith("SEND"):
        rows.append({"customer_id": d["customer_id"], "journey": d["journey"], "pack": "", "message": "",
                     "why": "Not messaged: " + d["reason"], "guardrail": "n/a (nothing sent)"})
        continue
    text, why = compose(d)
    probs = guardrail(text, d["offer"], d["journey"])
    rows.append({"customer_id": d["customer_id"], "journey": d["journey"], "pack": d["action"].replace("SEND ", ""),
                 "message": text if not probs else "", "why": why,
                 "guardrail": "PASS" if not probs else "BLOCKED: " + "; ".join(probs)})

with open(os.path.join(OUT, "messages.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# Proof the guardrails work: messages that MUST be blocked
tests = [
    ("Formula discount", "Hi! It's Nest Helper. Save 10% on Infant Formula Stage 1 today!", "FM-1", "REFILL", True),
    ("Starting a formula message", "Hi! It's Nest Helper. Time to restock your formula.", "FM-1", "REFILL", True),
    ("Pressure", "Hi! It's Nest Helper. Last chance, hurry before it sells out!", "DP-3", "REFILL", True),
    ("Personal data", "Hi! It's Nest Helper. Happy birthday Aarav, born on 3 Oct, we know you live at 12 Elm Road 560123.", "DP-3", "REFILL", True),
    ("Health advice", "Hi! It's Nest Helper. That rash is probably an allergy, try a new cream.", "DP-3", "REFILL", True),
    ("Pretends to be human", "Hi! It's Sarah from Nestling. Your diapers are due.", "DP-3", "REFILL", True),
    ("Milk with an offer", "Hi! It's Nest Helper. Growing-up Milk Stage 3 is on offer, save 15%!", "GM-3", "REFILL", True),
    ("A normal good message", "Hi! It's Nest Helper from Nestling. Your Diapers Size 3 should be running out in the next few days. Want the same again?", "DP-3", "REFILL", False),
]
ok_all = True
with open(os.path.join(OUT, "guardrail_tests.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["test", "should_be_blocked", "result", "reasons"])
    for name, msg, off, j, must_block in tests:
        p = guardrail(msg, off, j)
        good = bool(p) == must_block
        ok_all &= good
        w.writerow([name, "yes" if must_block else "no", "blocked" if p else "passed", "; ".join(p)])

sent = [r for r in rows if r["pack"]]
print(f"Messages written: {len(sent)} sent-ready, {len(rows) - len(sent)} held back")
print(f"Guardrails: {sum(r['guardrail'] == 'PASS' for r in sent)}/{len(sent)} passed")
print("Guardrail self-test:", "ALL CORRECT" if ok_all else "SOMETHING IS WRONG")
