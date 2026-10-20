# Nestling — Nest Helper (Team JARDS, AI-GNITION 2026, Problem Statement 1)

> **Fictional shop. Simulated data.** Nestling is not a real business. Every customer, order and result here is invented for the competition.

**Live site:** https://jefire916.github.io/JARDS_PS1_Nestling/
**Bot:** "Nest Helper (JARDS)", MantaGO bot ID `olejqMRdj`, on the website's LiveChat bubble.

## What it is
Nest Helper is a MantaGO chatbot for a fictional Singapore baby shop. Babies run out of diapers, outgrow clothes and hit milestones on a schedule. A decision engine reads the order data, works out each family's next need, and picks **one** message per family: REFILL, SIZE_UP, MILESTONE or WIN_BACK. Each message is written for that baby's age and purchases, then checked by safety guardrails before it can go out. Parents reorder in one or two taps, can stop messages at any time, and can ask for a human.

What makes it different:
1. **Written for each baby.** A 10-month-old on Size 3 diapers gets the Size 4 suggestion, not a generic sale.
2. **"Why this message?"** Every reminder can explain which data it used.
3. **Guardrails first.** Consent, a 7-day cooldown and the infant-formula rules are checked before anything is sent. 7 of 20 families are deliberately *not* messaged (35%).

## The website
The site is static (GitHub Pages, from `docs/`):
- **Home:** the shop, an example reminder, and the offers.
- **Store:** all products, a working cart (checkout is switched off because the shop is fictional), the 10% stock-up discount and free-delivery messages.
- **Product pages:** 26 pages under `shop/`. The bot's reminder buttons open these pages with tracking tags (`?utm_source=livechat&utm_medium=refill|sizeup|winback|reorder&utm_campaign=nestling_ai`). Arriving from the bot shows a "You came from Nest Helper" banner.
- **How it works** (`OurStory.html`): how a message is chosen, the table of all 20 families and what each got (or why not), what is real and what is simulated, and contact details.

### Our offers
| Offer | Rule |
|---|---|
| Stage Bundles | S$49 / 52 / 58 / 58 / 62, with free delivery |
| Free delivery | On every bundle and on orders over S$60 |
| Stock up | Buy 3 packs of the same diapers or wipes, save 10% |
| Free size exchange | Clothing and bundles, within 30 days (unworn, with tags), free both ways |
| Welcome back | No order for 60+ days: free delivery on the next order within 14 days |
| Milestones | At 6 months and in the first-birthday month: free delivery on the next order within 7 days |

No offer applies to infant formula, follow-on formula or growing-up milk.

## Try the bot
1. Open the website and tap the chat bubble at the bottom right, then **Start Chat**.
2. Type a keyword:
   - `DEMO` — **Meet the families**: pick a family to see the message the engine chose for them. Tap **Why this message?** to see the data used.
   - `MENU` — main menu
   - `REORDER` — reorder past items
   - `ASK` — AI questions (sizes, shipping, offers, care)
   - `HUMAN` — talk to a person
   - `STOP` — stop reminders

## The decision engine
Uses Python 3 only, no extra libraries.
```
python3 engine/segment_engine.py              # decisions as of 2026-10-20
python3 engine/segment_engine.py 2026-10-27   # any other date
python3 engine/compose_messages.py            # writes and guardrail-checks the messages
python3 engine/build_site_v2.py docs          # rebuilds the product pages and "How it works"
```
Results are written to `output/`:
- `decisions.csv` — every customer, the action and the reason.
- `messages.csv` — the message chosen for each messaged customer.
- `guardrail_tests.csv` — the guardrail checks (13 of 13 real messages pass; 7 of 7 deliberately bad messages are blocked).
- `broadcast_groups.csv` — which message pack goes to which customers.
- `mantago_items_import.csv` — the product list for MantaGO's database.
- `report.md` — a readable summary.

### Rules
| Journey | Trigger |
|---|---|
| REFILL | Diapers, wipes or growing-up milk run out within 2 days before or 3 days after today, based on the family's own reorder gap. Suggests the next diaper size when the baby is ready. |
| SIZE_UP | The baby's age is within 1 month of the upper limit of the last clothing size bought. |
| MILESTONE | The baby is 6 or 12 months old. |
| WIN_BACK | 2 or more orders, and 60 or more days since the last order. |

- **Priority:** REFILL, then SIZE_UP, then MILESTONE, then WIN_BACK. One message per customer.
- **Restraint:** messages go only to customers who agreed to reminders, at most one every 7 days.
- **Result for the 20 fictional families:** 13 messaged (REFILL 6, SIZE_UP 2, MILESTONE 2, WIN_BACK 3), 7 held back (2 no consent, 4 no rule matched, 1 cooldown).

## Infant formula policy (SIFECS)
This follows Singapore's Code of Ethics for the Sale of Infant Foods (SIFECS), 5th edition.
- **Infant formula (0–12 months):** no discounts, no bundles, no promotion and no message started by the bot. Parent-initiated reorder only. The bot never recommends brands and never gives feeding advice.
- **Growing-up milk (1–3 years):** refill reminders go only to customers who agreed to reminders. No discounts.

## Testing
`tests/Nestling_Test_Log_and_Results.xlsx` holds the test log and results: **35 tests, 34 pass, 0 fail, 1 not run** (UTM click analytics needs a MantaGO premium plan, which we do not have).
One real failure was found and fixed: the AI repeated a customer's name and date from a customer-data file. We switched that file off, added a privacy rule, and retested. The "Failure Fix" sheet shows before and after.

## What is real vs simulated
- **Real:** the MantaGO bot (menu, message packs, reorder, STOP, human handover), the AI answers, the engine logic and its output, the website, the tracked links on the bot's buttons, and the tests.
- **Simulated:** the shop, customers, orders and prices; the engine run (we run it by hand, the bot does not call it); the reminder arriving (shown through "Meet the families" instead of a scheduled broadcast, because scheduled sending needs a premium plan); click analytics (links are tagged but we cannot read the clicks); the "Remind me in 3 days" follow-up; and all metric results.

## Limitations and next steps
- Run the engine daily and send each pack as a broadcast (needs a MantaGO plan with scheduling).
- Make "Remind me in 3 days" a real snooze.
- Read UTM clicks to measure repeat purchases against a holdout group (the target measure is repeat buyers ÷ families reminded within 30 days, vs a 20% holdout).
- Add birthday-based ideas for toys and play.

## Repository contents
| Folder | What it holds | Owner |
|---|---|---|
| `docs/` | The Nestling website (GitHub Pages) | Jeiyanth, Reyansh (site design) |
| `data/` | Fictional customers, orders, products | Devanshi |
| `engine/` | Decision engine, message writer with guardrails, site builder | Devanshi (engine), Jeiyanth (site builder) |
| `output/` | Engine results and the MantaGO product import | Devanshi |
| `bot/` | Message packs, link list, AI set-up | Adhvik |
| `ai/` | AI knowledge file ("Nestling Shop Facts") and set-up notes | Shivangi |
| `tests/` | Test log and results workbook | Jeiyanth, Reyansh |
| `slides/` | Slides outline, demo script, screenshots | Reyansh |

## AI use declaration
Claude (Anthropic) helped draft the fictional data, the engine code, the website pages and the bot content. The team reviewed, built, configured and tested everything in MantaGO.

## Team JARDS
| Member | Role |
|---|---|
| Jeiyanth (lead) | Chat window, product database, connecting everything, GitHub, testing |
| Devanshi | Customer data and decision engine |
| Adhvik | Message packs |
| Shivangi | AI answers, knowledge base, human agent |
| Reyansh | Website design, results, slides |
