"""
TDD: CrossRef API 메타데이터 추출 테스트
네트워크 호출은 mock으로 처리
"""
import pytest
from unittest.mock import patch, Mock
from src.fetch_metadata import fetch_by_doi, parse_crossref_response


SAMPLE_CROSSREF_RESPONSE = {
    "status": "ok",
    "message": {
        "title": ["The impact of AI on HR practices"],
        "author": [
            {"family": "Smith", "given": "John A."},
            {"family": "Jones", "given": "Beth"},
        ],
        "published": {"date-parts": [[2020, 3, 15]]},
        "container-title": ["Journal of Applied Psychology"],
        "volume": "105",
        "issue": "3",
        "page": "300-320",
        "DOI": "10.1037/apl0000123",
        "abstract": "<jats:p>This paper examines AI adoption in HR.</jats:p>",
    }
}


# --- parse_crossref_response 테스트 (순수 함수) ---

def test_parse_extracts_title():
    result = parse_crossref_response(SAMPLE_CROSSREF_RESPONSE)
    assert result["title"] == "The impact of AI on HR practices"


def test_parse_extracts_authors():
    result = parse_crossref_response(SAMPLE_CROSSREF_RESPONSE)
    assert result["authors"] == [
        {"family": "Smith", "given": "John A."},
        {"family": "Jones", "given": "Beth"},
    ]


def test_parse_extracts_year():
    result = parse_crossref_response(SAMPLE_CROSSREF_RESPONSE)
    assert result["year"] == 2020


def test_parse_extracts_journal():
    result = parse_crossref_response(SAMPLE_CROSSREF_RESPONSE)
    assert result["journal"] == "Journal of Applied Psychology"


def test_parse_extracts_volume_issue_pages():
    result = parse_crossref_response(SAMPLE_CROSSREF_RESPONSE)
    assert result["volume"] == "105"
    assert result["issue"] == "3"
    assert result["pages"] == "300-320"


def test_parse_extracts_doi():
    result = parse_crossref_response(SAMPLE_CROSSREF_RESPONSE)
    assert result["doi"] == "10.1037/apl0000123"


def test_parse_strips_jats_tags_from_abstract():
    """CrossRef abstract는 JATS XML 태그 포함 — 제거해야 함"""
    result = parse_crossref_response(SAMPLE_CROSSREF_RESPONSE)
    assert result["abstract"] == "This paper examines AI adoption in HR."
    assert "<jats:p>" not in result["abstract"]


def test_parse_handles_missing_abstract():
    response = {
        "status": "ok",
        "message": {**SAMPLE_CROSSREF_RESPONSE["message"]}
    }
    del response["message"]["abstract"]
    result = parse_crossref_response(response)
    assert result["abstract"] is None


def test_parse_handles_missing_issue():
    response = {
        "status": "ok",
        "message": {**SAMPLE_CROSSREF_RESPONSE["message"]}
    }
    del response["message"]["issue"]
    result = parse_crossref_response(response)
    assert result["issue"] is None


def test_parse_handles_missing_pages():
    response = {
        "status": "ok",
        "message": {**SAMPLE_CROSSREF_RESPONSE["message"]}
    }
    del response["message"]["page"]
    result = parse_crossref_response(response)
    assert result["pages"] is None


# --- fetch_by_doi 테스트 (네트워크 mock) ---

def test_fetch_by_doi_calls_correct_url():
    """CrossRef API URL 형식 검증: https://api.crossref.org/works/{doi}"""
    with patch("src.fetch_metadata.requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: SAMPLE_CROSSREF_RESPONSE
        )
        fetch_by_doi("10.1037/apl0000123")
        called_url = mock_get.call_args[0][0]
        assert called_url == "https://api.crossref.org/works/10.1037/apl0000123"


def test_fetch_by_doi_returns_parsed_metadata():
    with patch("src.fetch_metadata.requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: SAMPLE_CROSSREF_RESPONSE
        )
        result = fetch_by_doi("10.1037/apl0000123")
        assert result["title"] == "The impact of AI on HR practices"
        assert result["year"] == 2020


def test_fetch_by_doi_raises_on_404():
    """DOI가 없을 때 명확한 에러 반환"""
    with patch("src.fetch_metadata.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=404)
        with pytest.raises(ValueError, match="DOI not found"):
            fetch_by_doi("10.9999/nonexistent")


def test_fetch_by_doi_raises_on_network_error():
    """네트워크 오류 시 명확한 에러 반환"""
    import requests as req
    with patch("src.fetch_metadata.requests.get") as mock_get:
        mock_get.side_effect = req.exceptions.ConnectionError("Network error")
        with pytest.raises(ConnectionError, match="CrossRef API"):
            fetch_by_doi("10.1037/apl0000123")


def test_fetch_by_doi_strips_doi_prefix():
    """사용자가 'https://doi.org/10.xxx' 형태로 입력해도 처리"""
    with patch("src.fetch_metadata.requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=lambda: SAMPLE_CROSSREF_RESPONSE
        )
        fetch_by_doi("https://doi.org/10.1037/apl0000123")
        called_url = mock_get.call_args[0][0]
        assert called_url == "https://api.crossref.org/works/10.1037/apl0000123"
