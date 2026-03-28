"""
TDD: Topics 허브 노트 자동 생성 테스트
새 태그 입력 시 Topics/{tag}.md가 없으면 자동 생성
"""
import pytest
from pathlib import Path
from src.topics import ensure_topic_notes


@pytest.fixture
def vault(tmp_path):
    (tmp_path / "Topics").mkdir()
    return str(tmp_path)


def test_creates_topic_file_for_new_tag(vault):
    """새 태그에 대한 Topics 노트 생성"""
    ensure_topic_notes(["Turnover Prediction"], vault_path=vault)
    assert (Path(vault) / "Topics" / "Turnover Prediction.md").exists()


def test_does_not_overwrite_existing_topic(vault):
    """이미 존재하는 Topics 노트는 덮어쓰지 않음"""
    existing = Path(vault) / "Topics" / "HR Analytics.md"
    existing.write_text("# 기존 내용", encoding="utf-8")

    ensure_topic_notes(["HR Analytics"], vault_path=vault)

    assert existing.read_text(encoding="utf-8") == "# 기존 내용"


def test_creates_multiple_topics(vault):
    """여러 태그를 한 번에 처리"""
    ensure_topic_notes(["AI", "NLP", "HRM"], vault_path=vault)
    assert (Path(vault) / "Topics" / "AI.md").exists()
    assert (Path(vault) / "Topics" / "NLP.md").exists()
    assert (Path(vault) / "Topics" / "HRM.md").exists()


def test_topic_file_has_header(vault):
    """생성된 Topics 노트에 h1 헤더 포함"""
    ensure_topic_notes(["Turnover Prediction"], vault_path=vault)
    content = (Path(vault) / "Topics" / "Turnover Prediction.md").read_text(encoding="utf-8")
    assert "# Turnover Prediction" in content


def test_topic_file_has_related_papers_section(vault):
    """생성된 Topics 노트에 관련 논문 섹션 포함"""
    ensure_topic_notes(["Turnover Prediction"], vault_path=vault)
    content = (Path(vault) / "Topics" / "Turnover Prediction.md").read_text(encoding="utf-8")
    assert "## 관련 논문" in content


def test_topic_file_has_research_connection_section(vault):
    """내 연구와의 연결 섹션 포함"""
    ensure_topic_notes(["Turnover Prediction"], vault_path=vault)
    content = (Path(vault) / "Topics" / "Turnover Prediction.md").read_text(encoding="utf-8")
    assert "## 내 연구와의 연결" in content


def test_returns_list_of_created_topics(vault):
    """새로 생성된 태그 목록 반환"""
    (Path(vault) / "Topics" / "HR Analytics.md").write_text("기존", encoding="utf-8")

    created = ensure_topic_notes(["HR Analytics", "AI", "NLP"], vault_path=vault)
    assert set(created) == {"AI", "NLP"}


def test_empty_tags_returns_empty(vault):
    created = ensure_topic_notes([], vault_path=vault)
    assert created == []
