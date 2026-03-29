"""
TDD: Claude API를 이용한 논문 노트 자동 요약 테스트
"""
import pytest
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock
from src.fill_note import fill_note_sections, update_note_file, SECTION_MARKERS


SAMPLE_NOTE = """---
title: "Is anthropomorphizing AI worth it?"
authors:
  - "Li, S."
year: 2026
doi: "10.1016/j.chb.2026.108983"
read_date: 2026-03-29
tags:
  - AI
status: reading
---

# Is anthropomorphizing AI worth it?

## APA Citation
Li, S. et al. (2026). ...

## Abstract Summary
> This study examines whether anthropomorphizing AI affects advice uptake.

## 핵심 주장 (1-2문장)


## 이론적 배경
- 기반 이론:
- 선행 연구와의 관계:

## 연구 방법
| 항목 | 내용 |
|------|------|
| 연구 설계 | |
| 샘플 | N= , 산업/직종: |
| 주요 변수 | |
| 측정 도구 | |
| 분석 방법 | |

## 주요 결과
-

## 한계점 및 향후 연구
-

## 내 연구와의 연결
### 인용 포인트 (어떤 주장 뒷받침에 쓸 수 있나)

### 방법론 참고할 점

### 비판적 메모

## Related Topics
- [[Topics/AI]]
"""

MOCK_CLAUDE_RESPONSE = """## 핵심 주장
AI를 의인화하는 것이 조언 수용에 긍정적 영향을 미치지만, 이는 직접 경험 여부에 따라 조절된다.

## 이론적 배경
- 기반 이론: 기술 수용 모델(TAM), 의인화 이론
- 선행 연구와의 관계: AI 신뢰 및 수용 연구의 연장선

## 연구 방법
| 항목 | 내용 |
|------|------|
| 연구 설계 | 실험 연구 (온라인) |
| 샘플 | N=412, 일반 성인 |
| 주요 변수 | AI 의인화, 조언 수용, 직접 경험 |
| 측정 도구 | 설문 (Likert 5점) |
| 분석 방법 | 조절 매개 분석 (PROCESS) |

## 주요 결과
- AI 의인화는 조언 수용을 증가시킴
- 직접 경험이 있을 때 효과가 약화됨

## 한계점 및 향후 연구
- 온라인 샘플의 일반화 한계
- 장기적 효과 미검증
"""


@pytest.fixture
def note_file(tmp_path):
    f = tmp_path / "test_note.md"
    f.write_text(SAMPLE_NOTE, encoding="utf-8")
    return str(f)


# --- fill_note_sections 테스트 ---

def test_fill_note_sections_returns_updated_content(note_file):
    """Claude API 응답으로 빈 섹션이 채워진 노트 반환"""
    with patch("src.fill_note.call_claude_api", return_value=MOCK_CLAUDE_RESPONSE):
        result = fill_note_sections(note_file)

    assert "AI를 의인화하는 것이" in result


def test_fill_note_sections_preserves_frontmatter(note_file):
    """YAML frontmatter 보존"""
    with patch("src.fill_note.call_claude_api", return_value=MOCK_CLAUDE_RESPONSE):
        result = fill_note_sections(note_file)

    assert "doi: " in result
    assert "read_date:" in result


def test_fill_note_sections_preserves_apa(note_file):
    """APA 인용문 보존"""
    with patch("src.fill_note.call_claude_api", return_value=MOCK_CLAUDE_RESPONSE):
        result = fill_note_sections(note_file)

    assert "## APA Citation" in result


def test_fill_note_sections_preserves_related_topics(note_file):
    """Related Topics 위키링크 보존"""
    with patch("src.fill_note.call_claude_api", return_value=MOCK_CLAUDE_RESPONSE):
        result = fill_note_sections(note_file)

    assert "[[Topics/AI]]" in result


# --- update_note_file 테스트 ---

def test_update_note_file_writes_to_disk(note_file):
    """업데이트된 내용이 파일에 저장됨"""
    new_content = SAMPLE_NOTE.replace("## 핵심 주장 (1-2문장)", "## 핵심 주장 (1-2문장)\n업데이트된 내용")
    update_note_file(note_file, new_content)

    saved = Path(note_file).read_text(encoding="utf-8")
    assert "업데이트된 내용" in saved


def test_update_note_file_updates_status_to_done(note_file):
    """파일 저장 시 status: reading → done으로 변경"""
    with patch("src.fill_note.call_claude_api", return_value=MOCK_CLAUDE_RESPONSE):
        result = fill_note_sections(note_file)
    update_note_file(note_file, result)

    saved = Path(note_file).read_text(encoding="utf-8")
    assert "status: done" in saved
