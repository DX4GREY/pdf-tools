from docx import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table as DocxTable
from docx.text.paragraph import Paragraph as DocxParagraph

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib import colors
from PIL import Image as PILImage
from io import BytesIO
import os

def get_alignment(alignment):
    return {
        0: TA_LEFT,
        1: TA_CENTER,
        2: TA_RIGHT,
        3: TA_JUSTIFY
    }.get(alignment, TA_LEFT)

def docx_to_pdf_better(docx_path, output_path):
    doc = Document(docx_path)
    styles = getSampleStyleSheet()
    
    styles.add(ParagraphStyle(name='JustifyCustom', alignment=TA_JUSTIFY, fontSize=11, leading=15))
    styles.add(ParagraphStyle(name='MyHeading1', fontSize=16, leading=18, spaceAfter=12, spaceBefore=12, alignment=TA_LEFT, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='MyHeading2', fontSize=14, leading=16, spaceAfter=10, spaceBefore=10, alignment=TA_LEFT, textColor=colors.darkblue))

    story = []

    for element in doc.element.body:
        if isinstance(element, CT_P):
            p = DocxParagraph(element, doc)
            text = ''
            for run in p.runs:
                run_text = run.text.replace('\n', '<br/>')
                if run.bold:
                    run_text = f"<b>{run_text}</b>"
                if run.italic:
                    run_text = f"<i>{run_text}</i>"
                if run.underline:
                    run_text = f"<u>{run_text}</u>"
                text += run_text
            
            style = styles['JustifyCustom']
            if p.style.name.startswith("Heading 1"):
                style = styles['MyHeading1']
            elif p.style.name.startswith("Heading 2"):
                style = styles['MyHeading2']
            else:
                # Adjust font size and alignment based on Word styles
                font_size = p.style.font.size.pt if p.style.font.size else 11
                style = ParagraphStyle(
                    name=f"Para-{p.alignment}",
                    parent=styles['JustifyCustom'],
                    alignment=get_alignment(p.alignment),
                    fontSize=font_size
                )

            if text.strip():
                story.append(Paragraph(text, style))
                story.append(Spacer(1, 0.2 * inch))

        elif isinstance(element, CT_Tbl):
            tbl = DocxTable(element, doc)
            data = []
            for row in tbl.rows:
                row_data = []
                for cell in row.cells:
                    cell_text = '<br/>'.join(p.text for p in cell.paragraphs)
                    row_data.append(Paragraph(cell_text, styles['JustifyCustom']))
                data.append(row_data)
            t = Table(data, hAlign='LEFT')
            t.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 10),
            ]))
            story.append(t)
            story.append(Spacer(1, 0.2 * inch))

    # Handle images with proper scaling
    for rel in doc.part._rels:
        rel = doc.part._rels[rel]
        if "image" in rel.target_ref:
            img_data = rel.target_part.blob
            img_io = BytesIO(img_data)
            img = PILImage.open(img_io)
            max_width = 5 * inch
            ratio = min(max_width / img.width, 1)  # Scale down if necessary
            img_width = img.width * ratio
            img_height = img.height * ratio
            story.append(Image(img_io, width=img_width, height=img_height))
            story.append(Spacer(1, 0.2 * inch))

    pdf = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=72, bottomMargin=72)
    pdf.build(story)