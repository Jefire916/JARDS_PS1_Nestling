"""
Nestling Decision Engine (Team JARDS, AI-GNITION 2026, Problem Statement 1)
Author: Devanshi (customer data and decision engine lead)

What it does
    For every customer it decides: send one message, or stay quiet, and why.
    It follows the decision flowchart, in this order:

      1. Guardrail: STOP pressed, or no reminder consent   -> no message (NO-MSG-C05)
      2. Guardrail: infant formula (SIFECS)                  -> formula never triggers a message (NO-MSG-C07)
      3. Guardrail: snooze active ("Remind me in 3 days")    -> hold off
      4. Guardrail: 7-day cooldown                           -> hold off
      5. Rules, one message only, in priority order:
           Priority 1  REFILL     diapers, wipes or growing-up milk run out within
                                  2 days before to 3 days after today, from the
                                  family's own reorder gap (suggests the next
                                  diaper size when the baby is ready)
           Priority 2  SIZE_UP    baby is within 1 month of the top of the last
                                  clothing size bought
           Priority 3  MILESTONE  baby is 6 or 12 months old
           Priority 4  WIN_BACK   2+ orders and 60+ days since the last order
      6. Nothing matched                                     -> no message

    The numbers are the same as engine/segment_engine.py and the website, and
    the script checks itself against output/decisions.csv every time it runs.

Data
    Reads data/customers.csv, data/orders.csv and data/products.csv.
    It uses only the baby's birth month and what was bought. No names, photos
    or addresses are stored or used.
    Optional columns in customers.csv: "stopped" (Y/N) and "snooze_until"
    (YYYY-MM-DD). If they are missing, nobody is treated as stopped or snoozed.

Run (Python 3 only, no extra libraries)
    python3 engine/decision_engine.py               decisions as of 2026-10-20
    python3 engine/decision_engine.py 2026-10-27    any other date
    Writes output/decision_engine_results.csv and prints a summary.

Optional API (for a future live connection to MantaGO)
    pip install fastapi uvicorn
    python3 engine/decision_engine.py --api         http://localhost:8000/docs
    Note: on our MantaGO plan the bot cannot call an outside API or send on a
    schedule, so in the demo we run the engine by hand and show its decisions
    through the "Meet the families" menu.
"""

import csv
import os
import sys
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from datetime import date, timedelta
from statistics import median
from typing import Dict, List, Optional, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
OUT_DIR = os.path.join(ROOT, "output")
DEFAULT_AS_OF = date(2026, 10, 20)   # fixed date so the demo always gives the same answers

# ---------------------------------------------------------
# RULES (same numbers as segment_engine.py and the website)
# ---------------------------------------------------------
REFILL_WINDOW = (-2, 3)              # run-out from 2 days ago to 3 days ahead
REFILL_CATEGORIES = {"diapers", "wipes", "milk_growing_up"}
INFANT_FORMULA = "formula_infant"    # SIFECS: never starts a message
CLOTHING_CATEGORIES = {"clothing", "bundle"}
MILESTONE_AGES = {6, 12}             # 6 months and the first-birthday month
WIN_BACK_DAYS = 60
WIN_BACK_MIN_ORDERS = 2
ANTI_SPAM_COOLDOWN_DAYS = 7          # at most one bot-started message every 7 days
PRIORITY = ["REFILL", "SIZE_UP", "MILESTONE", "WIN_BACK"]
DIAPER_LADDER = ["DP-NB", "DP-1", "DP-2", "DP-3", "DP-4"]
NEXT_BUNDLE = {"NB": "BN-0-3", "0-3M": "BN-3-6", "3-6M": "BN-6-9", "6-9M": "BN-9-12", "9-12M": "BN-12-18"}

# ---------------------------------------------------------
# EXACT MANTAGO MESSAGE PACK NAMES (as built in Nest Helper)
# ---------------------------------------------------------
BUILT_JOURNEY_PACKS = {"RF-DP3-UP-DP4", "SU-0-3M-TO-3-6M", "MS-12M", "WB-12-18M"}
REFILL_FALLBACK_PACKS = [("DP", "MP-RE-DIAPERS"), ("WP", "MP-RE-WIPES"), ("GM", "MP-RE-MILK")]
WHY_PACKS = {"REFILL": "WHY-RF", "SIZE_UP": "WHY-SU", "MILESTONE": "WHY-MS", "WIN_BACK": "WHY-WB"}
BUNDLE_CARD_PACKS = {"BN-3-6": "CARD-BN-3-6", "BN-12-18": "CARD-BN-12-18"}
NO_CONSENT_PACK = "NO-MSG-C05"
FORMULA_LOCK_PACK = "NO-MSG-C07"
DEMO_BUTTONS = {  # the six families in the bot's "Meet the families" menu (MP-DEMO)
    "C01": "Diapers running low", "C02": "Outgrowing clothes", "C03": "First birthday",
    "C04": "Been a while", "C05": "Didn't opt in", "C07": "Formula is due",
}
PRIORITY_LABEL = {"REFILL": "Priority 1: Refill", "SIZE_UP": "Priority 2: Size up",
                  "MILESTONE": "Priority 3: Milestone", "WIN_BACK": "Priority 4: Win back"}


# ---------------------------------------------------------
# DATA MODELS
# ---------------------------------------------------------
@dataclass
class Order:
    order_id: str
    order_date: date
    item_id: str
    qty: int


@dataclass
class CustomerProfile:
    customer_id: str
    child_birth_month: Optional[str]       # "YYYY-MM", or None if unknown
    reminder_consent: bool
    last_bot_message_date: Optional[date] = None
    is_stopped: bool = False               # pressed STOP (MP-STOP)
    snooze_until: Optional[date] = None    # from "Remind me in 3 days" (MP-LATER) or MP-QUIET
    orders: List[Order] = field(default_factory=list)


@dataclass
class DecisionOutput:
    customer_id: str
    baby_age_months: Optional[int]
    age_estimated: bool
    eligible_for_outbound: bool
    priority_rank: str
    journey: str                       # REFILL / SIZE_UP / MILESTONE / WIN_BACK / -
    journey_code: str                  # e.g. RF-DP3-UP-DP4 (matches segment_engine.py)
    target_message_pack: str           # the MantaGO pack to send or show
    pack_status: str                   # built / closest built pack / not built yet / -
    recommended_bundle_pack: str
    explanation_pack: str              # matching "Why this message?" pack
    offer: str
    rules_matched: str
    decision_reason: str
    demo_button: str


# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------
def _read_csv(name: str) -> List[dict]:
    with open(os.path.join(DATA_DIR, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _to_date(text: Optional[str]) -> Optional[date]:
    text = (text or "").strip()
    return date.fromisoformat(text) if text else None


def load_products() -> Dict[str, dict]:
    return {p["item_id"]: p for p in _read_csv("products.csv")}


def load_customers() -> Dict[str, CustomerProfile]:
    orders_by_customer = defaultdict(list)
    for o in _read_csv("orders.csv"):
        orders_by_customer[o["customer_id"]].append(
            Order(o["order_id"], date.fromisoformat(o["order_date"]), o["item_id"], int(o["qty"])))
    customers = {}
    for row in _read_csv("customers.csv"):
        cid = row["customer_id"].strip()
        customers[cid] = CustomerProfile(
            customer_id=cid,
            child_birth_month=row.get("child_birth_month", "").strip() or None,
            reminder_consent=row.get("reminder_consent", "").strip().upper() == "Y",
            last_bot_message_date=_to_date(row.get("last_bot_message_date")),
            is_stopped=row.get("stopped", "").strip().upper() == "Y",
            snooze_until=_to_date(row.get("snooze_until")),
            orders=orders_by_customer.get(cid, []),
        )
    return customers


PRODUCTS = load_products()


# ---------------------------------------------------------
# DECISION ENGINE LOGIC
# ---------------------------------------------------------
def _months_between(d1: date, d2: date) -> int:
    return (d2.year - d1.year) * 12 + (d2.month - d1.month) - (1 if d2.day < d1.day else 0)


def _describe(offer: str) -> str:
    """Turn 'DP-3->DP-4, WP-80' into product names for the reason text."""
    parts = []
    for piece in offer.split(", "):
        if "->" in piece:
            a, b = piece.split("->")
            parts.append(f"{PRODUCTS[a]['name']} (or move up to {PRODUCTS[b]['name']})")
        else:
            parts.append(PRODUCTS[piece]["name"])
    return " and ".join(parts)


class NestlingDecisionEngine:

    @staticmethod
    def verify_consent(cust: CustomerProfile, tags_conf: Optional[Dict[str, float]] = None) -> Tuple[bool, str]:
        """Consent from the customer record. If MantaGO consent tags are passed in
        (e.g. from the CONSENT-YES / CONSENT-NO packs), opt-in must be strictly
        higher than opt-out plus OPT_OUT, otherwise there is no consent."""
        if tags_conf:
            conf_in = tags_conf.get("consent_opted_in", 0.0)
            rejection = tags_conf.get("consent_opted_out", 0.0) + tags_conf.get("OPT_OUT", 0.0)
            return conf_in > rejection, f"tags: opt-in {conf_in:.2f} vs opt-out {rejection:.2f}"
        return cust.reminder_consent, "customer record"

    @staticmethod
    def resolve_baby_age(cust: CustomerProfile, today: date) -> Tuple[Optional[int], bool]:
        """Age in whole months from the birth month. If the birth month is unknown,
        estimate it from the last sized item bought (middle of that size band plus
        the months since). Returns (age, estimated)."""
        if cust.child_birth_month:
            y, m = map(int, cust.child_birth_month.split("-"))
            return (today.year - y) * 12 + (today.month - m), False
        sized = [o for o in cust.orders
                 if PRODUCTS[o.item_id]["category"] in CLOTHING_CATEGORIES | {"diapers"}]
        if not sized:
            return None, True
        last = max(sized, key=lambda o: o.order_date)
        p = PRODUCTS[last.item_id]
        mid = (float(p["min_age_m"]) + float(p["max_age_m"])) / 2
        return int(mid + _months_between(last.order_date, today)), True

    @staticmethod
    def items_running_out(cust: CustomerProfile, today: date) -> Tuple[List[str], List[str]]:
        """Predict when each consumable runs out from the family's own reorder gap
        (median gap x pack quantity), or pack days x quantity if bought only once.
        Returns (refill items due, infant formula items due)."""
        by_item = defaultdict(list)
        for o in cust.orders:
            by_item[o.item_id].append(o)
        due, formula_due = [], []
        for iid, lst in by_item.items():
            category = PRODUCTS[iid]["category"]
            if category not in REFILL_CATEGORIES | {INFANT_FORMULA}:
                continue
            lst.sort(key=lambda o: o.order_date)
            last = lst[-1]
            if len(lst) >= 2:
                gap = median((b.order_date - a.order_date).days for a, b in zip(lst, lst[1:])) * last.qty
            else:
                gap = int(PRODUCTS[iid]["pack_days"]) * last.qty
            days_left = (last.order_date + timedelta(days=round(gap)) - today).days
            if REFILL_WINDOW[0] <= days_left <= REFILL_WINDOW[1]:
                (formula_due if category == INFANT_FORMULA else due).append(iid)
        return sorted(due), sorted(formula_due)

    @staticmethod
    def next_diaper_size(iid: str, age: Optional[int]) -> Optional[str]:
        if iid not in DIAPER_LADDER or age is None:
            return None
        i = DIAPER_LADDER.index(iid)
        if i + 1 < len(DIAPER_LADDER) and age >= float(PRODUCTS[DIAPER_LADDER[i + 1]]["min_age_m"]):
            return DIAPER_LADDER[i + 1]
        return None

    @staticmethod
    def bundle_for_age(age: int) -> str:
        for iid in ["BN-0-3", "BN-3-6", "BN-6-9", "BN-9-12", "BN-12-18"]:
            if age < float(PRODUCTS[iid]["max_age_m"]):
                return iid
        return "BN-12-18"

    @classmethod
    def match_rules(cls, cust: CustomerProfile, age: Optional[int], today: date):
        """Check all four rules. Returns (matched {journey: code}, offers, formula items due)."""
        matched, offer = {}, {}
        n_orders = len({o.order_id for o in cust.orders})
        last_order = max((o.order_date for o in cust.orders), default=None)
        days_since = (today - last_order).days if last_order else None

        # Priority 1: REFILL
        due, formula_due = cls.items_running_out(cust, today)
        if due:
            recs = []
            for iid in due:
                up = cls.next_diaper_size(iid, age)
                recs.append(f"{iid}->{up}" if up else iid)
            matched["REFILL"] = "RF-" + "+".join(
                r.replace("DP-", "DP").replace("WP-", "WP").replace("GM-", "GM").replace("->", "-UP-") for r in recs)
            offer["REFILL"] = ", ".join(recs)

        # Priority 2: SIZE_UP
        clothes = [o for o in cust.orders if PRODUCTS[o.item_id]["category"] in CLOTHING_CATEGORIES]
        if clothes and age is not None:
            last_cl = PRODUCTS[max(clothes, key=lambda o: o.order_date).item_id]
            top = float(last_cl["max_age_m"])
            if top - 1 <= age <= top + 1 and last_cl["size"] in NEXT_BUNDLE:
                nxt = NEXT_BUNDLE[last_cl["size"]]
                matched["SIZE_UP"] = f"SU-{last_cl['size']}-TO-{PRODUCTS[nxt]['size']}"
                offer["SIZE_UP"] = nxt

        # Priority 3: MILESTONE
        if age in MILESTONE_AGES and n_orders >= 1:
            matched["MILESTONE"] = f"MS-{age}M"
            offer["MILESTONE"] = cls.bundle_for_age(age + 1)

        # Priority 4: WIN_BACK
        if n_orders >= WIN_BACK_MIN_ORDERS and days_since is not None and days_since >= WIN_BACK_DAYS:
            b = cls.bundle_for_age(age + 1) if age is not None else "BN-12-18"
            matched["WIN_BACK"] = f"WB-{PRODUCTS[b]['size']}"
            offer["WIN_BACK"] = b

        return matched, offer, formula_due

    @staticmethod
    def pick_pack(journey: str, code: str) -> Tuple[str, str]:
        if code in BUILT_JOURNEY_PACKS:
            return code, "built"
        if journey == "REFILL":
            for prefix, pack in REFILL_FALLBACK_PACKS:
                if f"-{prefix}" in code or f"+{prefix}" in code:
                    return pack, "closest built pack"
        return code, "not built yet"

    @classmethod
    def evaluate(cls, cust: CustomerProfile, today: date = DEFAULT_AS_OF,
                 tags_conf: Optional[Dict[str, float]] = None) -> DecisionOutput:
        """Single-message waterfall: guardrails first, then the highest-priority rule.
        At most one message per customer."""
        age, estimated = cls.resolve_baby_age(cust, today)
        matched, offer, formula_due = cls.match_rules(cust, age, today)
        rules = " + ".join(j for j in PRIORITY if j in matched) or "-"
        base = dict(customer_id=cust.customer_id, baby_age_months=age, age_estimated=estimated,
                    rules_matched=rules, demo_button=DEMO_BUTTONS.get(cust.customer_id, ""))

        def quiet(rank, pack, reason):
            return DecisionOutput(eligible_for_outbound=False, priority_rank=rank, journey="-",
                                  journey_code="-", target_message_pack=pack,
                                  pack_status="built" if pack != "-" else "-",
                                  recommended_bundle_pack="-", explanation_pack="-", offer="-",
                                  decision_reason=reason, **base)

        # Guardrail 1: STOP or no consent
        has_consent, _ = cls.verify_consent(cust, tags_conf)
        if cust.is_stopped:
            return quiet("Guardrail 1: Stopped", "-",
                         "This parent typed STOP, so Nest Helper sends nothing until they opt in again.")
        if not has_consent:
            return quiet("Guardrail 1: No consent", NO_CONSENT_PACK,
                         "This family didn't agree to reminders, so Nest Helper stays quiet. No consent, no message.")

        # Guardrail 2: infant formula never triggers a message (SIFECS)
        if formula_due and not matched:
            return quiet("Guardrail 2: Infant formula (SIFECS)", FORMULA_LOCK_PACK,
                         "Infant formula is due, but Nest Helper never starts a message about infant formula "
                         "(Singapore's SIFECS code). The parent can still type REORDER.")
        formula_note = (" Infant formula is also due, but it is never mentioned (SIFECS)." if formula_due else "")

        # Guardrail 3: snooze
        if cust.snooze_until and today < cust.snooze_until:
            days_left = (cust.snooze_until - today).days
            return quiet("Guardrail 3: Snoozed", "-",
                         f"The parent asked to wait. Held off for {days_left} more day(s), until {cust.snooze_until}.")

        # Guardrail 4: cooldown
        if cust.last_bot_message_date and (today - cust.last_bot_message_date).days < ANTI_SPAM_COOLDOWN_DAYS:
            return quiet("Guardrail 4: 7-day cooldown", "-",
                         f"Nest Helper already messaged on {cust.last_bot_message_date}. "
                         f"At most one message every {ANTI_SPAM_COOLDOWN_DAYS} days.")

        # Rules: highest priority wins, the rest wait
        journey = next((j for j in PRIORITY if j in matched), None)
        if journey is None:
            return quiet("No rule matched", "-", "Nothing is running out and no milestone is due, so no message."
                         + formula_note)

        code = matched[journey]
        pack, status = cls.pick_pack(journey, code)
        bundle = BUNDLE_CARD_PACKS.get(offer[journey], "-") if journey != "REFILL" else "-"
        waiting = [j for j in PRIORITY if j in matched and j != journey]
        what = _describe(offer[journey])
        months = f"{age} month{'s' if age != 1 else ''}"
        reason = {
            "REFILL": f"Running out soon, based on how often this family reorders: {what}.",
            "SIZE_UP": f"Baby is {months}, near the top of the last clothing size. Suggests the {what}.",
            "MILESTONE": f"Baby turns {months}. Free delivery for 7 days, plus the {what}.",
            "WIN_BACK": f"No order for {WIN_BACK_DAYS}+ days. Welcome back: free delivery within 14 days, plus the {what}.",
        }[journey]
        if waiting:
            reason += f" Also matched {', '.join(waiting)}; only one message is sent, the rest wait."
        return DecisionOutput(eligible_for_outbound=True, priority_rank=PRIORITY_LABEL[journey],
                              journey=journey, journey_code=code, target_message_pack=pack,
                              pack_status=status, recommended_bundle_pack=bundle,
                              explanation_pack=WHY_PACKS[journey], offer=offer[journey],
                              decision_reason=reason + formula_note, **base)


# ---------------------------------------------------------
# COMMAND LINE RUN
# ---------------------------------------------------------
def run_all(today: date = DEFAULT_AS_OF) -> List[DecisionOutput]:
    return [NestlingDecisionEngine.evaluate(c, today) for c in load_customers().values()]


def self_check(results: List[DecisionOutput]) -> str:
    """Compare with output/decisions.csv (written by segment_engine.py for the same date)."""
    path = os.path.join(OUT_DIR, "decisions.csv")
    if not os.path.exists(path):
        return "Self-check skipped: run engine/segment_engine.py first."
    with open(path, newline="", encoding="utf-8") as f:
        expected = {r["customer_id"]: r["action"] for r in csv.DictReader(f)}
    mismatches = []
    for r in results:
        mine = f"SEND {r.journey_code}" if r.eligible_for_outbound else "NO MESSAGE"
        if expected.get(r.customer_id) != mine:
            mismatches.append(f"{r.customer_id}: engine says {mine}, decisions.csv says {expected.get(r.customer_id)}")
    if mismatches:
        return "Self-check FAILED (if you used another date, run segment_engine.py with it too):\n  " + "\n  ".join(mismatches)
    return f"Self-check passed: same decision as output/decisions.csv for all {len(results)} customers."


def main_cli(today: date) -> None:
    results = run_all(today)
    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, "decision_engine_results.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(asdict(results[0])))
        w.writeheader()
        w.writerows(asdict(r) for r in results)

    sent = [r for r in results if r.eligible_for_outbound]
    print(f"Nestling decision engine, as of {today} (fictional data)")
    print(f"Customers: {len(results)} | Messaged: {len(sent)} | Held back: {len(results) - len(sent)}")
    print("By journey: " + ", ".join(f"{k} {v}" for k, v in Counter(r.journey for r in sent).items()))
    print("Held back: " + ", ".join(f"{k} {v}" for k, v in
                                    Counter(r.priority_rank for r in results if not r.eligible_for_outbound).items()))
    print()
    print(f"{'ID':<4} {'Age':>3}  {'Decision':<38} {'MantaGO pack':<16} Reason")
    for r in results:
        decision = r.journey_code if r.eligible_for_outbound else r.priority_rank
        print(f"{r.customer_id:<4} {'' if r.baby_age_months is None else r.baby_age_months:>3}  "
              f"{decision:<38} {r.target_message_pack:<16} {r.decision_reason}")
    print()
    print(self_check(results) if today == DEFAULT_AS_OF else
          "Self-check runs only for the default date (2026-10-20).")
    print(f"Saved: {os.path.relpath(out_path, ROOT)}")


# ---------------------------------------------------------
# OPTIONAL REST API (needs: pip install fastapi uvicorn)
# ---------------------------------------------------------
def build_api():
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel

    app = FastAPI(title="Nestling Decision Engine API",
                  description="Decides which single message Nest Helper should send, or why it stays quiet. "
                              "Fictional data.", version="3.0.0")
    customers = load_customers()   # in-memory copy; STOP and snooze changes last until restart

    class SnoozeAction(BaseModel):
        customer_id: str
        snooze_type: str = "3_DAYS"    # "3_DAYS" (MP-LATER) or "7_DAYS" (MP-QUIET)

    class CustomerAction(BaseModel):
        customer_id: str

    def get(cid: str) -> CustomerProfile:
        if cid not in customers:
            raise HTTPException(404, f"Unknown customer {cid}. No data, so no message.")
        return customers[cid]

    @app.get("/")
    def health_check():
        return {"status": "online", "engine": "Nestling Decision Engine 3.0",
                "as_of": str(DEFAULT_AS_OF), "customers_loaded": len(customers),
                "order": ["Guardrail: STOP / consent", "Guardrail: infant formula (SIFECS)",
                          "Guardrail: snooze", "Guardrail: 7-day cooldown",
                          "Priority 1 REFILL", "Priority 2 SIZE_UP", "Priority 3 MILESTONE", "Priority 4 WIN_BACK"]}

    @app.get("/api/v1/decisions")
    def all_decisions(as_of: Optional[str] = None):
        today = date.fromisoformat(as_of) if as_of else DEFAULT_AS_OF
        return [asdict(NestlingDecisionEngine.evaluate(c, today)) for c in customers.values()]

    @app.get("/api/v1/decisions/{customer_id}")
    def one_decision(customer_id: str, as_of: Optional[str] = None):
        today = date.fromisoformat(as_of) if as_of else DEFAULT_AS_OF
        return asdict(NestlingDecisionEngine.evaluate(get(customer_id), today))

    @app.post("/api/v1/snooze")
    def snooze(action: SnoozeAction):
        days = 3 if action.snooze_type == "3_DAYS" else 7
        get(action.customer_id).snooze_until = DEFAULT_AS_OF + timedelta(days=days)
        return {"customer_id": action.customer_id, "pack": "MP-LATER" if days == 3 else "MP-QUIET",
                "snooze_until": str(DEFAULT_AS_OF + timedelta(days=days))}

    @app.post("/api/v1/stop")
    def stop(action: CustomerAction):
        get(action.customer_id).is_stopped = True
        return {"customer_id": action.customer_id, "pack": "MP-STOP", "stopped": True}

    @app.post("/api/v1/mantago-webhook")
    def mantago_webhook(payload: dict):
        """For a future MantaGO action: send {"customerId": "C01", "tags": ["consent_opted_in"]}."""
        cust = get(str(payload.get("customerId", "")))
        tags = payload.get("tags")
        tags_conf = {t: 1.0 for t in tags} if isinstance(tags, list) else (tags if isinstance(tags, dict) else None)
        r = NestlingDecisionEngine.evaluate(cust, DEFAULT_AS_OF, tags_conf)
        return {"replyMessagePack": r.target_message_pack, "sendNow": r.eligible_for_outbound,
                "recommendedBundlePack": r.recommended_bundle_pack, "explanationPack": r.explanation_pack,
                "priorityRank": r.priority_rank, "reason": r.decision_reason}

    return app


if __name__ == "__main__":
    if "--api" in sys.argv:
        import uvicorn
        uvicorn.run(build_api(), host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
    else:
        args = [a for a in sys.argv[1:] if not a.startswith("--")]
        main_cli(date.fromisoformat(args[0]) if args else DEFAULT_AS_OF)
