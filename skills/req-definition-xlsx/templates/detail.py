"""Sheet 3: 세부요구사항 생성 — 14컬럼, 자동 행 높이"""
from .common import *

COLUMNS = [
    ("A", "번호", 5),
    ("B", "요구사항 분류", 12),
    ("C", "요구사항 ID", 11),
    ("D", "요구사항명", 16),
    ("E", "정의", 18),
    ("F", "세부 내용", 75),
    ("G", "출처", 10),
    ("H", "기술현상", 8),
    ("I", "인터뷰", 8),
    ("J", "설계 및 개발", 10),
    ("K", "비고", 12),
    ("L", "요구부서", 12),
    ("M", "수용\n여부", 6),
    ("N", "사유(수용불가/부분\n수용 시)", 20),
]

def create_detail_sheet(wb, requirements, source_label="제안요청서"):
    """세부요구사항 시트 생성."""
    ws = wb.create_sheet("세부요구사항")

    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = 'landscape'
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = 0.3
    ws.page_margins.right = 0.3
    ws.page_margins.top = 0.4
    ws.page_margins.bottom = 0.4

    for letter, _, width in COLUMNS:
        ws.column_dimensions[letter].width = width

    # 헤더
    ws.row_dimensions[1].height = 36
    for i, (_, name, _) in enumerate(COLUMNS, 1):
        c = ws.cell(row=1, column=i, value=name)
        c.font = FONT_HEADER
        c.fill = FILL_ACCENT
        c.alignment = ALIGN_CENTER
        c.border = BORDER_HEADER

    ws.freeze_panes = "A2"

    # 데이터 행
    for idx, req in enumerate(requirements):
        row = idx + 2
        no = idx + 1
        is_even = (no % 2 == 0)
        fill = FILL_LIGHT if is_even else FILL_WHITE

        detail_text = req.get('detail', '')
        ws.row_dimensions[row].height = row_height_for_text(detail_text)

        row_data = [
            (no, FONT_NO, ALIGN_CENTER),
            (req.get('category', ''), FONT_DATA, ALIGN_LEFT_CENTER),
            (req.get('id', ''), FONT_DATA, ALIGN_CENTER),
            (req.get('name', ''), FONT_DATA, ALIGN_LEFT_CENTER),
            (req.get('definition', ''), FONT_DATA_WRAP, ALIGN_LEFT_TOP),
            (detail_text, FONT_DATA_WRAP, ALIGN_LEFT_TOP),
            (source_label, FONT_DATA, ALIGN_CENTER),
            (None, FONT_DATA, ALIGN_CENTER),
            (None, FONT_DATA, ALIGN_CENTER),
            (None, FONT_DATA, ALIGN_CENTER),
            (None, FONT_DATA, ALIGN_CENTER),
            (None, FONT_DATA, ALIGN_CENTER),
            (None, FONT_DATA, ALIGN_CENTER),
            (None, FONT_DATA, ALIGN_LEFT_CENTER),
        ]

        for col_idx, (val, font, align) in enumerate(row_data, 1):
            c = ws.cell(row=row, column=col_idx, value=val)
            c.font = font
            c.alignment = align
            c.border = BORDER_THIN
            c.fill = fill

    total = len(requirements)
    ws.print_area = f'A1:N{total + 1}'
    return ws
