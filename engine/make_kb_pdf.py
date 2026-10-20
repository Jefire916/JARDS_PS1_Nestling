"""Render ai/Nestling_Shop_Facts.md to ai/Nestling_Shop_Facts.pdf (uploaded to MantaGO GAI knowledge base)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from xml.sax.saxutils import escape
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
st = getSampleStyleSheet()
lines = open(os.path.join(ROOT, 'ai/Nestling_Shop_Facts.md'), encoding='utf-8').read().splitlines()
story, tbl = [], []
def flush():
    global tbl
    if tbl:
        rows = [[c.strip() for c in r.strip('|').split('|')] for r in tbl if not set(r.replace('|', '').strip()) <= set('-')]
        t = Table(rows); t.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.grey), ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue), ('FONTSIZE', (0, 0), (-1, -1), 9)]))
        story.extend([t, Spacer(1, 6)]); tbl = []
for l in lines:
    if l.startswith('|'): tbl.append(l); continue
    flush()
    if not l.strip(): story.append(Spacer(1, 4))
    elif l.startswith('### '): story.append(Paragraph(escape(l[4:]), st['Heading3']))
    elif l.startswith('## '): story.append(Paragraph(escape(l[3:]), st['Heading2']))
    elif l.startswith('# '): story.append(Paragraph(escape(l[2:]), st['Title']))
    elif l.startswith('- '): story.append(Paragraph('• ' + escape(l[2:]), st['BodyText']))
    else: story.append(Paragraph(escape(l), st['BodyText']))
flush()
SimpleDocTemplate(os.path.join(ROOT, 'ai/Nestling_Shop_Facts.pdf'), pagesize=A4, title='Nestling Shop Facts').build(story)
print('ok')
