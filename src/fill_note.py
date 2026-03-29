"""
Claude API를 이용한 논문 노트 자동 요약
빈 섹션을 Claude가 채워줌
"""
import os
import re
from pathlib import Path
import anthropic

# 자동 채울 섹션의 시작/끝 마커
SECTION_MARKERS = {
    "start": "## 핵심 주장",
    "end": "## Related Topics",
}

SYSTEM_PROMPT = """당신은 HR 및 AI 분야 연구자를 돕는 학술 논문 요약 전문가입니다.
논문 정보를 바탕으로 다음 섹션을 한국어로 간결하게 작성하세요.
반드시 아래 마크다운 형식을 그대로 유지하세요."""

USER_PROMPT_TEMPLATE = """다음 논문을 분석하여 각 섹션을 채워주세요.

제목: {title}
저자: {authors}
저널: {journal} ({year})
초록: {abstract}

아래 형식으로 작성하세요 (형식 변경 금지):

## 핵심 주장 (1-2문장)
[논문의 핵심 주장을 1-2문장으로 작성]

## 이론적 배경
- 기반 이론: [주요 이론]
- 선행 연구와의 관계: [이 논문이 선행 연구와 어떻게 연결되는지]

## 연구 방법
| 항목 | 내용 |
|------|------|
| 연구 설계 | [연구 설계 방법] |
| 샘플 | N=[숫자], [산업/직종 특성] |
| 주요 변수 | [독립변수, 종속변수] |
| 측정 도구 | [측정 방법] |
| 분석 방법 | [통계 분석 방법] |

## 주요 결과
- [결과 1]
- [결과 2]

## 한계점 및 향후 연구
- [한계점]
- [향후 연구 방향]

## 내 연구와의 연결
### 인용 포인트 (어떤 주장 뒷받침에 쓸 수 있나)
[인용 가능한 포인트]

### 방법론 참고할 점
[방법론에서 참고할 부분]

### 비판적 메모
[비판적 검토 사항]"""


def call_claude_api(title: str, authors: str, journal: str, year: int, abstract: str) -> str:
    """Claude API 호출 → 구조화된 섹션 내용 반환"""
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = USER_PROMPT_TEMPLATE.format(
        title=title,
        authors=authors,
        journal=journal,
        year=year,
        abstract=abstract or "(초록 없음)",
    )

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    return message.content[0].text


def _extract_frontmatter_value(content: str, key: str) -> str:
    """YAML frontmatter에서 값 추출"""
    match = re.search(rf'^{key}:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
    return match.group(1).strip('"') if match else ""


def _extract_abstract(content: str) -> str:
    """노트에서 Abstract Summary 섹션 추출"""
    match = re.search(r"## Abstract Summary\n>\s*(.+?)(?=\n##)", content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def fill_note_sections(note_path: str) -> str:
    """
    노트 파일을 읽어 빈 섹션을 Claude API로 채운 내용 반환

    Args:
        note_path: Obsidian 노트 파일 경로

    Returns:
        업데이트된 노트 전체 문자열
    """
    content = Path(note_path).read_text(encoding="utf-8")

    # 메타데이터 추출
    title = _extract_frontmatter_value(content, "title")
    year = _extract_frontmatter_value(content, "year")
    journal = _extract_frontmatter_value(content, "journal")
    abstract = _extract_abstract(content)

    # 저자 추출 (YAML 배열)
    authors_match = re.findall(r'^\s+- "(.+?)"', content, re.MULTILINE)
    authors_str = ", ".join(authors_match) if authors_match else ""

    # Claude API 호출
    filled = call_claude_api(
        title=title,
        authors=authors_str,
        journal=journal,
        year=int(year) if year.isdigit() else 0,
        abstract=abstract,
    )

    # 노트에서 채울 구간 교체
    start_marker = SECTION_MARKERS["start"]
    end_marker = SECTION_MARKERS["end"]

    before = content[:content.index(start_marker)]
    after_start = content[content.index(end_marker):]

    return before + filled.strip() + "\n\n" + after_start


def update_note_file(note_path: str, content: str) -> None:
    """
    업데이트된 내용을 파일에 저장하고 status를 done으로 변경

    Args:
        note_path: 저장할 파일 경로
        content: 업데이트된 노트 내용
    """
    updated = re.sub(r"^status: reading$", "status: done", content, flags=re.MULTILINE)
    Path(note_path).write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    import argparse
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="논문 노트 섹션을 Claude AI로 자동 채웁니다.")
    parser.add_argument("note_path", help="Obsidian 노트 파일 경로 (.md)")
    args = parser.parse_args()

    print(f"분석 중: {args.note_path}")
    updated_content = fill_note_sections(args.note_path)
    update_note_file(args.note_path, updated_content)
    print("[OK] 노트 업데이트 완료")
