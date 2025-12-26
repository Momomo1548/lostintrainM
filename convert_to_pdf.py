from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
import os

INPUT_FILE = 'resources.html'
OUTPUT_DIR = 'assets'
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'procesverhaal.pdf')

GITHUB_URL = 'https://github.com/Momomo1548/lostintrainM'

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'lxml')

section = soup.find('section')
if not section:
    print('Geen <section> gevonden in resources.html')
    exit(1)

# Collect title and paragraphs
elements = []
for child in section.find_all(['h2', 'p']):
    tag = child.name
    text = child.get_text(strip=True)
    if text:
        elements.append((tag, text))

os.makedirs(OUTPUT_DIR, exist_ok=True)

styles = getSampleStyleSheet()
style_h = styles['Heading2']
style_p = styles['BodyText']

# Build story
story = []
for tag, text in elements:
    if tag == 'h2':
        story.append(Paragraph(text, style_h))
        story.append(Spacer(1, 6))
    else:
        story.append(Paragraph(text, style_p))
        story.append(Spacer(1, 6))

if not story:
    print('Geen inhoud gevonden om te exporteren')
    exit(1)


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    # Header: left title
    canvas.setFont('Helvetica-Bold', 12)
    canvas.drawString(40, height - 30, 'Procesverhaal')
    # Optional thin line under header
    canvas.setLineWidth(0.5)
    canvas.line(40, height - 36, width - 40, height - 36)

    # Footer: left copyright, right GitHub link
    canvas.setFont('Helvetica', 8)
    canvas.drawString(40, 20, '\u00A9 2023 Projectdocumentatie | Lost in Tra(i)nslation')
    github_text = 'GITHUB: ' + GITHUB_URL
    text_width = canvas.stringWidth(github_text, 'Helvetica', 8)
    canvas.drawString(width - 40 - text_width, 20, github_text)

    canvas.restoreState()

from reportlab.lib.pagesizes import A4 as PAGESIZE
from reportlab.platypus import PageBreak

doc = BaseDocTemplate(OUTPUT_FILE, pagesize=PAGESIZE,
                      leftMargin=40, rightMargin=40, topMargin=60, bottomMargin=40)
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 20, id='normal')
template = PageTemplate(id='with-header-footer', frames=[frame], onPage=header_footer)
doc.addPageTemplates([template])

try:
    doc.build(story)
    print('PDF aangemaakt:', OUTPUT_FILE)
except Exception as e:
    print('Fout bij PDF generatie:', e)
    exit(1)
