"""
APA 7판 인용문 생성
"""
import re


def _format_author(author: dict) -> str:
    """저자 딕셔너리 → APA 형식 (Last, F. M.)"""
    family = author.get("family", "")
    given = author.get("given", "")

    # 이름 이니셜 처리: "John A." → "J. A."
    initials = " ".join(
        part[0] + "." for part in given.split() if part
    )
    if initials:
        return f"{family}, {initials}"
    return family


def _format_author_list(authors: list) -> str:
    """저자 목록 → APA 7판 형식"""
    n = len(authors)

    if n == 0:
        return ""

    if n <= 20:
        formatted = [_format_author(a) for a in authors]
        if n == 1:
            return formatted[0]
        return ", ".join(formatted[:-1]) + ", & " + formatted[-1]

    # 21명 이상: 처음 19명 + ... + 마지막 저자
    first_19 = [_format_author(a) for a in authors[:19]]
    last = _format_author(authors[-1])
    return ", ".join(first_19) + ", ... " + last


def generate_apa_citation(metadata: dict) -> str:
    """
    메타데이터 딕셔너리 → APA 7판 인용문 문자열

    형식: Author(s). (Year). Title. Journal, Volume(Issue), pages. https://doi.org/xxx
    """
    authors_str = _format_author_list(metadata.get("authors", []))
    year = metadata.get("year", "n.d.")
    title = metadata.get("title", "")
    journal = metadata.get("journal", "")
    volume = metadata.get("volume", "")
    issue = metadata.get("issue")
    pages = metadata.get("pages")
    doi = metadata.get("doi", "")

    # 저널 + 권호 + 페이지
    journal_part = journal
    if volume:
        journal_part += f", {volume}"
        if issue:
            journal_part += f"({issue})"
    if pages:
        journal_part += f", {pages}"

    doi_url = f"https://doi.org/{doi}" if doi else ""

    parts = [
        f"{authors_str.rstrip('.')}. ({year}).",
        f"{title}.",
        f"{journal_part}.",
    ]
    if doi_url:
        parts.append(doi_url)

    return " ".join(parts)
