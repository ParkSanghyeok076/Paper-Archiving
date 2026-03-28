"""
TDD: 통합 CLI add_paper 파이프라인 테스트
fetch_metadata → generate_apa → create_note → 파일 저장
"""
import pytest
from pathlib import Path
from unittest.mock import patch, Mock
from src.add_paper import add_paper


MOCK_METADATA = {
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
    "abstract": "This paper examines AI adoption in HR.",
}


@pytest.fixture
def vault(tmp_path):
    """임시 Vault 경로"""
    return str(tmp_path)


def test_add_paper_creates_note_file(vault):
    """DOI 입력 시 Obsidian 노트 파일이 생성됨"""
    with patch("src.add_paper.fetch_by_doi", return_value=MOCK_METADATA):
        result = add_paper(doi="10.1037/apl0000123", vault_path=vault, tags=["AI", "HRM"])

    assert Path(result["note_path"]).exists()


def test_add_paper_returns_note_path(vault):
    """반환값에 생성된 노트 경로 포함"""
    with patch("src.add_paper.fetch_by_doi", return_value=MOCK_METADATA):
        result = add_paper(doi="10.1037/apl0000123", vault_path=vault, tags=["AI"])

    assert "note_path" in result
    assert result["note_path"].endswith(".md")


def test_add_paper_note_contains_apa(vault):
    """생성된 노트에 APA 인용문 포함"""
    with patch("src.add_paper.fetch_by_doi", return_value=MOCK_METADATA):
        result = add_paper(doi="10.1037/apl0000123", vault_path=vault, tags=["AI"])

    content = Path(result["note_path"]).read_text(encoding="utf-8")
    assert "Smith, J. A., & Jones, B. (2024)" in content
    assert "https://doi.org/10.1037/apl0000123" in content


def test_add_paper_note_has_read_date(vault):
    """생성된 노트 frontmatter에 오늘 날짜 read_date 포함"""
    with patch("src.add_paper.fetch_by_doi", return_value=MOCK_METADATA):
        result = add_paper(doi="10.1037/apl0000123", vault_path=vault, tags=["AI"])

    content = Path(result["note_path"]).read_text(encoding="utf-8")
    assert "read_date:" in content


def test_add_paper_note_has_tags(vault):
    """생성된 노트에 입력한 태그 포함"""
    with patch("src.add_paper.fetch_by_doi", return_value=MOCK_METADATA):
        result = add_paper(doi="10.1037/apl0000123", vault_path=vault, tags=["AI", "HRM"])

    content = Path(result["note_path"]).read_text(encoding="utf-8")
    assert "- AI" in content
    assert "- HRM" in content


def test_add_paper_returns_apa_citation(vault):
    """반환값에 APA 인용문 포함"""
    with patch("src.add_paper.fetch_by_doi", return_value=MOCK_METADATA):
        result = add_paper(doi="10.1037/apl0000123", vault_path=vault, tags=[])

    assert "apa_citation" in result
    assert "Smith" in result["apa_citation"]


def test_add_paper_propagates_fetch_error(vault):
    """DOI 없을 때 ValueError 전파"""
    with patch("src.add_paper.fetch_by_doi", side_effect=ValueError("DOI not found")):
        with pytest.raises(ValueError, match="DOI not found"):
            add_paper(doi="10.9999/bad", vault_path=vault, tags=[])


def test_add_paper_default_tags_empty(vault):
    """tags 미입력 시 빈 리스트로 처리"""
    with patch("src.add_paper.fetch_by_doi", return_value=MOCK_METADATA):
        result = add_paper(doi="10.1037/apl0000123", vault_path=vault)

    assert Path(result["note_path"]).exists()
