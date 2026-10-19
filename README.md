# Nestling – Nest Helper (Team JARDS, AI-GNITION 2026, Problem Statement 1)

> **Fictional shop. Simulated data.** Nestling is not a real business. Every customer, order and result here is invented for the competition.

**Live site:** https://jefire916.github.io/JARDS_PS1_Nestling/

## What it is
Nest Helper is a MantaGO chatbot for a fictional baby shop, Nestling. It uses customer data to send each family one personal message at the right time (refill, size-up, milestone or win-back), lets parents reorder in one or two taps, answers questions with AI in the parent's own language, and hands over to a real person when needed.

What makes it different:
1. **Written for each baby.** Messages use the baby's age band and past purchases. We store no names, photos or addresses.
2. **"Why this message?"** Every reminder has a button that tells the parent exactly which data was used.
3. **Guardrails before anything is sent.** A check blocks any message that promotes infant formula (Singapore's SIFECS code), pressures the parent, gives health advice, includes personal data or hides that it is an AI.

## Try the bot
Open the live site and click the chat bubble (bottom right).

| Tap or type | What happens |
|---|---|
| **Meet the families** | See the reminder the engine chose for each family, or why it stays quiet |
| `REORDER` | Reorder past items |
| `ASK` | Ask the AI a question (try Chinese or Malay) |
| `HUMAN` | Talk to a person |
| `STOP` | Stop reminders |

The page **How it works** shows all 20 families, the 13 messages sent and the 7 held back, with the reason for each.

## Repository contents
| Folder | What's in it | Owner |
|---|---|---|
| `docs/` | The Nestling website (served by GitHub Pages) with the chat window | Jeiyanth |
| `database/` | Product list imported into MantaGO (Database → Item Management) | Jeiyanth |
| `data/`, `engine/`, `output/` | Customer data, decision engine, message writer and guardrails | Devanshi |
| `bot/` | Message packs | Adhvik |
| `ai/` | AI set-up and knowledge base | Shivangi |
| `tests/`, `slides/` | Test log, results, slides, screenshots | Reyansh |

## What is real and what is simulated
**Real:** the decision engine, the chatbot in MantaGO, the AI answers and their safety rules, human handover, the tracking links on every button.
**Simulated:** the shop, customers and orders. We run the engine by hand, and a reminder appears in the chat when you pick a family, because we are not connected to a real messaging account. Checkout is switched off.

## Team JARDS
| Member | Role |
|---|---|
| Jeiyanth | Lead, website and chat window, product database, connecting the bot, GitHub |
| Devanshi | Customer data and decision engine |
| Adhvik | Message packs |
| Shivangi | AI answers, knowledge base, human agent |
| Reyansh | Testing, slides, results |

## AI use declaration
We used AI tools to help draft parts of the content and code. The team reviewed, built, configured and tested everything in MantaGO. In a live shop a language model would draft each reminder per family; the guardrail check shown here would run on every draft in exactly the same way.
