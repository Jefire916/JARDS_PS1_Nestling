# AI set-up (MantaGO GAI) – as it runs in the live bot

- **App:** MantaGO → Applications → GAI → "Nest Helper AI"
- **Model:** gemini-3.1-flash-lite (chosen in MantaGO)
- **Start the AI:** tap "Ask Nest Helper", or type ASK, ask AI, help, question, recommend, find (and similar)
- **Leave the AI:** type MENU, bye, done, exit, home or stop
- **Knowledge base:** `Nestling_Shop_Facts.md` (this folder), uploaded to MantaGO as a PDF. After any change to the file, upload the new PDF to MantaGO and switch the old one off. It is the single source of shop facts: products, prices, clothing and diaper sizes, offers, formula rules (SIFECS), delivery, returns, privacy.
- **Not in the knowledge base on purpose:** customer data. The AI does not need it (reminders come from the decision engine), and in testing it leaked a phone number when a customer file was included (see tests/ → Failure Fix).
- **Bot personality (GAI → Advanced):** warm, short answers; no medical or feeding advice; no formula brands or offers; emergencies → call 995 or type HUMAN; never share any customer's personal data.
- **Topics to avoid:** politics, violence, adult, gambling, formula promos, medical advice, discounts, personal data
- **When it has no answer:** "Sorry, I can't help with that one… type HUMAN to talk to a person."
- **Human handover:** type HUMAN or tap "Talk to a person" → MantaGO Live Chat mode; the team replies in Conversations.
