"""
TDD: Reading Log 자동 업데이트 테스트
논문 추가 시 Reading Log/{date}.md에 항목 추가
"""
import pytest
from pathlib import Path
from src.reading_log import append_to_reading_log, get_log_path


SAMPLE_ENTRY = {
    "title": "The impact of AI on HR practices",
    "note_path": "Papers/2024/2024-Smith-the-impact-of-ai-on-hr-practices.md",
    "tags": ["AI", "HRM"],
    "apa_citation": "Smith, J. A., & Jones, B. (2024). The impact of AI on HR practices. Journal of Applied Psychology, 105(3), 300-320. https://doi.org/10.1037/apl0000123",
}


@pytest.fixture
def vault(tmp_path):
    (tmp_path / "Reading Log").mkdir()
    return str(tmp_path)


# --- get_log_path 테스트 ---

def test_get_log_path_format(tmp_path):
    path = get_log_path("2026-03-29", vault_path=str(tmp_path))
    assert path == str(tmp_path / "Reading Log" / "2026-03-29.md")


def test_get_log_path_creates_reading_log_dir(tmp_path):
    get_log_path("2026-03-29", vault_path=str(tmp_path))
    assert (tmp_path / "Reading Log").exists()


# --- append_to_reading_log 테스트 ---

def test_creates_log_file_if_not_exists(vault):
    """로그 파일이 없으면 새로 생성"""
    append_to_reading_log(SAMPLE_ENTRY, date="2026-03-29", vault_path=vault)
    log_path = Path(vault) / "Reading Log" / "2026-03-29.md"
    assert log_path.exists()


def test_new_log_has_date_header(vault):
    """새 로그 파일에 날짜 헤더 포함"""
    append_to_reading_log(SAMPLE_ENTRY, date="2026-03-29", vault_path=vault)
    content = (Path(vault) / "Reading Log" / "2026-03-29.md").read_text(encoding="utf-8")
    assert "# Reading Log — 2026-03-29" in content


def test_log_contains_paper_title(vault):
    append_to_reading_log(SAMPLE_ENTRY, date="2026-03-29", vault_path=vault)
    content = (Path(vault) / "Reading Log" / "2026-03-29.md").read_text(encoding="utf-8")
    assert "The impact of AI on HR practices" in content


def test_log_contains_wikilink_to_note(vault):
    """노트 경로가 위키링크로 삽입됨"""
    append_to_reading_log(SAMPLE_ENTRY, date="2026-03-29", vault_path=vault)
    content = (Path(vault) / "Reading Log" / "2026-03-29.md").read_text(encoding="utf-8")
    assert "[[Papers/2024/2024-Smith-the-impact-of-ai-on-hr-practices]]" in content


def test_log_contains_tags(vault):
    append_to_reading_log(SAMPLE_ENTRY, date="2026-03-29", vault_path=vault)
    content = (Path(vault) / "Reading Log" / "2026-03-29.md").read_text(encoding="utf-8")
    assert "AI" in content
    assert "HRM" in content


def test_appends_to_existing_log(vault):
    """같은 날짜 로그가 있으면 항목을 추가 (덮어쓰기 아님)"""
    entry2 = {**SAMPLE_ENTRY, "title": "Second paper today"}

    append_to_reading_log(SAMPLE_ENTRY, date="2026-03-29", vault_path=vault)
    append_to_reading_log(entry2, date="2026-03-29", vault_path=vault)

    content = (Path(vault) / "Reading Log" / "2026-03-29.md").read_text(encoding="utf-8")
    assert "The impact of AI on HR practices" in content
    assert "Second paper today" in content


def test_date_header_not_duplicated(vault):
    """같은 날짜 로그에 헤더가 중복 추가되지 않음"""
    append_to_reading_log(SAMPLE_ENTRY, date="2026-03-29", vault_path=vault)
    append_to_reading_log(SAMPLE_ENTRY, date="2026-03-29", vault_path=vault)

    content = (Path(vault) / "Reading Log" / "2026-03-29.md").read_text(encoding="utf-8")
    assert content.count("# Reading Log — 2026-03-29") == 1
