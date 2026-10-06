import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Nirmala', r'C:\Windows\Fonts\Nirmala.ttf'))
pdfmetrics.registerFont(TTFont('NirmalaB', r'C:\Windows\Fonts\NirmalaB.ttf'))

PAGE_W, PAGE_H = landscape(A4)

title_style = ParagraphStyle(
    'DocTitle',
    fontName='NirmalaB',
    fontSize=18,
    leading=22,
    alignment=1, # Center
    textColor=colors.HexColor('#0f172a')
)

subtitle_style = ParagraphStyle(
    'DocSubtitle',
    fontName='Nirmala',
    fontSize=10,
    leading=14,
    alignment=1,
    textColor=colors.HexColor('#475569')
)

lesson_head_style = ParagraphStyle(
    'LessonHead',
    fontName='NirmalaB',
    fontSize=13,
    leading=17,
    textColor=colors.HexColor('#1e3a8a'),
    spaceAfter=6
)

swara_cell_style = ParagraphStyle(
    'SwaraCell',
    fontName='NirmalaB',
    fontSize=13,
    leading=16,
    alignment=1,
    textColor=colors.HexColor('#b45309')
)

west_cell_style = ParagraphStyle(
    'WestCell',
    fontName='NirmalaB',
    fontSize=11,
    leading=14,
    alignment=1,
    textColor=colors.HexColor('#0284c7')
)

tala_head_style = ParagraphStyle(
    'TalaHead',
    fontName='NirmalaB',
    fontSize=9,
    leading=12,
    alignment=1,
    textColor=colors.HexColor('#64748b')
)

def make_adi_table(lines_data):
    # lines_data is a list of tuples: (swara_row_list_of_8, west_row_list_of_8)
    # 8 beats + 2 dividers (after beat 4, after beat 6) => 10 cols or 8 cols with border styles
    # We will use 8 columns with cell borders marking the Tala partitions (1-4 laghu, 5-6 dhrutam, 7-8 dhrutam)
    header_row = [
        Paragraph("1 (தட்டு)", tala_head_style),
        Paragraph("2 (சுண்டு)", tala_head_style),
        Paragraph("3 (மோதிர)", tala_head_style),
        Paragraph("4 (நடு)", tala_head_style),
        Paragraph("5 (தட்டு)", tala_head_style),
        Paragraph("6 (வீச்சு)", tala_head_style),
        Paragraph("7 (தட்டு)", tala_head_style),
        Paragraph("8 (வீச்சு)", tala_head_style),
    ]
    
    table_data = [header_row]
    for swaras, west_notes in lines_data:
        s_row = [Paragraph(s, swara_cell_style) for s in swaras]
        w_row = [Paragraph(w, west_cell_style) for w in west_notes]
        table_data.append(s_row)
        table_data.append(w_row)
    
    col_w = (PAGE_W - 68) / 8 # ~96 pt per beat
    t = Table(table_data, colWidths=[col_w]*8)
    
    t_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        # Tala division thick lines:
        ('RIGHTPADDING', (3, 0), (3, -1), 8),
        ('LINEAFTER', (3, 0), (3, -1), 2.0, colors.HexColor('#b45309')), # End of Laghu
        ('LINEAFTER', (5, 0), (5, -1), 2.0, colors.HexColor('#b45309')), # End of 1st Dhrutam
        ('LINEAFTER', (7, 0), (7, -1), 2.5, colors.HexColor('#b45309')), # End of Avartanam
    ]
    
    # Shade Western notes rows lightly
    for r in range(2, len(table_data), 2):
        t_style.append(('BACKGROUND', (0, r), (-1, r), colors.HexColor('#f8fafc')))
        t_style.append(('BOTTOMPADDING', (0, r), (-1, r), 7))
        t_style.append(('TOPPADDING', (0, r-1), (-1, r-1), 7))
    
    t.setStyle(TableStyle(t_style))
    return t

# ==============================================================================
# 1. Jantai Varisai (1 to 10)
# ==============================================================================
def build_jantai_pdf():
    pdf_path = "PDF/Janta_1_to_10_Swaram_Western_Below_gana_amitha_pothini.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(A4),
        leftMargin=34, rightMargin=34,
        topMargin=28, bottomMargin=28
    )
    story = []
    
    header_block = [
        Paragraph("ஜண்டை வரிசைகள் — 1 to 10 | Jantai Varisai — Swaram + Western Notes", title_style),
        Spacer(1, 4),
        Paragraph("கானாம்ருத போதினி • Gana Amrutha Bodhini • ராகம்: மாயாமாளவகௌளை • தாளம்: ஆதி தாளம் • Sa = C4 (1-ம் கட்டை)", subtitle_style),
        Spacer(1, 14)
    ]
    
    jantai_lessons = [
        # (title, [ (swara_8, west_8), ... ])
        (
            "1. ஜண்டை வரிசை (Jantai Varisai 1) — இரட்டை சுவர அடிப்படை (Twin Notes)",
            [
                (["ச  ச", "ரி  ரி", "க  க", "ம  ம", "ப  ப", "த  த", "நி  நி", "ஸ்  ஸ்"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4", "C5 C5"]),
                (["ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப", "ம  ம", "க  க", "ரி  ரி", "ச  ச"],
                 ["C5 C5", "B4 B4", "G#4 G#4", "G4 G4", "F4 F4", "E4 E4", "C#4 C#4", "C4 C4"])
            ]
        ),
        (
            "2. ஜண்டை வரிசை (Jantai Varisai 2) — சுவர தழுவல் (Twin Note Flow)",
            [
                (["ச  ச", "ரி  ரி", "க  க", "ம  ம", "ரி  ரி", "க  க", "ம  ம", "ப  ப"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "F4 F4", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4"]),
                (["க  க", "ம  ம", "ப  ப", "த  த", "ம  ம", "ப  ப", "த  த", "நி  நி"],
                 ["E4 E4", "F4 F4", "G4 G4", "G#4 G#4", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4"]),
                (["ப  ப", "த  த", "நி  நி", "ஸ்  ஸ்", "ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப"],
                 ["G4 G4", "G#4 G#4", "B4 B4", "C5 C5", "C5 C5", "B4 B4", "G#4 G#4", "G4 G4"]),
                (["நி  நி", "த  த", "ப  ப", "ம  ம", "த  த", "ப  ப", "ம  ம", "க  க"],
                 ["B4 B4", "G#4 G#4", "G4 G4", "F4 F4", "G#4 G#4", "G4 G4", "F4 F4", "E4 E4"]),
                (["ப  ப", "ம  ம", "க  க", "ரி  ரி", "ம  ம", "க  க", "ரி  ரி", "ச  ச"],
                 ["G4 G4", "F4 F4", "E4 E4", "C#4 C#4", "F4 F4", "E4 E4", "C#4 C#4", "C4 C4"])
            ]
        ),
        (
            "3. ஜண்டை வரிசை (Jantai Varisai 3) — மூன்று சுவர ஜண்டை (Triple Jantai)",
            [
                (["ச  ச", "ரி  -", "ச  ச", "ரி  -", "ச  ச", "ரி  ரி", "க  க", "ம  ம"],
                 ["C4 C4", "C#4 -", "C4 C4", "C#4 -", "C4 C4", "C#4 C#4", "E4 E4", "F4 F4"]),
                (["ரி  ரி", "க  -", "ரி  ரி", "க  -", "ரி  ரி", "க  க", "ம  ம", "ப  ப"],
                 ["C#4 C#4", "E4 -", "C#4 C#4", "E4 -", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4"]),
                (["க  க", "ம  -", "க  க", "ம  -", "க  க", "ம  ம", "ப  ப", "த  த"],
                 ["E4 E4", "F4 -", "E4 E4", "F4 -", "E4 E4", "F4 F4", "G4 G4", "G#4 G#4"]),
                (["ம  ம", "ப  -", "ம  ம", "ப  -", "ம  ம", "ப  ப", "த  த", "நி  நி"],
                 ["F4 F4", "G4 -", "F4 F4", "G4 -", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4"]),
                (["ப  ப", "த  -", "ப  ப", "த  -", "ப  ப", "த  த", "நி  நி", "ஸ்  ஸ்"],
                 ["G4 G4", "G#4 -", "G4 G4", "G#4 -", "G4 G4", "G#4 G#4", "B4 B4", "C5 C5"]),
                (["ஸ்  ஸ்", "நி  -", "ஸ்  ஸ்", "நி  -", "ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப"],
                 ["C5 C5", "B4 -", "C5 C5", "B4 -", "C5 C5", "B4 B4", "G#4 G#4", "G4 G4"]),
                (["நி  நி", "த  -", "நி  நி", "த  -", "நி  நி", "த  த", "ப  ப", "ம  ம"],
                 ["B4 B4", "G#4 -", "B4 B4", "G#4 -", "B4 B4", "G#4 G#4", "G4 G4", "F4 F4"]),
                (["த  த", "ப  -", "த  த", "ப  -", "த  த", "ப  ப", "ம  ம", "க  க"],
                 ["G#4 G#4", "G4 -", "G#4 G#4", "G4 -", "G#4 G#4", "G4 G4", "F4 F4", "E4 E4"]),
                (["ப  ப", "ம  -", "ப  ப", "ம  -", "ப  ப", "ம  ம", "க  க", "ரி  ரி"],
                 ["G4 G4", "F4 -", "G4 G4", "F4 -", "G4 G4", "F4 F4", "E4 E4", "C#4 C#4"]),
                (["ம  ம", "க  -", "ம  ம", "க  -", "ம  ம", "க  க", "ரி  ரி", "ச  ச"],
                 ["F4 F4", "E4 -", "F4 F4", "E4 -", "F4 F4", "E4 E4", "C#4 C#4", "C4 C4"])
            ]
        ),
        (
            "4. ஜண்டை வரிசை (Jantai Varisai 4) — சுவர தாவல் ஜண்டை (Sphuritha Jantai)",
            [
                (["ச  ச", "ரி  ரி", "க  க", "ரி  ரி", "ச  ச", "ரி  ரி", "க  க", "ம  ம"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "C#4 C#4", "C4 C4", "C#4 C#4", "E4 E4", "F4 F4"]),
                (["ரி  ரி", "க  க", "ம  ம", "க  க", "ரி  ரி", "க  க", "ம  ம", "ப  ப"],
                 ["C#4 C#4", "E4 E4", "F4 F4", "E4 E4", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4"]),
                (["க  க", "ம  ம", "ப  ப", "ம  ம", "க  க", "ம  ம", "ப  ப", "த  த"],
                 ["E4 E4", "F4 F4", "G4 G4", "F4 F4", "E4 E4", "F4 F4", "G4 G4", "G#4 G#4"]),
                (["ம  ம", "ப  ப", "த  த", "ப  ப", "ம  ம", "ப  ப", "த  த", "நி  நி"],
                 ["F4 F4", "G4 G4", "G#4 G#4", "G4 G4", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4"]),
                (["ப  ப", "த  த", "நி  நி", "த  த", "ப  ப", "த  த", "நி  நி", "ஸ்  ஸ்"],
                 ["G4 G4", "G#4 G#4", "B4 B4", "G#4 G#4", "G4 G4", "G#4 G#4", "B4 B4", "C5 C5"]),
                (["ஸ்  ஸ்", "நி  நி", "த  த", "நி  நி", "ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப"],
                 ["C5 C5", "B4 B4", "G#4 G#4", "B4 B4", "C5 C5", "B4 B4", "G#4 G#4", "G4 G4"]),
                (["நி  நி", "த  த", "ப  ப", "த  த", "நி  நி", "த  த", "ப  ப", "ம  ம"],
                 ["B4 B4", "G#4 G#4", "G4 G4", "G#4 G#4", "B4 B4", "G#4 G#4", "G4 G4", "F4 F4"]),
                (["த  த", "ப  ப", "ம  ம", "ப  ப", "த  த", "ப  ப", "ம  ம", "க  க"],
                 ["G#4 G#4", "G4 G4", "F4 F4", "G4 G4", "G#4 G#4", "G4 G4", "F4 F4", "E4 E4"]),
                (["ப  ப", "ம  ம", "க  க", "ம  ம", "ப  ப", "ம  ம", "க  க", "ரி  ரி"],
                 ["G4 G4", "F4 F4", "E4 E4", "F4 F4", "G4 G4", "F4 F4", "E4 E4", "C#4 C#4"]),
                (["ம  ம", "க  க", "ரி  ரி", "க  க", "ம  ம", "க  க", "ரி  ரி", "ச  ச"],
                 ["F4 F4", "E4 E4", "C#4 C#4", "E4 E4", "F4 F4", "E4 E4", "C#4 C#4", "C4 C4"])
            ]
        ),
        (
            "5. ஜண்டை வரிசை (Jantai Varisai 5) — கார்வை ஜண்டை (Karvai Jantai)",
            [
                (["ச  ச", "ரி  ரி", "க  க", "ம  -", "ச  ச", "ரி  ரி", "க  க", "ம  ம"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "F4 -", "C4 C4", "C#4 C#4", "E4 E4", "F4 F4"]),
                (["ரி  ரி", "க  க", "ம  ம", "ப  -", "ரி  ரி", "க  க", "ம  ம", "ப  ப"],
                 ["C#4 C#4", "E4 E4", "F4 F4", "G4 -", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4"]),
                (["க  க", "ம  ம", "ப  ப", "த  -", "க  க", "ம  ம", "ப  ப", "த  த"],
                 ["E4 E4", "F4 F4", "G4 G4", "G#4 -", "E4 E4", "F4 F4", "G4 G4", "G#4 G#4"]),
                (["ம  ம", "ப  ப", "த  த", "நி  -", "ம  ம", "ப  ப", "த  த", "நி  நி"],
                 ["F4 F4", "G4 G4", "G#4 G#4", "B4 -", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4"]),
                (["ப  ப", "த  த", "நி  நி", "ஸ்  -", "ப  ப", "த  த", "நி  நி", "ஸ்  ஸ்"],
                 ["G4 G4", "G#4 G#4", "B4 B4", "C5 -", "G4 G4", "G#4 G#4", "B4 B4", "C5 C5"]),
                (["ஸ்  ஸ்", "நி  நி", "த  த", "ப  -", "ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப"],
                 ["C5 C5", "B4 B4", "G#4 G#4", "G4 -", "C5 C5", "B4 B4", "G#4 G#4", "G4 G4"]),
                (["நி  நி", "த  த", "ப  ப", "ம  -", "நி  நி", "த  த", "ப  ப", "ம  ம"],
                 ["B4 B4", "G#4 G#4", "G4 G4", "F4 -", "B4 B4", "G#4 G#4", "G4 G4", "F4 F4"]),
                (["த  த", "ப  ப", "ம  ம", "க  -", "த  த", "ப  ப", "ம  ம", "க  க"],
                 ["G#4 G#4", "G4 G4", "F4 F4", "E4 -", "G#4 G#4", "G4 G4", "F4 F4", "E4 E4"]),
                (["ப  ப", "ம  ம", "க  க", "ரி  -", "ப  ப", "ம  ம", "க  க", "ரி  ரி"],
                 ["G4 G4", "F4 F4", "E4 E4", "C#4 -", "G4 G4", "F4 F4", "E4 E4", "C#4 C#4"]),
                (["ம  ம", "க  க", "ரி  ரி", "ச  -", "ம  ம", "க  க", "ரி  ரி", "ச  ச"],
                 ["F4 F4", "E4 E4", "C#4 C#4", "C4 -", "F4 F4", "E4 E4", "C#4 C#4", "C4 C4"])
            ]
        ),
        (
            "6. ஜண்டை வரிசை (Jantai Varisai 6) — சமச்சீர் ஜண்டை (Symmetrical Jantai)",
            [
                (["ச  ச", "ரி  ரி", "க  க", "ம  ம", "ப  ப", "ம  ம", "க  க", "ரி  ரி"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4", "F4 F4", "E4 E4", "C#4 C#4"]),
                (["ச  ச", "ரி  ரி", "க  க", "ம  ம", "ப  ப", "த  த", "நி  நி", "ஸ்  ஸ்"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4", "C5 C5"]),
                (["ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப", "ம  ம", "ப  ப", "த  த", "நி  நி"],
                 ["C5 C5", "B4 B4", "G#4 G#4", "G4 G4", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4"]),
                (["ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப", "ம  ம", "க  க", "ரி  ரி", "ச  ச"],
                 ["C5 C5", "B4 B4", "G#4 G#4", "G4 G4", "F4 F4", "E4 E4", "C#4 C#4", "C4 C4"])
            ]
        ),
        (
            "7. ஜண்டை வரிசை (Jantai Varisai 7) — தாண்டுதல் ஜண்டை (Leaping Jantai)",
            [
                (["ச  ச", "க  க", "ரி  ரி", "ம  ம", "க  க", "ப  ப", "ம  ம", "த  த"],
                 ["C4 C4", "E4 E4", "C#4 C#4", "F4 F4", "E4 E4", "G4 G4", "F4 F4", "G#4 G#4"]),
                (["ப  ப", "நி  நி", "த  த", "ஸ்  ஸ்", "ஸ்  ஸ்", "த  த", "நி  நி", "ப  ப"],
                 ["G4 G4", "B4 B4", "G#4 G#4", "C5 C5", "C5 C5", "G#4 G#4", "B4 B4", "G4 G4"]),
                (["த  த", "ம  ம", "ப  ப", "க  க", "ம  ம", "ரி  ரி", "க  க", "ச  ச"],
                 ["G#4 G#4", "F4 F4", "G4 G4", "E4 E4", "F4 F4", "C#4 C#4", "E4 E4", "C4 C4"])
            ]
        ),
        (
            "8. ஜண்டை வரிசை (Jantai Varisai 8) — சுழற்சி ஜண்டை (Loop Jantai)",
            [
                (["ச  ச", "ரி  ரி", "க  க", "ச  ச", "ரி  ரி", "க  க", "ம  ம", "ப  ப"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "C4 C4", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4"]),
                (["க  க", "ம  ம", "ப  ப", "க  க", "ம  ம", "ப  ப", "த  த", "நி  நி"],
                 ["E4 E4", "F4 F4", "G4 G4", "E4 E4", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4"]),
                (["ப  ப", "த  த", "நி  நி", "ஸ்  ஸ்", "ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப"],
                 ["G4 G4", "G#4 G#4", "B4 B4", "C5 C5", "C5 C5", "B4 B4", "G#4 G#4", "G4 G4"]),
                (["நி  நி", "த  த", "ப  ப", "நி  நி", "த  த", "ப  ப", "ம  ம", "க  க"],
                 ["B4 B4", "G#4 G#4", "G4 G4", "B4 B4", "G#4 G#4", "G4 G4", "F4 F4", "E4 E4"]),
                (["த  த", "ப  ப", "ம  ம", "க  க", "ரி  ரி", "ச  ச", "ரி  ரி", "ச  ச"],
                 ["G#4 G#4", "G4 G4", "F4 F4", "E4 E4", "C#4 C#4", "C4 C4", "C#4 C#4", "C4 C4"])
            ]
        ),
        (
            "9. ஜண்டை வரிசை (Jantai Varisai 9) — இரட்டை நீட்சி ஜண்டை (Extended Jantai)",
            [
                (["ச  ச", "ரி  ரி", "க  க", "ம  ம", "ப  ப", "த  த", "ப  ப", "ம  ம"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4", "G#4 G#4", "G4 G4", "F4 F4"]),
                (["க  க", "ம  ம", "ப  ப", "த  த", "நி  நி", "ஸ்  ஸ்", "நி  நி", "த  த"],
                 ["E4 E4", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4", "C5 C5", "B4 B4", "G#4 G#4"]),
                (["ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப", "ம  ம", "க  க", "ம  ம", "ப  ப"],
                 ["C5 C5", "B4 B4", "G#4 G#4", "G4 G4", "F4 F4", "E4 E4", "F4 F4", "G4 G4"]),
                (["த  த", "ப  ப", "ம  ம", "க  க", "ரி  ரி", "ச  ச", "ரி  ரி", "ச  ச"],
                 ["G#4 G#4", "G4 G4", "F4 F4", "E4 E4", "C#4 C#4", "C4 C4", "C#4 C#4", "C4 C4"])
            ]
        ),
        (
            "10. ஜண்டை வரிசை (Jantai Varisai 10) — முத்தாய்ப்பு ஜண்டை (Grand Finale Jantai)",
            [
                (["ச  ச", "ரி  ரி", "க  க", "ம  ம", "ப  ப", "த  த", "நி  நி", "ஸ்  ஸ்"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "F4 F4", "G4 G4", "G#4 G#4", "B4 B4", "C5 C5"]),
                (["ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப", "ம  ம", "க  க", "ரி  ரி", "ச  ச"],
                 ["C5 C5", "B4 B4", "G#4 G#4", "G4 G4", "F4 F4", "E4 E4", "C#4 C#4", "C4 C4"]),
                (["ச  ச", "ரி  ரி", "க  க", "ம  ம", "ப  -", "த  -", "நி  -", "ஸ்  -"],
                 ["C4 C4", "C#4 C#4", "E4 E4", "F4 F4", "G4 -", "G#4 -", "B4 -", "C5 -"]),
                (["ஸ்  ஸ்", "நி  நி", "த  த", "ப  ப", "ம  -", "க  -", "ரி  -", "ச  -"],
                 ["C5 C5", "B4 B4", "G#4 G#4", "G4 G4", "F4 -", "E4 -", "C#4 -", "C4 -"])
            ]
        )
    ]
    
    # 2 lessons per page
    for idx, (title, lines) in enumerate(jantai_lessons):
        if idx % 2 == 0:
            if idx > 0:
                story.append(PageBreak())
            story.extend(header_block)
        else:
            story.append(Spacer(1, 14))
        
        story.append(Paragraph(title, lesson_head_style))
        story.append(make_adi_table(lines))
    
    doc.build(story)
    print(f"Generated {pdf_path}")

# ==============================================================================
# 2. Dhatu Varisai (1 to 4)
# ==============================================================================
def build_dhatu_pdf():
    pdf_path = "PDF/Dhatu_1_to_4_Swaram_Western_Below_gana_amitha_pothini.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(A4),
        leftMargin=34, rightMargin=34,
        topMargin=28, bottomMargin=28
    )
    story = []
    
    header_block = [
        Paragraph("தாட்டு வரிசைகள் — 1 to 4 | Dhatu Varisai — Swaram + Western Notes", title_style),
        Spacer(1, 4),
        Paragraph("கானாம்ருத போதினி • Gana Amrutha Bodhini • ராகம்: மாயாமாளவகௌளை • தாளம்: ஆதி தாளம் • Sa = C4 (1-ம் கட்டை)", subtitle_style),
        Spacer(1, 14)
    ]
    
    dhatu_lessons = [
        (
            "1. தாட்டு வரிசை (Dhatu Varisai 1) — குறுக்கு சுவர தாவல் (Single Step Zig-Zag)",
            [
                (["ச  க", "ரி  ம", "க  ப", "ம  த", "ப  நி", "த  ஸ்", "ஸ்  த", "நி  ப"],
                 ["C4 E4", "C#4 F4", "E4 G4", "F4 G#4", "G4 B4", "G#4 C5", "C5 G#4", "B4 G4"]),
                (["த  ம", "ப  க", "ம  ரி", "க  ச", "ச  ரி", "க  ம", "ப  த", "நி  ஸ்"],
                 ["G#4 F4", "G4 E4", "F4 C#4", "E4 C4", "C4 C#4", "E4 F4", "G4 G#4", "B4 C5"]),
                (["ஸ்  நி", "த  ப", "ம  க", "ரி  ச", "ஸ்  த", "நி  ப", "த  ம", "ப  க"],
                 ["C5 B4", "G#4 G4", "F4 E4", "C#4 C4", "C5 G#4", "B4 G4", "G#4 F4", "G4 E4"]),
                (["ம  ரி", "க  ச", "ச  ரி", "க  ம", "ப  ம", "க  ரி", "ச  -", "ச  -"],
                 ["F4 C#4", "E4 C4", "C4 C#4", "E4 F4", "G4 F4", "E4 C#4", "C4 -", "C4 -"])
            ]
        ),
        (
            "2. தாட்டு வரிசை (Dhatu Varisai 2) — இரட்டை தாவல் தாட்டு (Double Skip Leap)",
            [
                (["ச  ம", "க  ரி", "ச  ரி", "க  ம", "ரி  ப", "ம  க", "ரி  க", "ம  ப"],
                 ["C4 F4", "E4 C#4", "C4 C#4", "E4 F4", "C#4 G4", "F4 E4", "C#4 E4", "F4 G4"]),
                (["க  த", "ப  ம", "க  ம", "ப  த", "ம  நி", "த  ப", "ம  ப", "த  நி"],
                 ["E4 G#4", "G4 F4", "E4 F4", "G4 G#4", "F4 B4", "G#4 G4", "F4 G4", "G#4 B4"]),
                (["ப  ஸ்", "நி  த", "ப  த", "நி  ஸ்", "ஸ்  ப", "த  நி", "ஸ்  நி", "த  ப"],
                 ["G4 C5", "B4 G#4", "G4 G#4", "B4 C5", "C5 G4", "G#4 B4", "C5 B4", "G#4 G4"]),
                (["நி  ம", "ப  த", "நி  த", "ப  ம", "த  க", "ம  ப", "த  ப", "ம  க"],
                 ["B4 F4", "G4 G#4", "B4 G#4", "G4 F4", "G#4 E4", "F4 G4", "G#4 G4", "F4 E4"]),
                (["ப  ரி", "க  ம", "ப  ம", "க  ரி", "ம  ச", "ரி  க", "ம  க", "ரி  ச"],
                 ["G4 C#4", "E4 F4", "G4 F4", "E4 C#4", "F4 C4", "C#4 E4", "F4 E4", "C#4 C4"])
            ]
        ),
        (
            "3. தாட்டு வரிசை (Dhatu Varisai 3) — சுவர சுழல் தாட்டு (Looping Zig-Zag)",
            [
                (["ச  க", "ரி  ச", "ரி  ம", "க  ரி", "க  ப", "ம  க", "ம  த", "ப  ம"],
                 ["C4 E4", "C#4 C4", "C#4 F4", "E4 C#4", "E4 G4", "F4 E4", "F4 G#4", "G4 F4"]),
                (["ப  நி", "த  ப", "த  ஸ்", "நி  த", "ஸ்  த", "நி  ஸ்", "நி  ப", "த  நி"],
                 ["G4 B4", "G#4 G4", "G#4 C5", "B4 G#4", "C5 G#4", "B4 C5", "B4 G4", "G#4 B4"]),
                (["த  ம", "ப  த", "ப  க", "ம  ப", "ம  ரி", "க  ம", "க  ச", "ரி  ச"],
                 ["G#4 F4", "G4 G#4", "G4 E4", "F4 G4", "F4 C#4", "E4 F4", "E4 C4", "C#4 C4"])
            ]
        ),
        (
            "4. தாட்டு வரிசை (Dhatu Varisai 4) — ஜண்டை தாட்டு (Twin-Note Leaps)",
            [
                (["ச  ச", "க  க", "ரி  ரி", "ம  ம", "க  க", "ப  ப", "ம  ம", "த  த"],
                 ["C4 C4", "E4 E4", "C#4 C#4", "F4 F4", "E4 E4", "G4 G4", "F4 F4", "G#4 G#4"]),
                (["ப  ப", "நி  நி", "த  த", "ஸ்  ஸ்", "ஸ்  ஸ்", "த  த", "நி  நி", "ப  ப"],
                 ["G4 G4", "B4 B4", "G#4 G#4", "C5 C5", "C5 C5", "G#4 G#4", "B4 B4", "G4 G4"]),
                (["த  த", "ம  ம", "ப  ப", "க  க", "ம  ம", "ரி  ரி", "க  க", "ச  ச"],
                 ["G#4 G#4", "F4 F4", "G4 G4", "E4 E4", "F4 F4", "C#4 C#4", "E4 E4", "C4 C4"])
            ]
        )
    ]
    
    for idx, (title, lines) in enumerate(dhatu_lessons):
        if idx % 2 == 0:
            if idx > 0:
                story.append(PageBreak())
            story.extend(header_block)
        else:
            story.append(Spacer(1, 14))
        
        story.append(Paragraph(title, lesson_head_style))
        story.append(make_adi_table(lines))
    
    doc.build(story)
    print(f"Generated {pdf_path}")

# ==============================================================================
# 3. Saptha Tala Alankaram
# ==============================================================================
def build_alankaram_pdf():
    pdf_path = "PDF/Alankaram_Saptha_Tala_Swaram_Western_Below_gana_amitha_pothini.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=landscape(A4),
        leftMargin=34, rightMargin=34,
        topMargin=28, bottomMargin=28
    )
    story = []
    
    header_block = [
        Paragraph("சப்த தாள அலங்காரங்கள் | Saptha Tala Alankarams — Swaram + Western Notes", title_style),
        Spacer(1, 4),
        Paragraph("கானாம்ருத போதினி • Gana Amrutha Bodhini • ராகம்: மாயாமாளவகௌளை • Sa = C4 (1-ம் கட்டை)", subtitle_style),
        Spacer(1, 14)
    ]
    
    alankarams = [
        (
            "1. துருவ தாளம் (Dhruva Talam) — சதுஸ்ர ஜாதி (I4 + O + I4 + I4 = 14 அக்ஷரங்கள்)",
            [
                (["ச  ரி", "க  ம", "ப  த", "நி  ஸ்", "ரி  க", "ம  ப", "த  நி", "ஸ்  -"],
                 ["C4 C#4", "E4 F4", "G4 G#4", "B4 C5", "C#4 E4", "F4 G4", "G#4 B4", "C5 -"]),
                (["ஸ்  நி", "த  ப", "ம  க", "ரி  ச", "நி  த", "ப  ம", "க  ரி", "ச  -"],
                 ["C5 B4", "G#4 G4", "F4 E4", "C#4 C4", "B4 G#4", "G4 F4", "E4 C#4", "C4 -"])
            ]
        ),
        (
            "2. மட்ய தாளம் (Matya Talam) — சதுஸ்ர ஜாதி (I4 + O + I4 = 10 அக்ஷரங்கள்)",
            [
                (["ச  ரி", "க  ம", "ப  த", "ச  ரி", "க  ம", "ரி  க", "ம  ப", "த  நி"],
                 ["C4 C#4", "E4 F4", "G4 G#4", "C4 C#4", "E4 F4", "C#4 E4", "F4 G4", "G#4 B4"]),
                (["ஸ்  நி", "த  ப", "ம  க", "ஸ்  நி", "த  ப", "நி  த", "ப  ம", "க  ரி"],
                 ["C5 B4", "G#4 G4", "F4 E4", "C5 B4", "G#4 G4", "B4 G#4", "G4 F4", "E4 C#4"])
            ]
        ),
        (
            "3. ரூபக தாளம் (Roopaka Talam) — சதுஸ்ர ஜாதி (O + I4 = 6 அக்ஷரங்கள்)",
            [
                (["ச  ரி", "க  ம", "ப  த", "ரி  க", "ம  ப", "த  நி", "க  ம", "ப  த"],
                 ["C4 C#4", "E4 F4", "G4 G#4", "C#4 E4", "F4 G4", "G#4 B4", "E4 F4", "G4 G#4"]),
                (["ம  ப", "த  நி", "ஸ்  -", "ஸ்  நி", "த  ப", "ம  க", "நி  த", "ப  ம"],
                 ["F4 G4", "G#4 B4", "C5 -", "C5 B4", "G#4 G4", "F4 E4", "B4 G#4", "G4 F4"])
            ]
        ),
        (
            "4. ஜம்பை தாளம் (Jhampa Talam) — மிஸ்ர ஜாதி (I7 + U + O = 10 அக்ஷரங்கள்)",
            [
                (["ச  ரி", "க  ச", "ரி  க", "ம  ப", "த  நி", "ரி  க", "ம  ரி", "க  ம"],
                 ["C4 C#4", "E4 C4", "C#4 E4", "F4 G4", "G#4 B4", "C#4 E4", "F4 C#4", "E4 F4"]),
                (["ஸ்  நி", "த  ஸ்", "நி  த", "ப  ம", "க  ரி", "நி  த", "ப  நி", "த  ப"],
                 ["C5 B4", "G#4 C5", "B4 G#4", "G4 F4", "E4 C#4", "B4 G#4", "G4 B4", "G#4 G4"])
            ]
        ),
        (
            "5. த்ரிபுட தாளம் (Thriputa Talam) — திஸ்ர ஜாதி (I3 + O + O = 7 அக்ஷரங்கள்)",
            [
                (["ச  ரி", "க  ச", "ரி  க", "ம  -", "ரி  க", "ம  ரி", "க  ம", "ப  -"],
                 ["C4 C#4", "E4 C4", "C#4 E4", "F4 -", "C#4 E4", "F4 C#4", "E4 F4", "G4 -"]),
                (["ஸ்  நி", "த  ஸ்", "நி  த", "ப  -", "நி  த", "ப  நி", "த  ப", "ம  -"],
                 ["C5 B4", "G#4 C5", "B4 G#4", "G4 -", "B4 G#4", "G4 B4", "G#4 G4", "F4 -"])
            ]
        ),
        (
            "6. அட தாளம் (Ata Talam) — கண்ட ஜாதி (I5 + I5 + O + O = 14 அக்ஷரங்கள்)",
            [
                (["ச  ரி", "க  ம", "க  -", "ச  ரி", "க  ம", "ப  த", "நி  ஸ்", "ரி  க"],
                 ["C4 C#4", "E4 F4", "E4 -", "C4 C#4", "E4 F4", "G4 G#4", "B4 C5", "C#4 E4"]),
                (["ஸ்  நி", "த  ப", "த  -", "ஸ்  நி", "த  ப", "ம  க", "ரி  ச", "நி  த"],
                 ["C5 B4", "G#4 G4", "G#4 -", "C5 B4", "G#4 G4", "F4 E4", "C#4 C4", "B4 G#4"])
            ]
        ),
        (
            "7. ஏக தாளம் (Eka Talam) — சதுஸ்ர ஜாதி (I4 = 4 அக்ஷரங்கள்)",
            [
                (["ச  ரி", "க  ம", "ரி  க", "ம  ப", "க  ம", "ப  த", "ம  ப", "த  நி"],
                 ["C4 C#4", "E4 F4", "C#4 E4", "F4 G4", "E4 F4", "G4 G#4", "F4 G4", "G#4 B4"]),
                (["ப  த", "நி  ஸ்", "ஸ்  நி", "த  ப", "நி  த", "ப  ம", "த  ப", "ம  க"],
                 ["G4 G#4", "B4 C5", "C5 B4", "G#4 G4", "B4 G#4", "G4 F4", "G#4 G4", "F4 E4"])
            ]
        )
    ]
    
    for idx, (title, lines) in enumerate(alankarams):
        if idx % 2 == 0:
            if idx > 0:
                story.append(PageBreak())
            story.extend(header_block)
        else:
            story.append(Spacer(1, 14))
        
        story.append(Paragraph(title, lesson_head_style))
        story.append(make_adi_table(lines))
    
    doc.build(story)
    print(f"Generated {pdf_path}")

if __name__ == "__main__":
    build_jantai_pdf()
    build_dhatu_pdf()
    build_alankaram_pdf()
