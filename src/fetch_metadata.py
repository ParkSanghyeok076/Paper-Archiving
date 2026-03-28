"""
CrossRef API를 통한 논문 메타데이터 추출
"""
import re
import requests


def _strip_jats_tags(text: str) -> str:
    """JATS XML 태그 제거"""
    return re.sub(r"<[^>]+>", "", text).strip()


def _normalize_doi(doi: str) -> str:
    """DOI 정규화: URL 접두사 제거"""
    doi = doi.strip()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.lower().startswith(prefix):
            return doi[len(prefix):]
    return doi


def parse_crossref_response(response: dict) -> dict:
    """CrossRef API 응답 → 정규화된 메타데이터 딕셔너리"""
    msg = response["message"]

    title_list = msg.get("title", [""])
    title = title_list[0] if title_list else ""

    authors = msg.get("author", [])

    date_parts = msg.get("published", {}).get("date-parts", [[None]])
    year = date_parts[0][0] if date_parts and date_parts[0] else None

    journal_list = msg.get("container-title", [""])
    journal = journal_list[0] if journal_list else ""

    abstract_raw = msg.get("abstract")
    abstract = _strip_jats_tags(abstract_raw) if abstract_raw else None

    return {
        "title": title,
        "authors": authors,
        "year": year,
        "journal": journal,
        "volume": msg.get("volume"),
        "issue": msg.get("issue"),
        "pages": msg.get("page"),
        "doi": msg.get("DOI"),
        "abstract": abstract,
    }


def fetch_by_doi(doi: str) -> dict:
    """
    DOI로 CrossRef API 호출 → 메타데이터 반환

    Args:
        doi: DOI 문자열 또는 https://doi.org/... URL

    Returns:
        정규화된 메타데이터 딕셔너리

    Raises:
        ValueError: DOI를 찾을 수 없을 때
        ConnectionError: 네트워크 오류
    """
    doi = _normalize_doi(doi)
    url = f"https://api.crossref.org/works/{doi}"

    try:
        response = requests.get(url, headers={"User-Agent": "PaperArchiver/1.0"})
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"CrossRef API 연결 실패: {e}") from e

    if response.status_code == 404:
        raise ValueError(f"DOI not found: {doi}")

    response.raise_for_status()
    return parse_crossref_response(response.json())
