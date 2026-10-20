"""
Nestling segment engine (JARDS, AI-GNITION 2026).
Customer data and decision engine lead: Devanshi.

Reads fictional customers, orders and products, decides for every customer
whether the bot should message them, which journey, which exact product, and why.
Outputs:
  output/decisions.csv          one row per customer, with the reason
  output/broadcast_groups.csv   one row per message pack -> who receives it
  output/mantago_items_import.csv  product list in MantaGO's import columns
  output/report.md              human-readable summary

Run:  python3 engine/segment_engine.py            (as-of date 2026-10-20)
      python3 engine/segment_engine.py 2026-10-25 (any other date)
"""
import csv, sys, os
from datetime import date, timedelta
from statistics import median
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA, OUT = os.path.join(ROOT, "data"), os.path.join(ROOT, "output")
ASOF = date.fromisoformat(sys.argv[1]) if len(sys.argv) > 1 else date(2026, 10, 20)

# ---------------- rules (change numbers here, nowhere else) ----------------
REFILL_WINDOW = (-2, 3)        # message when predicted run-out is 2 days ago .. 3 days ahead
REFILL_CATS = {"diapers", "wipes", "milk_growing_up"}
WINBACK_DAYS = 60              # repeat buyer quiet for 60+ days
MILESTONE_AGES = {6, 12}       # 6 months, first birthday month
COOLDOWN_DAYS = 7              # max one bot-started message per customer per 7 days
PRIORITY = ["REFILL", "SIZE_UP", "MILESTONE", "WIN_BACK"]
CLOTHING_CATS = {"clothing", "bundle"}
SIZE_BANDS = ["NB", "0-3M", "3-6M", "6-9M", "9-12M", "12-18M"]
DIAPER_LADDER = ["DP-NB", "DP-1", "DP-2", "DP-3", "DP-4"]
BUNDLE_FOR = {"NB": "BN-0-3", "0-3M": "BN-3-6", "3-6M": "BN-6-9", "6-9M": "BN-9-12", "9-12M": "BN-12-18"}
# ---------------------------------------------------------------------------

def read(name):
    with open(os.path.join(DATA, name), newline="") as f:
        return list(csv.DictReader(f))

products = {p["item_id"]: p for p in read("products.csv")}
customers = read("customers.csv")
orders = read("orders.csv")
for o in orders:
    o["date"] = date.fromisoformat(o["order_date"]); o["qty"] = int(o["qty"])
by_cust = defaultdict(list)
for o in orders:
    by_cust[o["customer_id"]].append(o)

def months_between(d1, d2):
    return (d2.year - d1.year) * 12 + (d2.month - d1.month) - (1 if d2.day < d1.day else 0)

def child_age(c, olist):
    """Age in whole months. Uses birth month if given; otherwise estimates it from
    the most recent sized item bought (midpoint of that size band + time since)."""
    if c["child_birth_month"]:
        y, m = map(int, c["child_birth_month"].split("-"))
        return (ASOF.year - y) * 12 + (ASOF.month - m), False
    sized = [o for o in olist if products[o["item_id"]]["category"] in CLOTHING_CATS | {"diapers"}]
    if not sized:
        return None, True
    last = max(sized, key=lambda o: o["date"])
    p = products[last["item_id"]]
    mid = (float(p["min_age_m"]) + float(p["max_age_m"])) / 2
    return int(mid + months_between(last["date"], ASOF)), True

def refill_due(olist):
    """For each consumable item the customer buys, predict run-out date from their
    own reorder gaps (median), or from pack_days x qty if they bought it only once."""
    due, excluded = [], []
    items = defaultdict(list)
    for o in olist:
        items[o["item_id"]].append(o)
    for iid, lst in items.items():
        p = products[iid]
        if p["category"] not in REFILL_CATS | {"formula_infant"}:
            continue
        lst.sort(key=lambda o: o["date"])
        last = lst[-1]
        if len(lst) >= 2:
            gap = median((b["date"] - a["date"]).days for a, b in zip(lst, lst[1:]))
            gap = gap * last["qty"]
        else:
            gap = int(p["pack_days"]) * last["qty"]
        runout = last["date"] + timedelta(days=round(gap))
        delta = (runout - ASOF).days
        if REFILL_WINDOW[0] <= delta <= REFILL_WINDOW[1]:
            (excluded if p["category"] == "formula_infant" else due).append((iid, runout))
    return due, excluded

def diaper_upgrade(iid, age):
    if iid not in DIAPER_LADDER or age is None:
        return None
    i = DIAPER_LADDER.index(iid)
    if i + 1 < len(DIAPER_LADDER) and age >= float(products[DIAPER_LADDER[i + 1]]["min_age_m"]):
        return DIAPER_LADDER[i + 1]
    return None

def stage_bundle_for_age(age):
    for iid in ["BN-0-3", "BN-3-6", "BN-6-9", "BN-9-12", "BN-12-18"]:
        if age < float(products[iid]["max_age_m"]):
            return iid
    return "BN-12-18"

decisions, groups = [], defaultdict(list)
for c in customers:
    cid, olist = c["customer_id"], by_cust.get(c["customer_id"], [])
    age, estimated = child_age(c, olist)
    last_order = max((o["date"] for o in olist), default=None)
    days_since = (ASOF - last_order).days if last_order else None
    n_orders = len({o["order_id"] for o in olist})
    matched, offer, notes = {}, {}, []

    # 1. REFILL
    due, excl = refill_due(olist)
    for iid, _ in excl:
        notes.append(f"{iid} due but infant formula: no proactive message (SIFECS 6.1/6.3)")
    if due:
        recs = []
        for iid, _ in sorted(due):
            up = diaper_upgrade(iid, age)
            recs.append(f"{iid}->{up}" if up else iid)
        matched["REFILL"] = "RF-" + "+".join(r.replace("DP-", "DP").replace("WP-", "WP").replace("GM-", "GM").replace("->", "-UP-") for r in recs)
        offer["REFILL"] = ", ".join(recs)

    # 2. SIZE_UP (clothing)
    cl = [o for o in olist if products[o["item_id"]]["category"] in CLOTHING_CATS]
    if cl and age is not None:
        last_cl = products[max(cl, key=lambda o: o["date"])["item_id"]]
        mx = float(last_cl["max_age_m"])
        if mx - 1 <= age <= mx + 1 and last_cl["size"] in BUNDLE_FOR:
            nxt = BUNDLE_FOR[last_cl["size"]]
            matched["SIZE_UP"] = f"SU-{last_cl['size']}-TO-{products[nxt]['size']}"
            offer["SIZE_UP"] = nxt

    # 3. MILESTONE (6 or 12 months): thank-you free delivery plus the stage bundle for the next age band
    if age in MILESTONE_AGES and n_orders >= 1:
        matched["MILESTONE"] = f"MS-{age}M"
        offer["MILESTONE"] = stage_bundle_for_age(age + 1)

    # 4. WIN_BACK
    if n_orders >= 2 and days_since is not None and days_since >= WINBACK_DAYS:
        b = stage_bundle_for_age(age + 1) if age is not None else "BN-12-18"
        matched["WIN_BACK"] = f"WB-{products[b]['size']}"
        offer["WIN_BACK"] = b

    journey = next((j for j in PRIORITY if j in matched), None)
    last_msg = c["last_bot_message_date"]
    if journey is None:
        action, reason = "NO MESSAGE", "No rule matches"
    elif c["reminder_consent"] != "Y":
        action, reason = "NO MESSAGE", "No reminder consent"
    elif last_msg and (ASOF - date.fromisoformat(last_msg)).days < COOLDOWN_DAYS:
        action, reason = "NO MESSAGE", f"Cooldown: bot messaged on {last_msg}"
    else:
        action = "SEND " + matched[journey]
        reason = "Matched " + " + ".join(j for j in PRIORITY if j in matched)
        if len(matched) > 1:
            reason += f"; priority picks {journey}, others wait for next cycle"
        groups[matched[journey]].append(c)
    if notes:
        reason += "; " + "; ".join(notes)

    decisions.append({
        "customer_id": cid, "child_age_months": "" if age is None else age,
        "age_estimated": "Y" if estimated else "N", "orders": n_orders,
        "days_since_last_order": "" if days_since is None else days_since,
        "consent": c["reminder_consent"], "rules_matched": " + ".join(j for j in PRIORITY if j in matched) or "-",
        "journey": journey or "-", "offer": offer.get(journey, "") if journey else "",
        "action": action, "reason": reason, "demo_tester": c["demo_tester"]})

os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "decisions.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(decisions[0])); w.writeheader(); w.writerows(decisions)
with open(os.path.join(OUT, "broadcast_groups.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["message_pack", "customers", "demo_testers"])
    for pack, cs in sorted(groups.items()):
        w.writerow([pack, " ".join(c["customer_id"] for c in cs), " ".join(c["demo_tester"] for c in cs if c["demo_tester"])])
with open(os.path.join(OUT, "mantago_items_import.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["Item Name", "Item Description", "Item URL"])
    for p in products.values():
        if p["category"] in ("formula_infant", "milk_growing_up"):
            continue  # kept out of the recommendation database on purpose (SIFECS); shown only via MP-RE-MILK
        desc = f"{p['category']}; size {p['size'] or 'one size'}; age {p['min_age_m']}-{p['max_age_m']} months; S${p['price_sgd']}"
        w.writerow([p["name"], desc, p["url"]])

# frequently bought items (for 'popular at this stage')
pop = Counter(o["item_id"] for o in orders if products[o["item_id"]]["sifecs_scope"] != "Y")
sent = [d for d in decisions if d["action"].startswith("SEND")]
with open(os.path.join(OUT, "report.md"), "w") as f:
    f.write(f"# Segment engine report (as of {ASOF}, FICTIONAL data)\n\n")
    f.write(f"Customers: {len(decisions)} | Messaged: {len(sent)} | Not messaged: {len(decisions)-len(sent)}\n\n")
    f.write("By journey: " + ", ".join(f"{k} {v}" for k, v in Counter(d['journey'] for d in sent).items()) + "\n\n")
    f.write("Not messaged: " + ", ".join(f"{k} {v}" for k, v in Counter(d['reason'].split(';')[0] for d in decisions if not d['action'].startswith('SEND')).items()) + "\n\n")
    f.write("| Customer | Age (m) | Est. | Rules matched | Action | Offer | Reason |\n|---|---|---|---|---|---|---|\n")
    for d in decisions:
        f.write(f"| {d['customer_id']} | {d['child_age_months']} | {d['age_estimated']} | {d['rules_matched']} | {d['action']} | {d['offer']} | {d['reason']} |\n")
    f.write("\n## Broadcast groups (one MantaGO message pack each)\n\n| Message pack | Customers | Demo testers |\n|---|---|---|\n")
    for pack, cs in sorted(groups.items()):
        f.write(f"| {pack} | {' '.join(c['customer_id'] for c in cs)} | {' '.join(c['demo_tester'] for c in cs if c['demo_tester'])} |\n")
    f.write("\n## Most-bought items (excluding infant formula)\n\n" + ", ".join(f"{products[i]['name']} ({n})" for i, n in pop.most_common(5)) + "\n")

print(open(os.path.join(OUT, "report.md")).read())
