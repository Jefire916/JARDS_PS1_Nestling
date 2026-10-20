"""Writes bot/link_list.md: the exact URL for every Open-URL button in the message packs.
Run after changing the website address in data/products.csv:  python3 engine/make_link_list.py"""
import csv, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prod = {r["item_id"]: r for r in csv.DictReader(open(os.path.join(ROOT, "data", "products.csv")))}
def url(item, journey):
    return f'{prod[item]["url"]}?utm_source=livechat&utm_medium={journey}&utm_campaign=nestling_ai&utm_content={item}'
rows = [
 ("RF-DP3-UP-DP4", "Reorder Size 4", "DP-4", "refill"), ("RF-DP3-UP-DP4", "Stock up: 3 packs", "DP-4", "refill"),
 ("RF-DP3-UP-DP4", "Keep Size 3", "DP-3", "refill"),
 ("CARD-BN-3-6", "Buy in one tap", "BN-3-6", "sizeup"), ("CARD-BN-12-18", "Buy in one tap", "BN-12-18", "winback"),
 ("MP-RE-DIAPERS", "Reorder (Newborn card)", "DP-NB", "reorder"), ("MP-RE-DIAPERS", "Reorder (Size 1 card)", "DP-1", "reorder"),
 ("MP-RE-DIAPERS", "Reorder (Size 2 card)", "DP-2", "reorder"), ("MP-RE-DIAPERS", "Reorder (Size 3 card)", "DP-3", "reorder"),
 ("MP-RE-DIAPERS", "Reorder (Size 4 card)", "DP-4", "reorder"),
 ("MP-RE-WIPES", "Reorder (Water Wipes 80 card)", "WP-80", "reorder"), ("MP-RE-WIPES", "Reorder (3 Pack card)", "WP-3PK", "reorder"),
 ("MP-RE-MILK", "Reorder (Formula Stage 1 card)", "FM-1", "reorder"), ("MP-RE-MILK", "Reorder (Formula Stage 2 card)", "FM-2", "reorder"),
 ("MP-RE-MILK", "Reorder (Milk Stage 3 card)", "GM-3", "reorder"),
]
out = ["# Link list: new website links for every Open URL button", "",
       "Paste each link into the button's **Open URL** box, replacing the old `example.com` link.",
       "Do not retype it. Copy the whole line.", "",
       "| # | Pack | Button | New link |", "|---|---|---|---|"]
for i, (pack, btn, item, j) in enumerate(rows, 1):
    out.append(f"| {i} | {pack} | {btn} | `{url(item, j)}` |")
out += ["", "15 buttons in 6 packs. Nothing else in MantaGO uses a website link."]
open(os.path.join(ROOT, "bot", "link_list.md"), "w").write("\n".join(out) + "\n")
print("wrote", len(rows), "links")
