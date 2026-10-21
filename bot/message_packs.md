# Nest Helper: message packs (as live in MantaGO)

Bot: "Nest Helper (JARDS)", MantaGO bot ID `olejqMRdj`, on the website's LiveChat bubble.
27 message packs. Every reminder offers "Why this message?", "Stop messages" and a way to wait or say no.

How a pack's parts are written below:
- **Text**: one chat bubble.
- **Card**: a product card with a title, a short description and buttons.
- **Buttons / quick replies**: "→ PACK" opens that pack; "→ link" opens a product page on the website (the full tracked links are in [`link_list.md`](link_list.md)); "→ person" hands the chat to a team member (MantaGO Live Chat mode); "→ AI" starts the AI answers (keyword ASK).
- **[tag]** means the tap also adds a tag to the customer (BUY, OPT_OUT, HUMAN or the journey), so the team can see what happened.

## Keywords and set-up

| Typed by the parent | Opens |
|---|---|
| (first message) | Consent request, set as the Greeting message |
| MENU | MP-MENU |
| DEMO | MP-DEMO |
| REORDER | MP-REORDER |
| HUMAN | MP-HUMAN |
| STOP | MP-STOP |
| ASK (or "help", "question", "recommend") | AI answers (see [`../ai/README.md`](../ai/README.md)) |
| anything the bot doesn't understand | MP-UNKNOWN, set as the Unknown message |

## 1. Consent (first thing every parent sees)

### Consent request
- Text: Hi, welcome to Nestling! 🐣 I'm Nest Helper, the shop's AI assistant. Can I send you the odd reminder, like when diapers are running low or your baby is ready for the next size? I never send reminders about infant formula. Type STOP any time.
- Buttons: Yes → CONSENT-YES · No → CONSENT-NO

### CONSENT-YES
- Text: Great, you're in! I'll only message when something's actually useful. What can I help with now?
- Quick replies: Meet the families → MP-DEMO · Reorder → MP-REORDER · Ask Nest Helper → AI · Talk to a person → person · Stop messages → MP-STOP [tag]

### CONSENT-NO
- Text: No problem, I won't send you reminders. I'm still here whenever you need me. What can I help with?
- Quick replies: the same five as CONSENT-YES.

## 2. The reminders (one per journey)

The decision engine picks which family gets which reminder. In the demo, "Meet the families" (MP-DEMO) shows each one, because our MantaGO plan cannot send messages on a schedule.

### RF-DP3-UP-DP4 (refill, family C01)
- Text: Hi! It's Nest Helper from Nestling 🐣
- Text: Your Size 3 diapers should be running out around now. At 10 months, lots of babies move up to Size 4, so I've put both below.
- Card: **Diapers Size 4 (60) · S$18**, "Next size up. Buy 3, save 10%"
  - Reorder Size 4 → link (Size 4 diapers)
  - Stock up: 3 packs → link (Size 4 diapers)
  - Keep Size 3 → link (Size 3 diapers)
- Quick replies: Remind me in 3 days → MP-LATER · Stop messages → MP-STOP [tag] · Why this message? → WHY-RF

### SU-0-3M-TO-3-6M (size-up, family C02)
- Text: Hi! It's Nest Helper from Nestling 🐣
- Text: Your little one is nearly 3 months, and 0-3M clothes usually get snug around now. How's the fit?
- Quick replies: Getting snug → CARD-BN-3-6 [tag] · Still fits → MP-LATER · Stop messages → MP-STOP [tag] · Why this message? → WHY-SU

### MS-12M (milestone, family C03)
- Text: Hi! It's Nest Helper from Nestling 🐣
- Text: Happy first-birthday month to your little one! 🎂
- Text: To celebrate: free delivery on your next order in the next 7 days. On us 😉
- Quick replies: See 12-18M bundle → CARD-BN-12-18 [tag] · All set, thanks → MP-QUIET · Stop messages → MP-STOP [tag] · Why this message? → WHY-MS

### WB-12-18M (win-back, family C04)
- Text: Hi! It's Nest Helper from Nestling 🐣
- Text: It's been a while, and we've missed you! Your little one is probably in 12-18M sizes by now.
- Text: Welcome back: free delivery on your next order in the next 14 days.
- Quick replies: See 12-18M bundle → CARD-BN-12-18 [tag] · All set, thanks → MP-QUIET · Stop messages → MP-STOP [tag] · Why this message? → WHY-WB

### CARD-BN-3-6
- Card: **Stage Bundle 3-6M · S$52**, "Bodysuits, sleepsuit, Size 2 diapers. Free exchange."
  - Buy in one tap → link (3-6M bundle) · How exchange works → MP-EXCH · Not now → MP-QUIET

### CARD-BN-12-18
- Card: **Stage Bundle 12-18M · S$62**, "Tees, shorts, sleepsuit, Size 4 diapers. Free exchange."
  - Buy in one tap → link (12-18M bundle) · How exchange works → MP-EXCH · Not now → MP-QUIET

## 3. When Nest Helper stays quiet

### NO-MSG-C05 (no consent)
- Text: This family didn't agree to reminders, so Nest Helper stays quiet and sends them nothing. No consent, no message.
- Quick reply: Back to families → MP-DEMO

### NO-MSG-C07 (infant formula, SIFECS)
- Text: This family's formula is due, but Nest Helper never starts a message about infant formula. Singapore's SIFECS code bans promoting it. Parents can still type REORDER themselves.
- Quick reply: Back to families → MP-DEMO

## 4. "Why this message?"

Each one says exactly which data was used.

| Pack | Second bubble (the data used) |
|---|---|
| WHY-RF | When you last ordered this and how often you reorder it, to guess when it runs out. Your baby's age band, to check the size. And you said yes to reminders. |
| WHY-SU | Your baby's age band, and the clothing size you bought last. Together they tell me when the next size is usually needed. And you said yes to reminders. |
| WHY-MS | Your baby's age band: this month they reach a milestone. And you said yes to reminders. The free delivery is our thank-you, with no catch. |
| WHY-WB | You've ordered from us before but not for a while, and your baby's age band suggests sizes that fit now. And you said yes to reminders. |

All four start with "Good question! Here's exactly what I used:" and end with "That's all. I never use your name, photos or address. Type STOP and I'll go quiet." (WHY-SU says "go quiet for good".) Quick replies: Stop messages → MP-STOP [tag] · Menu → MP-MENU [tag].

## 5. Menu, families and reorder

### MP-MENU
- Text: Sizes, top-ups, a question at 2am… I've got you. We sell clothes, diapers, wipes and toys. What can I help with?
- Quick replies: Meet the families → MP-DEMO · Reorder → MP-REORDER · Ask Nest Helper → AI · Talk to a person → person · Stop messages → MP-STOP [tag]

### MP-DEMO ("Meet the families")
- Text: Meet six families Nestling looks after. Tap one to see what Nest Helper would send them today, or why it stays quiet.
- Quick replies: Diapers running low → RF-DP3-UP-DP4 · Outgrowing clothes → SU-0-3M-TO-3-6M · First birthday → MS-12M · Been a while → WB-12-18M · Didn't opt in → NO-MSG-C05 · Formula is due → NO-MSG-C07

### MP-REORDER
- Text: Sure! What would you like to reorder?
- Quick replies: Diapers → MP-RE-DIAPERS [tag] · Wipes → MP-RE-WIPES [tag] · Formula or milk → MP-RE-MILK

### MP-RE-DIAPERS (5 cards, each with a "Reorder" link)
| Card | Description |
|---|---|
| Diapers Newborn · S$14 | Pack of 60. Buy 3, save 10% |
| Diapers Size 1 · S$16 | Pack of 70. Buy 3, save 10% |
| Diapers Size 2 · S$17 | Pack of 70. Buy 3, save 10% |
| Diapers Size 3 · S$18 | Pack of 66. Buy 3, save 10% |
| Diapers Size 4 · S$18 | Pack of 60. Buy 3, save 10% |

### MP-RE-WIPES (2 cards, each with a "Reorder" link)
| Card | Description |
|---|---|
| Water Wipes 80 · S$4 | 80 wipes. Buy 3, save 10% |
| Water Wipes 3 Pack · S$11 | 240 wipes. Buy 3, save 10% |

### MP-RE-MILK (formula rules apply)
- Text: Here are the formulas and milk we stock, at our usual prices. We don't recommend brands or give feeding advice. Your doctor or nurse can help you choose.
- 3 cards, each "Usual price. No offers apply." with a "Reorder" link: Infant Formula Stage 1 · S$45, Follow-on Formula Stage 2 · S$43, Growing-up Milk Stage 3 · S$38.
- No discount, bundle, "stock up" or recommendation appears on these cards (SIFECS).

## 6. Control packs

| Pack | Text | Quick replies |
|---|---|---|
| MP-LATER | Okay, I'll hold off for 3 days. (In this demo, reminders are simulated.) Type STOP anytime. | – |
| MP-QUIET | No problem. I'll leave you in peace for 7 days. Type MENU whenever you need me. | – |
| MP-STOP | Done. No more reminders from Nestling. I'm still here whenever you want to chat. | – |
| MP-EXCH | Clothes not fitting? No stress. Swap them for another size free within 30 days, unworn with tags. Delivery is free both ways. | Start an exchange → person · Menu → MP-MENU |
| MP-HUMAN | Of course. Tap "Connect me now" and a Nestling team member will join this chat. They can see everything, so you won't need to repeat yourself. Hours: Mon–Fri, 9am–6pm. | Connect me now → person |
| MP-UNKNOWN | Hmm, I didn't quite get that. Could you say it another way? Or pick one below 👇 | Ask Nest Helper → AI · Talk to a person → person · Menu → MP-MENU |
