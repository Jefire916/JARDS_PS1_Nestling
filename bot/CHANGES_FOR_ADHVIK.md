# Changes for the message packs (Adhvik)

Nothing to rebuild. Open each pack that already exists, change only what is listed, click **save**.
Total: about 27 small text edits, 4 new small packs, 4 new quick replies, 15 links. About 45 minutes.

Order matters: do **Part A**, then **Part B** (so the new packs exist), then **Part C**, then **Part D**.

## Part A. Edit the wording of existing packs

Open the pack, click the Text block, delete the old words, paste the new ones.

| Pack | Block | Old | New |
|---|---|---|---|
| MP-MENU | Text 1 | Hi! I'm Nest Helper, Nestling's AI assistant. Nestling is a demo shop… | Hi, welcome to Nestling! 🐣 I'm Nest Helper, the shop's AI assistant. |
| MP-MENU | Text 2 | What do you need? | Sizes, top-ups, a question at 2am… I've got you. What can I help with? |
| MP-MENU | Quick reply | Demo customers | Meet the families |
| MP-MENU | Quick reply | Ask a question | Ask Nest Helper |
| MP-DEMO | Text 1 | Demo: pick a customer to see… | Meet six families Nestling looks after. Tap one to see what Nest Helper would send them today, or why it stays quiet. |
| MP-DEMO | Quick reply 1 | C01 Diapers low | Diapers running low |
| MP-DEMO | Quick reply 2 | C02 Outgrowing | Outgrowing clothes |
| MP-DEMO | Quick reply 3 | C03 1st birthday | First birthday |
| MP-DEMO | Quick reply 4 | C04 Not back yet | Been a while |
| MP-DEMO | Quick reply 5 | C05 No consent | Didn't opt in |
| MP-DEMO | Quick reply 6 | C07 Formula due | Formula is due |
| RF-DP3-UP-DP4 | Text 1 | Hi! Nest Helper here, Nestling's AI assistant (demo shop). | Hi! It's Nest Helper from Nestling 🐣 |
| RF-DP3-UP-DP4 | Text 2 | Your Size 3 diapers usually run out about now. At 10 months, many babies move up to Size 4. | Your Size 3 diapers should be running out around now. At 10 months, lots of babies move up to Size 4, so I've put both below. |
| SU-0-3M-TO-3-6M | Text 1 | (same intro as above) | Hi! It's Nest Helper from Nestling 🐣 |
| SU-0-3M-TO-3-6M | Text 2 | Your baby is nearly 3 months. 0-3M clothes are usually outgrown around now. How's the fit? | Your little one is nearly 3 months, and 0-3M clothes usually get snug around now. How's the fit? |
| MS-12M | Text 1 | (same intro as above) | Hi! It's Nest Helper from Nestling 🐣 |
| WB-12-18M | Text 1 | (same intro as above) | Hi! It's Nest Helper from Nestling 🐣 |
| WB-12-18M | Text 2 | It's been a while! Your little one is probably in 12-18M sizes now. | It's been a while, and we've missed you! Your little one is probably in 12-18M sizes by now. |
| NO-MSG-C05 | Text 1 | Customer C05: no reminder today… (Demo explanation) | This family didn't agree to reminders, so Nest Helper stays quiet and sends them nothing. No consent, no message. |
| NO-MSG-C05 | Quick reply | Back to demo | Back to families |
| NO-MSG-C07 | Text 1 | Customer C07: formula is due… (Demo explanation) | This family's formula is due, but Nest Helper never starts a message about infant formula. Singapore's SIFECS code bans promoting it. Parents can still type REORDER themselves. |
| NO-MSG-C07 | Quick reply | Back to demo | Back to families |
| MP-REORDER | Text 1 | What would you like to reorder? | Sure! What would you like to reorder? |
| MP-EXCH | Text 1 | If clothes don't fit, exchange them… | Clothes not fitting? No stress. Swap them for another size free within 30 days, unworn with tags. Delivery is free both ways. |
| MP-QUIET | Text 1 | No problem. I won't message you for 7 days. Type MENU anytime. | No problem. I'll leave you in peace for 7 days. Type MENU whenever you need me. |
| MP-STOP | Text 1 | Done. You won't get any more reminders from Nestling. You can still chat here anytime. | Done. No more reminders from Nestling. I'm still here whenever you want to chat. |
| MP-HUMAN | Text 1 | Connecting you to a Nestling team member… | Of course. I'm getting a Nestling team member for you. They can see this chat, so you won't need to repeat yourself. Hours: Mon–Fri, 9am–6pm. |
| MP-UNKNOWN | Text 1 | Sorry, I didn't catch that. | Hmm, I didn't quite get that. Could you say it another way? Or pick one below 👇 |
| MP-UNKNOWN | Quick reply | Ask a question | Ask Nest Helper |

Leave these alone: MP-LATER, MP-RE-DIAPERS, MP-RE-WIPES, MP-RE-MILK (formula rules), CARD-BN-3-6, CARD-BN-12-18 text.

## Part B. Build 4 new packs

Full wording is in `message_packs.md`, section **E**. Each has 3 Text blocks and 2 quick replies.
Names must be exact: `WHY-RF`, `WHY-SU`, `WHY-MS`, `WHY-WB`.
Quick replies in all four: **Menu** → open MP-MENU, **Stop messages** → open MP-STOP (tag OPT_OUT).

Tip: build WHY-RF, then use the pack's copy option (⋮ menu) for the other three and just change Text 2.

## Part C. Add one quick reply to 4 packs

In each pack click **+ Quick Reply**, title `Why this message?` (17 characters), action **Message Pack**, pick the pack, **Confirm**, then save.

| Pack | Opens |
|---|---|
| RF-DP3-UP-DP4 | WHY-RF |
| SU-0-3M-TO-3-6M | WHY-SU |
| MS-12M | WHY-MS |
| WB-12-18M | WHY-WB |

## Part D. Replace the 15 website links

The old links go to a blank example.com page. Open `link_list.md`. For each row: open the pack, click the button, **Open URL**, delete the old link, paste the new one from the list, **Confirm**, save.

Packs: RF-DP3-UP-DP4 (3 buttons), CARD-BN-3-6 (1), CARD-BN-12-18 (1), MP-RE-DIAPERS (5), MP-RE-WIPES (2), MP-RE-MILK (3).

The links only work after Jeiyanth switches the website on (GitHub Pages). Paste them anyway. Check one by clicking it afterwards.

## When you finish

Click **Update** on the bot page, then tell Jeiyanth "packs v2 done".
