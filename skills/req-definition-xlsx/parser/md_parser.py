"""마크다운 요구사항 정의서 파서 — frontmatter + 요구사항 추출"""
import re

def parse_frontmatter(lines):
    """YAML frontmatter를 딕셔너리로 파싱."""
    meta = {}
    in_fm = False
    for line in lines:
        stripped = line.strip()
        if stripped == '---':
            if in_fm:
                break
            in_fm = True
            continue
        if in_fm and ':' in stripped:
            key, _, val = stripped.partition(':')
            val = val.strip().strip('"').strip("'")
            meta[key.strip()] = val
    return meta

def parse_requirements(lines):
    """요구사항 정의서에서 분류 + 개별 요구사항을 추출."""
    requirements = []
    current_category = ""
    current_req = None

    category_pattern = re.compile(r'^### 4\.\d+\s+(.+?)(?:\s*\(.*\))?\s*$')
    req_pattern = re.compile(r'^#### ([A-Z]+-\d+)\s+(.+)$')
    id_pattern = re.compile(r'\*\*요구사항 ID\*\*\s*\|\s*(.+?)\s*\|?$')
    name_pattern = re.compile(r'\*\*요구사항명\*\*\s*\|\s*(.+?)\s*\|?$')
    def_pattern = re.compile(r'^\*\*정의\*\*:\s*(.+)$')

    state = "IDLE"

    for line in lines:
        stripped = line.rstrip()

        cat_match = category_pattern.match(stripped)
        if cat_match:
            raw = cat_match.group(1).strip()
            for suffix in ['요구사항', '요구 사항']:
                if raw.endswith(suffix):
                    raw = raw[:-len(suffix)].strip()
                    break
            current_category = raw
            continue

        req_match = req_pattern.match(stripped)
        if req_match:
            if current_req and current_req.get('id'):
                current_req['detail'] = '\n'.join(current_req.get('_detail_lines', []))
                del current_req['_detail_lines']
                requirements.append(current_req)
            current_req = {
                'id': req_match.group(1),
                'name': req_match.group(2).strip(),
                'category': current_category,
                'definition': '',
                '_detail_lines': [],
            }
            state = "IDLE"
            continue

        if current_req:
            def_match = def_pattern.match(stripped)
            if def_match:
                current_req['definition'] = def_match.group(1).strip()
                continue

            if stripped.startswith('**세부 내용**'):
                state = "DETAIL"
                continue
            if stripped.startswith('**산출물**') or stripped.startswith('**변경 내역**'):
                state = "IDLE"
                continue

            if state == "DETAIL" and stripped:
                current_req['_detail_lines'].append(convert_bullet(stripped))

    if current_req and current_req.get('id'):
        current_req['detail'] = '\n'.join(current_req.get('_detail_lines', []))
        if '_detail_lines' in current_req:
            del current_req['_detail_lines']
        requirements.append(current_req)

    return requirements

def convert_bullet(line):
    """마크다운 불릿을 엑셀 셀 텍스트로 변환."""
    stripped = line.lstrip()
    indent = len(line) - len(stripped)

    if stripped.startswith('- '):
        content = stripped[2:]
        if indent == 0:
            return f"* {content}"
        elif indent <= 2:
            return f"  - {content}"
        else:
            return f"{'  ' * (indent // 2)}· {content}"
    return line

def parse_md_file(filepath):
    """md 파일을 읽어 frontmatter + requirements 반환."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    frontmatter = parse_frontmatter(lines)
    requirements = parse_requirements(lines)

    return {
        'frontmatter': frontmatter,
        'requirements': requirements,
        'total_count': len(requirements),
    }
