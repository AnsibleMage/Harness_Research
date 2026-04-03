"""Sheet 2: 개정이력 생성 — 19행 데이터 + 주석"""
from .common import *

def create_revision_sheet(wb, meta):
    """개정이력 시트 생성."""
    ws = wb.create_sheet("개정이력")

    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.orientation = 'landscape'
    ws.print_options.horizontalCentered = True
    ws.page_margins.left = 0.5
    ws.page_margins.right = 0.5
    ws.page_margins.top = 0.6
    ws.page_margins.bottom = 0.5

    widths = {'A': 5.5, 'B': 10, 'C': 14, 'D': 14, 'E': 36, 'F': 12, 'G': 12}
    for col, w in widths.items():
        ws.column_dimensions[col].width = w

    # 제목
    ws.row_dimensions[1].height = 42
    ws.merge_cells('A1:G1')
    c = ws.cell(row=1, column=1, value="개 정 이 력")
    c.font = FONT_SHEET_TITLE
    c.alignment = ALIGN_CENTER

    # 헤더
    ws.row_dimensions[2].height = 30
    headers = ["No", "버전", "변경일", "변경 사유", "변경 내용", "작성자", "승인자"]
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=2, column=i, value=h)
        c.font = FONT_HEADER_10
        c.fill = FILL_ACCENT
        c.alignment = ALIGN_CENTER
        c.border = BORDER_HEADER

    # 데이터 행 (No 1~19)
    version = meta.get('version', '1.0')
    if '.' in version:
        parts = version.split('.')
        version_short = f"{parts[0]}.{parts[1]}"
    else:
        version_short = version

    created = meta.get('created', '')
    created_dot = created.replace('-', '.') + '.' if created else ''
    author = meta.get('author', '')

    for row_idx in range(3, 22):
        no = row_idx - 2
        ws.row_dimensions[row_idx].height = 22
        is_even = (no % 2 == 0)
        fill = FILL_LIGHT if is_even else FILL_WHITE

        for col in range(1, 8):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = BORDER_THIN
            cell.fill = fill
            cell.font = FONT_DATA
            cell.alignment = ALIGN_CENTER

            if col == 1:
                cell.value = no
                cell.font = FONT_NO

        if row_idx == 3:
            ws.cell(row=3, column=2, value=version_short)
            ws.cell(row=3, column=3, value=created_dot)
            ws.cell(row=3, column=4, value="신규")
            ws.cell(row=3, column=5, value="최초 작성")
            ws.cell(row=3, column=5).alignment = ALIGN_LEFT_CENTER
            ws.cell(row=3, column=6, value=author)

    # 주석
    notes = [
        "1) 버전: 초안은 0.1으로 표시 하고, 검토 된 이후 승인을 득한 이후에는 1.0부터 시작하여 정수 단위로 변경 관리 함.",
        "   변경 발생 시, 소수점 아래 번호로 관리하고, 목차 내용이 바뀔 정도의 큰 변경이 발생하면 상위 정수를 변경 함.",
        "   (예, V1.2 : 2번 수정됨, 목차 내용이 변경되면 V2.0 이 됨)",
        "2) 변경 사유 : 변경 내용이 이전 문서에 대해 신규/추가/수정/삭제/검토/승인 인지 선택 기입",
        "3) 변경 내용 : 변경 내용을 자세히 기록(변경된 위치, 즉 페이지 번호와 변경 내용을 기술한다.)",
    ]
    for i, note in enumerate(notes):
        row = 22 + i
        ws.row_dimensions[row].height = 16
        ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=7)
        c = ws.cell(row=row, column=1, value=note)
        c.font = FONT_NOTE
        c.alignment = Alignment(horizontal='left', vertical='center')

    ws.print_area = 'A1:G26'
    return ws
