"""
TDD: Obsidian 논문 노트 생성 테스트
"""
import pytest
from pathlib import Path
from src.create_note import build_note_content, get_note_path, slugify


SAMPLE_METADATA = {
    "title": "The impact of AI on HR practices",
    "authors": [
        {"family": "Smith", "given": "John A."},
        {"family": "Jones", "given": "Beth"},
    ],
    "year": 2024,
    "journal": "Journal of Applied Psychology",
    "volume": "105",
    "issue": "3",
    "pages": "300-320",
    "doi": "10.1037/apl0000123",
    "abstract": "This paper examines AI adoption in HR departments.",
    "apa_citation": "Smith, J. A., & Jones, B. (2024). The impact of AI on HR practices. Journal of Applied Psychology, 105(3), 300-320. https://doi.org/10.1037/apl0000123",
    "read_date": "2026-03-28",
    "tags": ["AI", "HRM", "HR Analytics"],
}


# --- slugify 테스트 ---

def test_slugify_basic():
    assert slugify("The impact of AI on HR practices") == "the-impact-of-ai-on-hr-practices"


def test_slugify_removes_special_chars():
    assert slugify("Work & Life: A Study") == "work-life-a-study"


def test_slugify_truncates_long_titles():
    long_title = "A " * 30  # 60 chars
    result = slugify(long_title)
    assert len(result) <= 50


# --- get_note_path 테스트 ---

def test_get_note_path_format(tmp_path):
    """경로 형식: Papers/{year}-{first_author_family}-{slug}.md (flat)"""
    path = get_note_path(SAMPLE_METADATA, vault_path=str(tmp_path))
    assert path == str(tmp_path / "Papers" / "2024-Smith-the-impact-of-ai-on-hr-practices.md")


def test_get_note_path_creates_papers_directory(tmp_path):
    get_note_path(SAMPLE_METADATA, vault_path=str(tmp_path))
    assert (tmp_path / "Papers").exists()


# --- build_note_content 테스트 ---

def test_note_has_yaml_frontmatter():
    content = build_note_content(SAMPLE_METADATA)
    assert content.startswith("---\n")
    assert "\n---\n" in content


def test_note_frontmatter_has_required_fields():
    content = build_note_content(SAMPLE_METADATA)
    assert 'title: "The impact of AI on HR practices"' in content
    assert "year: 2024" in content
    assert 'doi: "10.1037/apl0000123"' in content
    assert "read_date: 2026-03-28" in content
    assert "status: reading" in content


def test_note_frontmatter_has_tags():
    content = build_note_content(SAMPLE_METADATA)
    assert "tags:" in content
    assert "- AI" in content
    assert "- HRM" in content
    assert "- HR Analytics" in content


def test_note_has_apa_citation_section():
    content = build_note_content(SAMPLE_METADATA)
    assert "## APA Citation" in content
    assert "Smith, J. A., & Jones, B. (2024)" in content


def test_note_has_abstract_section():
    content = build_note_content(SAMPLE_METADATA)
    assert "## Abstract Summary" in content
    assert "This paper examines AI adoption in HR departments." in content


def test_note_has_core_argument_section():
    content = build_note_content(SAMPLE_METADATA)
    assert "## 핵심 주장" in content


def test_note_has_theoretical_background_section():
    content = build_note_content(SAMPLE_METADATA)
    assert "## 이론적 배경" in content


def test_note_has_research_method_table():
    content = build_note_content(SAMPLE_METADATA)
    assert "## 연구 방법" in content
    assert "| 항목 |" in content


def test_note_has_key_results_section():
    content = build_note_content(SAMPLE_METADATA)
    assert "## 주요 결과" in content


def test_note_has_limitations_section():
    content = build_note_content(SAMPLE_METADATA)
    assert "## 한계점 및 향후 연구" in content


def test_note_has_research_connection_section():
    content = build_note_content(SAMPLE_METADATA)
    assert "## 내 연구와의 연결" in content
    assert "인용 포인트" in content
    assert "방법론 참고할 점" in content
    assert "비판적 메모" in content


def test_note_has_related_topics_wikilinks():
    content = build_note_content(SAMPLE_METADATA)
    assert "## Related Topics" in content
    assert "[[Topics/" in content


def test_note_tags_map_to_topic_wikilinks():
    """tags 목록이 Related Topics 위키링크에 반영됨"""
    content = build_note_content(SAMPLE_METADATA)
    assert "[[Topics/AI]]" in content
    assert "[[Topics/HRM]]" in content
    assert "[[Topics/HR Analytics]]" in content


def test_note_handles_missing_abstract():
    metadata = {**SAMPLE_METADATA, "abstract": None}
    content = build_note_content(metadata)
    assert "## Abstract Summary" in content
    assert "None" not in content
