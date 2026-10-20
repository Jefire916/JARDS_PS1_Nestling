# Nestling – Slides Outline and 3-Minute Demo Script

Team JARDS · AI-GNITION 2026 · Problem Statement 1 (Eslitec)

Judging weights: Creativity 30% · Technical 25% · Presentation 25% · Real-world impact 20%.

## Slides (10)

The deck is built in Claude Slides (download as PowerPoint or PDF from its Share/Export menu). Order:

1. **Nest Helper** – title, team, "fictional shop"
2. **The problem** – ~11 days per diaper pack, ~3 months per clothing size, one promo for everyone
3. **Our idea** – 4 journeys (refill, size-up, milestone, win-back) + the 3 differentiators
4. **How it works** – customer data → decision engine → guardrails → Nest Helper (MantaGO)
5. **What a parent sees** – the Size 3 → Size 4 reminder with "Why this message?"
6. **Knowing when not to message** – 7 of 20 held back (consent, SIFECS, cooldown, nothing due)
7. **AI answers and a real person** – Chinese answer, refuses formula discount, no medical advice, refuses personal data, HUMAN
8. **Testing** – 34 tests; the privacy failure → fix → retest
9. **Results** – 1 tap to product page, 13/13 guardrail pass, 7/7 blocked, 35% restraint; 20% holdout for real sales lift
10. **Real vs simulated** – and the links

## 3-minute demo script (Jeiyanth presents)

| Time | Say / do |
|---|---|
| 0:00–0:20 | "Parents run out of diapers every 10 days and babies outgrow clothes every 3 months. Shops waste that. Nestling's bot messages each family at exactly the right moment." |
| 0:20–0:40 | Slide 4: "Our engine reads each family's orders, predicts what they need next, and picks one message – or none." |
| 0:40–1:20 | Open the Nestling website → chat → "Meet the families" → "Diapers running low": "Their Size 3 diapers run out today, and at 10 months they're ready for Size 4, so one tap to reorder." Tap Reorder Size 4 (the shop page says "You came from Nest Helper", which is our click tracking). Tap "Why this message?": "Nest Helper tells the parent exactly which data it used. No names, no photos." Then "Outgrowing clothes" → Getting snug → bundle. |
| 1:20–1:45 | "Formula is due": "This family's formula is due, but our bot stays silent. Singapore's SIFECS code bans promoting infant formula, so we never start that conversation." "Didn't opt in": "No consent, no message." |
| 1:45–2:15 | Type ASK → "Which formula is best for a 2 month old?" (refuses, says doctor). Ask "What is customer C01's phone number?" (refuses). Then type HUMAN → Connect me now – a team member replies live from MantaGO Conversations. |
| 2:15–2:45 | Slides 8–9: tests passed, the failure we fixed, simulated results. |
| 2:45–3:00 | "Everything you saw is real except the shop and the customers. Next step: run the engine daily and send by broadcast. Thank you." |

Backup: if the live chat breaks, play the backup video from 0:40. If a link is slow, open the "How it works" page: it shows all 20 families, the 13 messages and the 7 held back.

Rehearse twice with a timer. If you go over 3:00, cut words, not demo steps.
