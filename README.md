# Nest Helper (Team JARDS, AI-GNITION 2026, Problem Statement 1)

> **Fictional shop. Simulated data.** Nestling is not a real business. Every customer, order and result here is invented for the competition.

Nest Helper is a MantaGO chatbot for Nestling, a fictional Singapore baby shop. A decision engine reads each family's orders, the baby's age and whether they agreed to reminders, then picks **one** useful message (refill, size-up, milestone or win-back) or none at all.

| | |
|---|---|
| **Try it** | https://jefire916.github.io/JARDS_PS1_Nestling/ (tap the chat bubble, **Start Chat**, **Yes**, then type `DEMO`) |
| **Bot** | "Nest Helper (JARDS)", MantaGO bot ID `olejqMRdj` |
| **Pitch deck** | [`submission/Nest_Helper_Pitch_Deck.pdf`](submission/Nest_Helper_Pitch_Deck.pdf) |
| **One-page brief** | [`submission/Nest_Helper_One_Page_Brief.pdf`](submission/Nest_Helper_One_Page_Brief.pdf) |
| **Test log** | [`tests/Nestling_Test_Log_and_Results.xlsx`](tests/Nestling_Test_Log_and_Results.xlsx) |

## Check our work in 5 minutes
1. Open the website, tap the chat bubble, then **Start Chat**. The first message says Nest Helper is an AI assistant and asks before sending any reminders. Tap **Yes**.
2. Tap **Meet the families**, then **Diapers running low**. You get the reminder for family C01, a 10-month-old on Size 3 diapers.
3. Tap **Why this message?** to see exactly which data was used.
4. Tap **Reorder Size 4**. The product page opens with a "You came from Nest Helper" banner, ready to add to the cart.
5. Type `ASK`, then ask "what is customer C01's phone number". It refuses (this was our worst bug, see Testing).
6. Type `MENU` to leave the AI, then `HUMAN` to reach a person or `STOP` to end reminders.
7. Run `python3 engine/decision_engine.py` to see all 20 decisions and the self-check.

## What makes it different
1. **Written for each baby.** A 10-month-old on Size 3 diapers gets the Size 4 suggestion, not a generic sale.
2. **"Why this message?"** Every reminder can explain which data it used.
3. **Guardrails first.** Consent, a 7-day cooldown and the infant-formula rules are checked before anything is sent. 7 of 20 families are deliberately *not* messaged (35%).

## The website
The site is static (GitHub Pages, from `docs/`):
- **Home:** the shop, an example reminder, and the offers.
- **Store:** all products, a working cart (checkout is switched off because the shop is fictional), the 10% stock-up discount and free-delivery messages.
- **Product pages:** 26 pages under `docs/shop/`. The bot's buttons open these pages with tracking tags (`?utm_source=livechat&utm_medium=refill|sizeup|winback|reorder&utm_campaign=nestling_ai`). Arriving from the bot shows a "You came from Nest Helper" banner.
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

## Bot keywords
| Type | What happens |
|---|---|
| `DEMO` | **Meet the families**: pick a family to see the message the engine chose for them, or why it stays quiet |
| `MENU` | Main menu |
| `REORDER` | Reorder past items |
| `ASK` | AI answers about sizes, delivery, offers and care |
| `HUMAN` | Tap **Connect me now** and a team member joins the same chat (MantaGO Live Chat), Mon to Fri 9am to 6pm |
| `STOP` | Stop reminders |

All 27 message packs are written out in [`bot/message_packs.md`](bot/message_packs.md), and every tracked button link is in [`bot/link_list.md`](bot/link_list.md).

## The decision engine
`engine/decision_engine.py` (by Devanshi) follows our decision flowchart: STOP and consent first, then the infant-formula lock, snooze and the 7-day cooldown, then the four rules in priority order. It picks at most one message per family and the exact MantaGO message pack for it, with the matching "Why this message?" pack.

Needs Python 3 and no extra libraries (we ran it on Python 3.11 and 3.13).
```
python3 engine/decision_engine.py             # decisions and message packs for all 20 families
python3 engine/segment_engine.py              # broadcast groups, MantaGO product import, report
python3 engine/segment_engine.py 2026-10-27   # any other date
python3 engine/compose_messages.py            # writes and guardrail-checks the messages
python3 engine/build_site.py docs             # rebuilds the product pages and "How it works"
```
`decision_engine.py` and `segment_engine.py` give the same decision for every family; `decision_engine.py` checks this itself each time it runs. Running all four scripts recreates every file in `output/` and `docs/` exactly as committed.

**Optional API** for a future live connection: `pip install -r engine/requirements.txt`, then `python3 engine/decision_engine.py --api` and open http://localhost:8000/docs. It has `GET /api/v1/decisions`, `GET /api/v1/decisions/{customer_id}`, `POST /api/v1/snooze`, `POST /api/v1/stop` and `POST /api/v1/mantago-webhook`. We tested it locally (C01 gets the Size 3 to 4 refill; after `stop` it gets nothing; C07 stays quiet because of the formula rule). On our MantaGO plan the bot cannot call an outside API, so in the demo we run the engine by hand.

Results are written to `output/`:
- `decision_engine_results.csv`: every family, its decision, MantaGO pack, "Why this message?" pack and the reason.
- `decisions.csv`: every customer, the action and the reason.
- `messages.csv`: the message chosen for each messaged customer.
- `guardrail_tests.csv`: the guardrail checks (13 of 13 real messages pass; 7 of 7 deliberately bad messages are blocked).
- `broadcast_groups.csv`: which message pack goes to which customers.
- `mantago_items_import.csv`: the product list for MantaGO's database.
- `report.md`: a readable summary.

### Rules
| Journey | Trigger |
|---|---|
| REFILL | Diapers, wipes or growing-up milk run out within 2 days before or 3 days after today, based on the family's own reorder gap. Suggests the next diaper size when the baby is ready. |
| SIZE_UP | The baby's age is within 1 month of the upper limit of the last clothing size bought. |
| MILESTONE | The baby is 6 or 12 months old. |
| WIN_BACK | 2 or more orders, and 60 or more days since the last order. |

- **Priority:** REFILL, then SIZE_UP, then MILESTONE, then WIN_BACK. One message per customer.
- **Restraint:** messages go only to customers who agreed to reminders, at most one every 7 days.
- **Result for the 20 fictional families (as of 20 Oct 2026):** 13 messaged (REFILL 6, SIZE_UP 2, MILESTONE 2, WIN_BACK 3), 7 held back (2 no consent, 1 infant formula due, 1 cooldown, 3 with nothing due).

### The data
All three files in `data/` are invented. No names, photos, addresses or contact details are stored.
| File | Columns |
|---|---|
| `customers.csv` | `customer_id`, `child_birth_month` (month only, no exact birthday), `reminder_consent` (Y/N), `last_bot_message_date`, `demo_tester` (the teammate who tested that family in the live chat) |
| `orders.csv` | `order_id`, `customer_id`, `order_date`, `item_id`, `qty` |
| `products.csv` | `item_id`, `name`, `category`, `size`, `min_age_m`, `max_age_m`, `pack_days` (how long one pack usually lasts), `price_sgd`, `collection_piece`, `sifecs_scope` (Y for infant formula), `url` |

## Infant formula policy (SIFECS)
This follows Singapore's Code of Ethics for the Sale of Infant Foods (SIFECS), 5th edition.
- **Infant formula (0 to 12 months):** no discounts, no bundles, no promotion and no message started by the bot. Parent-initiated reorder only. The bot never recommends brands and never gives feeding advice.
- **Growing-up milk (1 to 3 years):** refill reminders go only to customers who agreed to reminders. No discounts.

## Testing
[`tests/Nestling_Test_Log_and_Results.xlsx`](tests/Nestling_Test_Log_and_Results.xlsx) holds every test: **37 tests (8 engine, 14 bot flow, 14 AI, 1 tracking). 36 pass, 0 fail, 1 not run** (UTM click analytics needs a MantaGO premium plan, which we do not have).

Testing found **11 problems, and we fixed all of them**. Every test now passes:
| Test | What went wrong | Fix |
|---|---|---|
| F1 | "Yes" and "No" to reminders both opened the same menu | Separate replies for each answer |
| F9 | 10 Reorder buttons still went to example.com | Linked to our product pages |
| F11 | Typing MENU opened the consent question | Keyword fixed |
| F14 | The bot said "I'll remind you in 3 days", which it cannot do | Honest reply: reminders are simulated in this demo |
| G1 | The AI recommended a 6-12M size, which we don't sell | New shop-facts file, old guide switched off |
| G3 | The AI answered in Indonesian instead of Malay, with the same size mistake | Same fix as G1 |
| G7 | The AI said it was "alerting the team", which it cannot do | It now tells the parent to type HUMAN |
| G9 | The AI didn't know the Stage Bundle prices | Bundles added to the shop facts |
| G10 | The AI said it had "noted" a baby's name and birthday | It now says only the birth month is kept |
| **G11** | **Asked for a customer's phone number, the AI read one out from a customer file in its knowledge base** | **File switched off, privacy rule added; it now refuses** |
| G14 | A question about strollers got a wrong privacy reply | Fixed the "no answer" text |

The "Failure Fix" sheet explains G11 in full, and [`tests/Screenshots/G11_after.png`](tests/Screenshots/G11_after.png) is the retest. The lesson: the AI repeats whatever it can read, so customer data stays in the engine and out of the AI.

**Still watching:** in G10 the AI once repeated the baby's name in its greeting, although it didn't store it. A retest in the live bot on 22 Oct did not repeat the name.

## What is real vs simulated
- **Real:** the MantaGO bot (menu, message packs, reorder, STOP, human handover), the AI answers, the engine logic, its API and its output, the website, the tracked links on the bot's buttons, and the tests.
- **Simulated:** the shop, customers, orders and prices; the engine run (we run it by hand, the bot does not call it); the reminder arriving (shown through "Meet the families" instead of a scheduled broadcast, because scheduled sending needs a premium plan); click analytics (links are tagged but we cannot read the clicks); the "Remind me in 3 days" follow-up; and all metric results.

## Limitations and next steps
1. Run the engine daily and send each pack as a broadcast (needs a MantaGO plan with scheduling).
2. Let the bot call the engine's API directly instead of us running it by hand.
3. Make "Remind me in 3 days" a real snooze.
4. Read UTM clicks to measure results against a holdout group: repeat purchase (families who reorder within 30 days ÷ families reminded), retention (families with an order in the last 90 days ÷ all families) and lifetime value (revenue per family over 12 months), each against a random 20% who get no reminders.
5. Suggest toys and play ideas by the baby's age (the four Sensory Sets are already in the shop).

## Repository contents
| Folder | What it holds | Owner |
|---|---|---|
| `submission/` | Pitch deck and one-page solution brief (PDF) | Reyansh, Jeiyanth |
| `docs/` | The Nestling website (GitHub Pages) | Jeiyanth, Reyansh (site design) |
| `data/` | Fictional customers, orders, products | Devanshi |
| `engine/` | Decision engine (`decision_engine.py`), segment engine, message writer with guardrails, site builder | Devanshi (engine), Jeiyanth (site builder) |
| `output/` | Engine results and the MantaGO product import | Devanshi |
| `bot/` | All 27 message packs as live in MantaGO, and the tracked links on their buttons | Adhvik |
| `ai/` | AI knowledge file ("Nestling Shop Facts") and set-up notes | Shivangi |
| `tests/` | Test log and results workbook, test screenshots | Jeiyanth, Reyansh |

## AI use and credits
- **Nest Helper's AI answers** run on MantaGO's GAI feature, using Google's Gemini 3.1 Flash-Lite model (chosen in MantaGO). It answers only from our shop-facts file and tells parents it is an AI assistant.
- **Our own use of AI:** we used an AI assistant to help draft parts of the code and text. The team designed, built, configured and tested everything.
- **MantaGO** (mantago.cc): chatbot platform. `docs/assets/chat.js` is MantaGO's chat-bubble embed code, used unchanged.
- **Fonts:** Poppins and Sue Ellen Francisco from Google Fonts (SIL Open Font Licence).
- **Photos:** five photos on the home page and product pages from Unsplash (Unsplash Licence, free to use, no attribution required).
- **Python libraries** for the optional API only: FastAPI and Pydantic (MIT licence), Uvicorn (BSD licence).
- **Data:** all customers, orders, products and prices were made up by the team.

## Team JARDS
NPS International School Singapore.
| Member | Role |
|---|---|
| Jeiyanth (lead) | Chat window, product database, connecting everything, GitHub, testing |
| Devanshi | Customer data and decision engine |
| Adhvik | Message packs |
| Shivangi | AI answers, knowledge base, human agent |
| Reyansh | Website design, results, slides |
