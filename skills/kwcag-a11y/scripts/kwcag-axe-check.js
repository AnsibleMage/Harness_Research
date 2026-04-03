#!/usr/bin/env node
/**
 * KWCAG 2.2 axe-core 접근성 검사 스크립트 (Tier 2)
 *
 * axe-core와 jsdom을 사용하여 HTML 파일의 접근성을 자동 검사하고,
 * axe-core 위반 사항을 KWCAG 2.2 검사 항목 번호로 매핑합니다.
 *
 * Usage:
 *   node kwcag-axe-check.js <파일 또는 디렉토리> [--format json|md] [--severity critical|major|minor|all]
 */

'use strict';

// ---------------------------------------------------------------------------
// 의존성 검증 -- axe-core / jsdom 미설치 시 한국어 안내 후 종료
// ---------------------------------------------------------------------------
let axeSource;
let JSDOM;

try {
  JSDOM = require('jsdom').JSDOM;
} catch {
  console.error('[오류] jsdom 패키지가 설치되어 있지 않습니다.');
  console.error('  설치 방법: npm install jsdom');
  console.error('  또는 전역 설치: npm install -g jsdom');
  process.exit(1);
}

try {
  // axe-core 소스 코드를 문자열로 읽어서 jsdom에 주입하는 방식
  const axeCorePath = require.resolve('axe-core');
  axeSource = require('fs').readFileSync(axeCorePath, 'utf8');
} catch {
  console.error('[오류] axe-core 패키지가 설치되어 있지 않습니다.');
  console.error('  설치 방법: npm install axe-core');
  console.error('  또는 전역 설치: npm install -g axe-core');
  process.exit(1);
}

const fs = require('fs');
const path = require('path');

// ---------------------------------------------------------------------------
// axe-core 규칙 ID -> KWCAG 2.2 매핑 테이블
// ---------------------------------------------------------------------------
const AXE_TO_KWCAG = {
  'image-alt': { kwcag: '5.1.1', name: '적절한 대체 텍스트 제공', principle: '인식의 용이성', severity: 'critical', fix: '이미지에 적절한 alt 속성을 추가하세요.' },
  'area-alt': { kwcag: '5.1.1', name: '적절한 대체 텍스트 제공', principle: '인식의 용이성', severity: 'critical', fix: '이미지맵 <area>에 alt 속성을 추가하세요.' },
  'input-image-alt': { kwcag: '5.1.1', name: '적절한 대체 텍스트 제공', principle: '인식의 용이성', severity: 'critical', fix: '이미지 버튼에 alt 속성을 추가하세요.' },
  'role-img-alt': { kwcag: '5.1.1', name: '적절한 대체 텍스트 제공', principle: '인식의 용이성', severity: 'critical', fix: 'role="img" 요소에 aria-label을 추가하세요.' },
  'svg-img-alt': { kwcag: '5.1.1', name: '적절한 대체 텍스트 제공', principle: '인식의 용이성', severity: 'critical', fix: 'SVG에 <title> 또는 aria-label을 추가하세요.' },
  'object-alt': { kwcag: '5.1.1', name: '적절한 대체 텍스트 제공', principle: '인식의 용이성', severity: 'critical', fix: '<object>에 대체 텍스트를 제공하세요.' },
  'video-caption': { kwcag: '5.2.1', name: '자막 제공', principle: '인식의 용이성', severity: 'major', fix: '<video>에 <track kind="captions">을 추가하세요.' },
  'th-has-data-cells': { kwcag: '5.3.1', name: '표의 구성', principle: '인식의 용이성', severity: 'major', fix: '표 제목 셀이 데이터 셀과 올바르게 연결되도록 하세요.' },
  'td-headers-attr': { kwcag: '5.3.1', name: '표의 구성', principle: '인식의 용이성', severity: 'major', fix: '<td>의 headers 속성을 수정하세요.' },
  'heading-order': { kwcag: '5.3.2', name: '콘텐츠의 선형구조', principle: '인식의 용이성', severity: 'minor', fix: '제목 수준을 순차적으로 사용하세요.' },
  'list': { kwcag: '5.3.2', name: '콘텐츠의 선형구조', principle: '인식의 용이성', severity: 'major', fix: '목록 요소를 올바르게 구성하세요.' },
  'listitem': { kwcag: '5.3.2', name: '콘텐츠의 선형구조', principle: '인식의 용이성', severity: 'major', fix: '<li>는 <ul>/<ol> 안에 있어야 합니다.' },
  'color-contrast': { kwcag: '5.4.3', name: '텍스트 콘텐츠의 명도 대비', principle: '인식의 용이성', severity: 'major', fix: '텍스트와 배경 간 명도 대비를 4.5:1 이상으로 조정하세요.' },
  'scrollable-region-focusable': { kwcag: '6.1.1', name: '키보드 사용 보장', principle: '운용의 용이성', severity: 'critical', fix: '스크롤 가능한 영역에 tabindex를 추가하세요.' },
  'nested-interactive': { kwcag: '6.1.1', name: '키보드 사용 보장', principle: '운용의 용이성', severity: 'critical', fix: '대화형 요소를 중첩하지 마세요.' },
  'tabindex': { kwcag: '6.1.2', name: '초점 이동과 표시', principle: '운용의 용이성', severity: 'major', fix: 'tabindex > 0을 제거하세요.' },
  'bypass': { kwcag: '6.4.1', name: '반복 영역 건너뛰기', principle: '운용의 용이성', severity: 'major', fix: '본문 바로가기 링크를 추가하세요.' },
  'document-title': { kwcag: '6.4.2', name: '제목 제공', principle: '운용의 용이성', severity: 'major', fix: '<title>에 페이지 제목을 작성하세요.' },
  'page-has-heading-one': { kwcag: '6.4.2', name: '제목 제공', principle: '운용의 용이성', severity: 'major', fix: '페이지에 <h1>을 추가하세요.' },
  'empty-heading': { kwcag: '6.4.2', name: '제목 제공', principle: '운용의 용이성', severity: 'minor', fix: '빈 제목에 텍스트를 추가하세요.' },
  'frame-title': { kwcag: '6.4.2', name: '제목 제공', principle: '운용의 용이성', severity: 'major', fix: '<iframe>에 title을 추가하세요.' },
  'link-name': { kwcag: '6.4.3', name: '적절한 링크 텍스트', principle: '운용의 용이성', severity: 'major', fix: '링크에 용도를 알 수 있는 텍스트를 추가하세요.' },
  'button-name': { kwcag: '6.4.3', name: '적절한 링크 텍스트', principle: '운용의 용이성', severity: 'major', fix: '버튼에 용도를 알 수 있는 텍스트를 추가하세요.' },
  'html-has-lang': { kwcag: '7.1.1', name: '기본 언어 표시', principle: '이해의 용이성', severity: 'major', fix: '<html>에 lang 속성을 추가하세요.' },
  'html-lang-valid': { kwcag: '7.1.1', name: '기본 언어 표시', principle: '이해의 용이성', severity: 'major', fix: '유효한 lang 값을 사용하세요.' },
  'label': { kwcag: '7.3.2', name: '레이블 제공', principle: '이해의 용이성', severity: 'critical', fix: '입력 필드에 <label>을 연결하세요.' },
  'select-name': { kwcag: '7.3.2', name: '레이블 제공', principle: '이해의 용이성', severity: 'critical', fix: '<select>에 레이블을 추가하세요.' },
  'autocomplete-valid': { kwcag: '7.3.4', name: '반복 입력 정보', principle: '이해의 용이성', severity: 'minor', fix: 'autocomplete 값을 유효한 값으로 수정하세요.' },
  'duplicate-id-aria': { kwcag: '8.1.1', name: '마크업 오류 방지', principle: '견고성', severity: 'major', fix: 'ARIA에서 참조하는 id 중복을 수정하세요.' },
  'duplicate-id-active': { kwcag: '8.1.1', name: '마크업 오류 방지', principle: '견고성', severity: 'major', fix: '활성 요소의 id 중복을 수정하세요.' },
  'duplicate-id': { kwcag: '8.1.1', name: '마크업 오류 방지', principle: '견고성', severity: 'minor', fix: '중복 id를 고유한 값으로 수정하세요.' },
  'aria-allowed-attr': { kwcag: '8.2.1', name: '웹 애플리케이션 접근성 준수', principle: '견고성', severity: 'critical', fix: '허용되지 않는 ARIA 속성을 제거하세요.' },
  'aria-required-attr': { kwcag: '8.2.1', name: '웹 애플리케이션 접근성 준수', principle: '견고성', severity: 'critical', fix: '필수 ARIA 속성을 추가하세요.' },
  'aria-roles': { kwcag: '8.2.1', name: '웹 애플리케이션 접근성 준수', principle: '견고성', severity: 'critical', fix: '유효한 ARIA role을 사용하세요.' },
  'aria-valid-attr': { kwcag: '8.2.1', name: '웹 애플리케이션 접근성 준수', principle: '견고성', severity: 'critical', fix: '유효한 ARIA 속성을 사용하세요.' },
  'aria-valid-attr-value': { kwcag: '8.2.1', name: '웹 애플리케이션 접근성 준수', principle: '견고성', severity: 'critical', fix: 'ARIA 속성 값을 수정하세요.' },
  'aria-hidden-focus': { kwcag: '8.2.1', name: '웹 애플리케이션 접근성 준수', principle: '견고성', severity: 'critical', fix: 'aria-hidden 내 포커스 가능한 요소를 제거하세요.' },
};

// axe-core impact -> 우리 severity 매핑 (매핑 테이블에 없는 규칙용)
const IMPACT_TO_SEVERITY = {
  critical: 'critical',
  serious: 'major',
  moderate: 'major',
  minor: 'minor',
};

// axe-core tag -> KWCAG 원칙 매핑 (매핑 테이블에 없는 규칙용)
const WCAG_TAG_TO_PRINCIPLE = {
  'wcag2a': '기본 접근성',
  'wcag2aa': '향상된 접근성',
  'wcag2aaa': '최고 수준 접근성',
  'wcag21a': '기본 접근성 (2.1)',
  'wcag21aa': '향상된 접근성 (2.1)',
  'wcag22aa': '향상된 접근성 (2.2)',
  'best-practice': '권장 사항',
};

// ---------------------------------------------------------------------------
// CLI 인자 파서
// ---------------------------------------------------------------------------
function parseArgs(argv) {
  const args = argv.slice(2);
  const parsed = {
    target: null,
    format: 'json',
    severity: 'all',
  };

  let i = 0;
  while (i < args.length) {
    const arg = args[i];
    if (arg === '--format' && i + 1 < args.length) {
      const val = args[i + 1].toLowerCase();
      if (!['json', 'md'].includes(val)) {
        console.error(`[오류] 지원하지 않는 형식입니다: ${val} (json 또는 md만 가능)`);
        process.exit(1);
      }
      parsed.format = val;
      i += 2;
    } else if (arg === '--severity' && i + 1 < args.length) {
      const val = args[i + 1].toLowerCase();
      if (!['critical', 'major', 'minor', 'all'].includes(val)) {
        console.error(`[오류] 지원하지 않는 심각도입니다: ${val} (critical, major, minor, all 중 선택)`);
        process.exit(1);
      }
      parsed.severity = val;
      i += 2;
    } else if (arg === '--help' || arg === '-h') {
      printUsage();
      process.exit(0);
    } else if (!arg.startsWith('--')) {
      parsed.target = arg;
      i += 1;
    } else {
      console.error(`[오류] 알 수 없는 옵션입니다: ${arg}`);
      printUsage();
      process.exit(1);
    }
  }

  if (!parsed.target) {
    console.error('[오류] 검사할 HTML 파일 또는 디렉토리 경로를 지정하세요.');
    printUsage();
    process.exit(1);
  }

  return parsed;
}

function printUsage() {
  console.error('');
  console.error('사용법: node kwcag-axe-check.js <파일 또는 디렉토리> [옵션]');
  console.error('');
  console.error('옵션:');
  console.error('  --format json|md          출력 형식 (기본: json)');
  console.error('  --severity critical|major|minor|all  심각도 필터 (기본: all)');
  console.error('  --help, -h                도움말 표시');
  console.error('');
  console.error('예시:');
  console.error('  node kwcag-axe-check.js index.html');
  console.error('  node kwcag-axe-check.js ./pages --format md --severity critical');
  console.error('');
}

// ---------------------------------------------------------------------------
// 파일 탐색 -- 디렉토리 재귀 순회, *.html 수집
// ---------------------------------------------------------------------------
function collectHtmlFiles(targetPath) {
  const resolved = path.resolve(targetPath);

  if (!fs.existsSync(resolved)) {
    console.error(`[오류] 경로를 찾을 수 없습니다: ${resolved}`);
    process.exit(1);
  }

  const stat = fs.statSync(resolved);

  if (stat.isFile()) {
    if (!resolved.toLowerCase().endsWith('.html') && !resolved.toLowerCase().endsWith('.htm')) {
      console.error(`[오류] HTML 파일이 아닙니다: ${resolved}`);
      process.exit(1);
    }
    return [resolved];
  }

  if (stat.isDirectory()) {
    return walkDirectory(resolved);
  }

  console.error(`[오류] 파일 또는 디렉토리가 아닙니다: ${resolved}`);
  process.exit(1);
}

function walkDirectory(dirPath) {
  const results = [];
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      // node_modules, .git 등 제외
      if (['node_modules', '.git', '.svn', '__pycache__'].includes(entry.name)) {
        continue;
      }
      results.push(...walkDirectory(fullPath));
    } else if (entry.isFile()) {
      const lower = entry.name.toLowerCase();
      if (lower.endsWith('.html') || lower.endsWith('.htm')) {
        results.push(fullPath);
      }
    }
  }

  return results.sort();
}

// ---------------------------------------------------------------------------
// axe-core 실행 -- jsdom 위에서 axe-core를 주입하여 검사
// ---------------------------------------------------------------------------
async function runAxeOnHtml(htmlContent, filePath) {
  const dom = new JSDOM(htmlContent, {
    url: `file:///${filePath.replace(/\\/g, '/')}`,
    runScripts: 'dangerously',
    resources: 'usable',
    pretendToBeVisual: true,
  });

  const { window } = dom;
  const { document } = window;

  // axe-core 소스를 jsdom 환경에 주입
  const scriptEl = document.createElement('script');
  scriptEl.textContent = axeSource;
  document.head.appendChild(scriptEl);

  // axe 객체 존재 확인
  if (!window.axe) {
    throw new Error('axe-core 주입에 실패했습니다.');
  }

  // axe-core 실행 -- 매핑 테이블에 포함된 규칙만 활성화
  const ruleIds = Object.keys(AXE_TO_KWCAG);
  const axeConfig = {
    runOnly: {
      type: 'rule',
      values: ruleIds,
    },
    resultTypes: ['violations'],
  };

  try {
    const results = await window.axe.run(document, axeConfig);
    window.close();
    return results;
  } catch (err) {
    window.close();
    throw err;
  }
}

// ---------------------------------------------------------------------------
// 위반 사항 매핑 -- axe-core 결과 -> KWCAG 통합 형식
// ---------------------------------------------------------------------------
function mapViolations(axeViolations, filePath, severityFilter) {
  const violations = [];

  for (const violation of axeViolations) {
    const ruleId = violation.id;
    const mapping = AXE_TO_KWCAG[ruleId];

    // 매핑 정보 결정 (매핑 테이블에 있으면 사용, 없으면 axe 정보로 보완)
    const kwcagId = mapping ? mapping.kwcag : '미매핑';
    const kwcagName = mapping ? mapping.name : violation.help;
    const principle = mapping ? mapping.principle : derivePrinciple(violation.tags);
    const severity = mapping ? mapping.severity : (IMPACT_TO_SEVERITY[violation.impact] || 'minor');
    const fixGuide = mapping ? mapping.fix : violation.help;

    // 심각도 필터 적용
    if (severityFilter !== 'all' && severity !== severityFilter) {
      continue;
    }

    // 각 위반 노드를 개별 violation으로 변환
    for (const node of violation.nodes) {
      violations.push({
        requirement_id: kwcagId,
        requirement_name: kwcagName,
        principle: principle,
        axe_rule_id: ruleId,
        severity: severity,
        element: node.html,
        selector: node.target ? node.target.join(' > ') : '',
        message: fixGuide,
        help_url: violation.helpUrl || '',
      });
    }
  }

  return violations;
}

function derivePrinciple(tags) {
  for (const tag of tags) {
    if (WCAG_TAG_TO_PRINCIPLE[tag]) {
      return WCAG_TAG_TO_PRINCIPLE[tag];
    }
  }
  return '기타';
}

// ---------------------------------------------------------------------------
// 요약 통계 생성
// ---------------------------------------------------------------------------
function buildSummary(violations) {
  const bySeverity = { critical: 0, major: 0, minor: 0 };
  const byPrinciple = {};

  for (const v of violations) {
    bySeverity[v.severity] = (bySeverity[v.severity] || 0) + 1;
    byPrinciple[v.principle] = (byPrinciple[v.principle] || 0) + 1;
  }

  return {
    total_violations: violations.length,
    by_severity: bySeverity,
    by_principle: byPrinciple,
  };
}

// ---------------------------------------------------------------------------
// 단일 파일 분석
// ---------------------------------------------------------------------------
async function analyzeFile(filePath, severityFilter) {
  const absolutePath = path.resolve(filePath);
  const htmlContent = fs.readFileSync(absolutePath, 'utf8');
  const relativePath = path.relative(process.cwd(), absolutePath);
  const displayPath = relativePath || absolutePath;

  console.error(`[검사 중] ${displayPath}`);

  try {
    const axeResults = await runAxeOnHtml(htmlContent, absolutePath);
    const violations = mapViolations(axeResults.violations, absolutePath, severityFilter);
    const summary = buildSummary(violations);

    return {
      file: displayPath.replace(/\\/g, '/'),
      timestamp: new Date().toISOString().replace(/\.\d{3}Z$/, ''),
      tier: 2,
      tool: 'axe-core',
      summary: summary,
      violations: violations,
    };
  } catch (err) {
    console.error(`[오류] ${displayPath} 검사 실패: ${err.message}`);
    return {
      file: displayPath.replace(/\\/g, '/'),
      timestamp: new Date().toISOString().replace(/\.\d{3}Z$/, ''),
      tier: 2,
      tool: 'axe-core',
      error: err.message,
      summary: { total_violations: 0, by_severity: {}, by_principle: {} },
      violations: [],
    };
  }
}

// ---------------------------------------------------------------------------
// 출력 포맷터 -- JSON
// ---------------------------------------------------------------------------
function formatJSON(allResults) {
  const output = allResults.length === 1 ? allResults[0] : allResults;
  return JSON.stringify(output, null, 2);
}

// ---------------------------------------------------------------------------
// 출력 포맷터 -- Markdown
// ---------------------------------------------------------------------------
function formatMarkdown(allResults) {
  const lines = [];

  lines.push('# KWCAG 2.2 접근성 검사 보고서 (Tier 2: axe-core)');
  lines.push('');
  lines.push(`> 검사 일시: ${new Date().toISOString().replace(/T/, ' ').replace(/\.\d{3}Z$/, '')}`);
  lines.push(`> 검사 파일 수: ${allResults.length}`);
  lines.push('');

  // 전체 요약
  const globalSummary = { total: 0, critical: 0, major: 0, minor: 0 };
  for (const result of allResults) {
    globalSummary.total += result.summary.total_violations;
    globalSummary.critical += result.summary.by_severity.critical || 0;
    globalSummary.major += result.summary.by_severity.major || 0;
    globalSummary.minor += result.summary.by_severity.minor || 0;
  }

  lines.push('## 전체 요약');
  lines.push('');
  lines.push(`| 항목 | 수량 |`);
  lines.push(`|------|------|`);
  lines.push(`| 총 위반 사항 | ${globalSummary.total} |`);
  lines.push(`| 심각 (Critical) | ${globalSummary.critical} |`);
  lines.push(`| 주요 (Major) | ${globalSummary.major} |`);
  lines.push(`| 경미 (Minor) | ${globalSummary.minor} |`);
  lines.push('');

  // 파일별 상세
  for (const result of allResults) {
    lines.push(`---`);
    lines.push('');
    lines.push(`## ${result.file}`);
    lines.push('');

    if (result.error) {
      lines.push(`> [!warning] 검사 오류: ${result.error}`);
      lines.push('');
      continue;
    }

    if (result.violations.length === 0) {
      lines.push('위반 사항이 없습니다.');
      lines.push('');
      continue;
    }

    lines.push(`총 ${result.summary.total_violations}건의 위반 사항이 발견되었습니다.`);
    lines.push('');

    // 원칙별 그룹핑
    const byPrinciple = groupBy(result.violations, 'principle');

    for (const [principle, violations] of Object.entries(byPrinciple)) {
      lines.push(`### ${principle}`);
      lines.push('');

      // 검사 항목별 그룹핑
      const byRequirement = groupBy(violations, 'requirement_id');

      for (const [reqId, reqViolations] of Object.entries(byRequirement)) {
        const first = reqViolations[0];
        const severityIcon = getSeverityIcon(first.severity);
        lines.push(`#### ${severityIcon} [${reqId}] ${first.requirement_name} (${reqViolations.length}건)`);
        lines.push('');

        lines.push(`| # | 심각도 | axe 규칙 | 요소 | 수정 방법 |`);
        lines.push(`|---|--------|---------|------|----------|`);

        reqViolations.forEach((v, idx) => {
          const element = truncate(escapeMarkdown(v.element), 60);
          lines.push(`| ${idx + 1} | ${getSeverityLabel(v.severity)} | \`${v.axe_rule_id}\` | \`${element}\` | ${v.message} |`);
        });

        lines.push('');
      }
    }
  }

  return lines.join('\n');
}

function groupBy(arr, key) {
  const groups = {};
  for (const item of arr) {
    const k = item[key];
    if (!groups[k]) groups[k] = [];
    groups[k].push(item);
  }
  return groups;
}

function getSeverityIcon(severity) {
  switch (severity) {
    case 'critical': return '[C]';
    case 'major': return '[M]';
    case 'minor': return '[m]';
    default: return '[-]';
  }
}

function getSeverityLabel(severity) {
  switch (severity) {
    case 'critical': return '심각';
    case 'major': return '주요';
    case 'minor': return '경미';
    default: return severity;
  }
}

function truncate(str, maxLen) {
  if (str.length <= maxLen) return str;
  return str.slice(0, maxLen - 3) + '...';
}

function escapeMarkdown(str) {
  return str.replace(/\|/g, '\\|').replace(/\n/g, ' ').replace(/\r/g, '');
}

// ---------------------------------------------------------------------------
// 메인 실행
// ---------------------------------------------------------------------------
async function main() {
  const { target, format, severity } = parseArgs(process.argv);
  const htmlFiles = collectHtmlFiles(target);

  if (htmlFiles.length === 0) {
    console.error('[경고] 검사할 HTML 파일이 없습니다.');
    process.exit(0);
  }

  console.error(`[시작] ${htmlFiles.length}개 파일 검사를 시작합니다.`);
  console.error('');

  const allResults = [];

  for (const filePath of htmlFiles) {
    const result = await analyzeFile(filePath, severity);
    allResults.push(result);
  }

  console.error('');

  // 전체 통계 출력 (stderr)
  let totalViolations = 0;
  for (const r of allResults) {
    totalViolations += r.summary.total_violations;
  }
  console.error(`[완료] ${allResults.length}개 파일, 총 ${totalViolations}건의 위반 사항 발견`);

  // 결과 출력 (stdout)
  const output = format === 'md' ? formatMarkdown(allResults) : formatJSON(allResults);
  process.stdout.write(output + '\n');

  // 위반 사항이 있으면 exit code 1
  process.exit(totalViolations > 0 ? 1 : 0);
}

main().catch((err) => {
  console.error(`[치명적 오류] ${err.message}`);
  process.exit(2);
});
