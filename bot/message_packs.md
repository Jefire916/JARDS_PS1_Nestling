# Nestling – Message Packs (build these in MantaGO)

Fictional shop for AI-GNITION 2026 (Team JARDS). Channel: website LiveChat.

**Version 2 (19 Oct): new warmer voice, "Why this message?" on every reminder, new website links. Packs already built only need EDITING, not rebuilding. See `CHANGES_FOR_ADHVIK.md` for the exact edits.**

## How to build a pack in MantaGO (checked on our bot, 16 Oct)

**Create a pack**

1. Open our bot in MantaGO. Under **Message Pack**, click **Add Intent**.
2. In **Message Pack Name**, type the pack name exactly as written in this doc (max 40 characters). Click **Confirm**.
3. The editor opens. The left purple bar has the blocks: **Text**, Image, Imagemap, **Card**, Video, Carousel, Location, file, More.
4. When the pack is finished, click **save** (top right). It changes to **Saved**.

**Add a text message**

- Click **Text** in the left bar, then type the text in the box (max 640 characters).
- Each "Text:" line in this doc is a separate Text block, in the same order.

**Add a card**

- Click **Card** in the left bar.
- Fill in **Enter Title** (max 40) and the description box under it ("Type here", max 60).
- Leave the picture box empty.
- Click **Add Button** under the card to add each button.
- For several cards in one message (the "carousel" packs), click the **+** to the right of the first card to add the next card. Don't use the Carousel block.

**Set up a button (on a card or text)**
Click **Add Button**. The "Actions" window opens.

1. **Button title:** type the button text (max 40).
2. Choose the action:
   - "→ open X" in this doc: click **Message Pack**, then **Select Conversation Module**, and pick pack X.
   - "→ link": click **Open URL** and paste the full link (see `link_list.md`). Ignore "Enable UTM" (it's a paid feature); the tracking is already inside our links.
   - "→ open Live Chat (Live Chat mode)": click **Live Chat mode**. Leave its two messages as they are.
   - "→ send keyword ASK (Keyword action)": click **Keyword** and type `ASK`.
3. Tag (if shown in [square brackets]): click **Add Tag**, type the tag name, then click **Add "TAG" Tag**.
4. Click **Confirm** (top right).

**Add a quick reply**
Quick replies are the small bubbles under the last message.

1. Click **+ Quick Reply** at the bottom of the editor.
2. **Button title** for quick replies is max **20** characters. The labels in this doc already fit.
3. Choose the action the same way as for buttons (Message Pack / Live Chat mode / Keyword). Quick replies have no Open URL.
4. Add the tag if shown, then click **Confirm**.

**Order to build in** (so the pack a button opens already exists):

1. MP-LATER, MP-QUIET, MP-STOP, MP-HUMAN
2. MP-DEMO and MP-MENU with their text only (no quick replies yet), then save
3. MP-EXCH, MP-UNKNOWN
4. NO-MSG-C05, NO-MSG-C07
5. CARD-BN-3-6, CARD-BN-12-18
6. MP-RE-DIAPERS, MP-RE-WIPES, MP-RE-MILK, then MP-REORDER
7. RF-DP3-UP-DP4, SU-0-3M-TO-3-6M, MS-12M, WB-12-18M
8. Go back into MP-DEMO and MP-MENU and add their quick replies, then save

**Rules**

- Copy the wording exactly. Don't change the formula cards (MP-RE-MILK); Singapore's SIFECS code bans offers or recommendations on infant formula.
- Name every pack exactly as written. The menu and keywords are linked by these names.
- Only build message packs. Don't change Keywords, Greeting message, Unknown message or GAI.
- When everything is done, go to the bot's main page and click **Update** (orange button). Nothing goes live on the website until you do.

## Link list

All website links now point to the Nestling shop site. The full list of 15 links is in `link_list.md`. Copy from there.

Example (Reorder Size 4 in the refill pack):
`https://jefire916.github.io/JARDS_PS1_Nestling/shop/diapers-4/?utm_source=livechat&utm_medium=refill&utm_campaign=nestling_ai&utm_content=DP-4`

---

## A. The 4 customer journeys (build first)

### RF-DP3-UP-DP4 (refill – customer C01)

1. Text: Hi! It's Nest Helper from Nestling 🐣
2. Text: Your Size 3 diapers should be running out around now. At 10 months, lots of babies move up to Size 4, so I've put both below.
3. Card
   - Title: Diapers Size 4 (60) · S$18
   - Description: Next size up. Buy 3, save 10%.
   - Button: Reorder Size 4 → link: diapers-4, refill, DP-4 [BUY] [J_REFILL]
   - Button: Stock up: 3 packs → link: diapers-4, refill, DP-4 [BUY]
   - Button: Keep Size 3 → link: diapers-3, refill, DP-3 [BUY]
4. Quick replies: Remind me in 3 days → open MP-LATER · Why this message? → open WHY-RF · Stop messages → open MP-STOP [OPT_OUT]

### SU-0-3M-TO-3-6M (size-up – customer C02)

1. Text: Hi! It's Nest Helper from Nestling 🐣
2. Text: Your little one is nearly 3 months, and 0-3M clothes usually get snug around now. How's the fit?
3. Quick replies: Getting snug → open CARD-BN-3-6 [J_SIZEUP] · Still fits → open MP-LATER · Why this message? → open WHY-SU · Stop messages → open MP-STOP [OPT_OUT]

### CARD-BN-3-6

1. Card
   - Title: Stage Bundle 3-6M · S$52
   - Description: Bodysuits, sleepsuit, Size 2 diapers. Free exchange.
   - Button: Buy in one tap → link: bundle-3-6m, sizeup, BN-3-6 [BUY]
   - Button: How exchange works → open MP-EXCH
   - Button: Not now → open MP-QUIET

### MS-12M (milestone – first birthday)

1. Text: Hi! It's Nest Helper from Nestling 🐣
2. Text: Happy first-birthday month to your little one! 🎂
3. Text: To celebrate: free delivery on your next order in the next 7 days. On us 😉
4. Quick replies: See 12-18M bundle → open CARD-BN-12-18 [J_MILESTONE] · All set, thanks → open MP-QUIET · Why this message? → open WHY-MS · Stop messages → open MP-STOP [OPT_OUT]

### WB-12-18M (win-back – customer C04)

1. Text: Hi! It's Nest Helper from Nestling 🐣
2. Text: It's been a while, and we've missed you! Your little one is probably in 12-18M sizes by now.
3. Text: Welcome back: free delivery on your next order in the next 14 days.
4. Quick replies: See 12-18M bundle → open CARD-BN-12-18 [J_WINBACK] · All set, thanks → open MP-QUIET · Why this message? → open WHY-WB · Stop messages → open MP-STOP [OPT_OUT]

### CARD-BN-12-18

1. Card
   - Title: Stage Bundle 12-18M · S$62
   - Description: Tees, shorts, sleepsuit, Size 4 diapers. Free exchange.
   - Button: Buy in one tap → link: bundle-12-18m, winback, BN-12-18 [BUY]
   - Button: How exchange works → open MP-EXCH
   - Button: Not now → open MP-QUIET

## B. The "no message" customers (shows the bot holds back)

### NO-MSG-C05

1. Text: This family didn't agree to reminders, so Nest Helper stays quiet and sends them nothing. No consent, no message.
2. Quick reply: Back to families → open MP-DEMO

### NO-MSG-C07

1. Text: This family's formula is due, but Nest Helper never starts a message about infant formula. Singapore's SIFECS code bans promoting it. Parents can still type REORDER themselves.
2. Quick reply: Back to families → open MP-DEMO

## C. The families menu (stands in for the reminder arriving)

### MP-DEMO

1. Text: Meet six families Nestling looks after. Tap one to see what Nest Helper would send them today, or why it stays quiet.
2. Quick replies:
   - Diapers running low → open RF-DP3-UP-DP4
   - Outgrowing clothes → open SU-0-3M-TO-3-6M
   - First birthday → open MS-12M
   - Been a while → open WB-12-18M
   - Didn't opt in → open NO-MSG-C05
   - Formula is due → open NO-MSG-C07

## D. Shared packs

### MP-MENU (used as the Greeting message)

1. Text: Hi, welcome to Nestling! 🐣 I'm Nest Helper, the shop's AI assistant.
2. Text: Sizes, top-ups, a question at 2am… I've got you. What can I help with?
3. Quick replies:
   - Meet the families → open MP-DEMO
   - Reorder → open MP-REORDER
   - Ask Nest Helper → send keyword ASK (Keyword action)
   - Talk to a person → open Live Chat (Live Chat mode) [HUMAN]
   - Stop messages → open MP-STOP [OPT_OUT]

### MP-REORDER

1. Text: Sure! What would you like to reorder?
2. Quick replies: Diapers → open MP-RE-DIAPERS · Wipes → open MP-RE-WIPES · Formula or milk → open MP-RE-MILK

### MP-RE-DIAPERS (carousel, 5 cards)
Each card has one button "Reorder" → link (journey = reorder) [BUY].

| Card title | Description | Link |
|---|---|---|
| Diapers Newborn · S$14 | Pack of 60. Buy 3, save 10%. | diapers-nb, DP-NB |
| Diapers Size 1 · S$16 | Pack of 70. Buy 3, save 10%. | diapers-1, DP-1 |
| Diapers Size 2 · S$17 | Pack of 70. Buy 3, save 10%. | diapers-2, DP-2 |
| Diapers Size 3 · S$18 | Pack of 66. Buy 3, save 10%. | diapers-3, DP-3 |
| Diapers Size 4 · S$18 | Pack of 60. Buy 3, save 10%. | diapers-4, DP-4 |

### MP-RE-WIPES (carousel, 2 cards)
Each card has one button "Reorder" → link (journey = reorder) [BUY].

| Card title | Description | Link |
|---|---|---|
| Water Wipes 80 · S$4 | 80 wipes. Buy 3, save 10%. | wipes-80, WP-80 |
| Water Wipes 3 Pack · S$11 | 240 wipes. Buy 3, save 10%. | wipes-3pk, WP-3PK |

### MP-RE-MILK (carousel, 3 cards) – formula rules apply

1. Text: Here are the formulas and milk we stock, at our usual prices. We don't recommend brands or give feeding advice. Your doctor or nurse can help you choose.
2. Carousel. Every card description is exactly: Usual price. No offers apply. Each card has one button "Reorder" → link (journey = reorder) [BUY].

| Card title | Link |
|---|---|
| Infant Formula Stage 1 · S$45 | formula-stage-1, FM-1 |
| Follow-on Formula Stage 2 · S$43 | formula-stage-2, FM-2 |
| Growing-up Milk Stage 3 · S$38 | milk-stage-3, GM-3 |

Never add "save 10%", "stock up" or any offer to these three cards.

### MP-EXCH

1. Text: Clothes not fitting? No stress. Swap them for another size free within 30 days, unworn with tags. Delivery is free both ways.
2. Quick replies: Start an exchange → open Live Chat (Live Chat mode) [HUMAN] · Menu → open MP-MENU

### MP-LATER

1. Text: Okay! I'll remind you in 3 days. Type STOP anytime.

### MP-QUIET

1. Text: No problem. I'll leave you in peace for 7 days. Type MENU whenever you need me.

### MP-STOP

1. Text: Done. No more reminders from Nestling. I'm still here whenever you want to chat.

### MP-HUMAN (opened by the keyword HUMAN)

1. Text: Of course. I'm getting a Nestling team member for you. They can see this chat, so you won't need to repeat yourself. Hours: Mon–Fri, 9am–6pm.
2. Quick reply: Talk to a person → open Live Chat (Live Chat mode) [HUMAN]

### MP-UNKNOWN (used as the Unknown message)

1. Text: Hmm, I didn't quite get that. Could you say it another way? Or pick one below 👇
2. Quick replies: Ask Nest Helper → send keyword ASK (Keyword action) · Talk to a person → open Live Chat (Live Chat mode) [HUMAN] · Menu → open MP-MENU

## E. NEW: the "Why this message?" packs (4 small packs)

Each reminder pack has a **Why this message?** quick reply that opens one of these. They tell the parent exactly which data was used. Build these four, then add the quick reply to the 4 reminder packs.

### WHY-RF

1. Text: Good question! Here's exactly what I used:
2. Text: When you last ordered this and how often you reorder it, to guess when it runs out. Your baby's age band, to check the size. And you said yes to reminders.
3. Text: That's all. I never use your name, photos or address. Type STOP and I'll go quiet for good.
4. Quick replies: Menu → open MP-MENU · Stop messages → open MP-STOP [OPT_OUT]

### WHY-SU

1. Text: Good question! Here's exactly what I used:
2. Text: Your baby's age band, and the clothing size you bought last. Together they tell me when the next size is usually needed. And you said yes to reminders.
3. Text: That's all. I never use your name, photos or address. Type STOP and I'll go quiet for good.
4. Quick replies: Menu → open MP-MENU · Stop messages → open MP-STOP [OPT_OUT]

### WHY-MS

1. Text: Good question! Here's exactly what I used:
2. Text: Your baby's age band: this month they reach a milestone. And you said yes to reminders. The free delivery is our thank-you, with no catch.
3. Text: That's all. I never use your name, photos or address. Type STOP and I'll go quiet for good.
4. Quick replies: Menu → open MP-MENU · Stop messages → open MP-STOP [OPT_OUT]

### WHY-WB

1. Text: Good question! Here's exactly what I used:
2. Text: You've ordered from us before but not for a while, and your baby's age band suggests sizes that fit now. And you said yes to reminders.
3. Text: That's all. I never use your name, photos or address. Type STOP and I'll go quiet for good.
4. Quick replies: Menu → open MP-MENU · Stop messages → open MP-STOP [OPT_OUT]

---

## Checklist (tick when built)

After all 24 are ticked: click **Update** on the bot's main page and tell Jeiyanth "packs done".


| # | Pack | Built | Every button tested |
|---|---|---|---|
| 1 | RF-DP3-UP-DP4 | ☐ | ☐ |
| 2 | SU-0-3M-TO-3-6M | ☐ | ☐ |
| 3 | CARD-BN-3-6 | ☐ | ☐ |
| 4 | MS-12M | ☐ | ☐ |
| 5 | WB-12-18M | ☐ | ☐ |
| 6 | CARD-BN-12-18 | ☐ | ☐ |
| 7 | NO-MSG-C05 | ☐ | ☐ |
| 8 | NO-MSG-C07 | ☐ | ☐ |
| 9 | MP-DEMO | ☐ | ☐ |
| 10 | MP-MENU | ☐ | ☐ |
| 11 | MP-REORDER | ☐ | ☐ |
| 12 | MP-RE-DIAPERS | ☐ | ☐ |
| 13 | MP-RE-WIPES | ☐ | ☐ |
| 14 | MP-RE-MILK | ☐ | ☐ |
| 15 | MP-EXCH | ☐ | ☐ |
| 16 | MP-LATER | ☐ | ☐ |
| 17 | MP-QUIET | ☐ | ☐ |
| 18 | MP-STOP | ☐ | ☐ |
| 19 | MP-HUMAN | ☐ | ☐ |
| 20 | MP-UNKNOWN | ☐ | ☐ |
| 21 | WHY-RF | ☐ | ☐ |
| 22 | WHY-SU | ☐ | ☐ |
| 23 | WHY-MS | ☐ | ☐ |
| 24 | WHY-WB | ☐ | ☐ |
