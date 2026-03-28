"""
통합 파이프라인: DOI/URL → 메타데이터 → APA 인용 → Obsidian 노트 저장
"""
from datetime import date
from pathlib import Path

from src.fetch_metadata import fetch_by_doi
from src.generate_apa import generate_apa_citation
from src.create_note import build_note_content, get_note_path
from config import VAULT_PATH


def add_paper(
    doi: str = None,
    vault_path: str = VAULT_PATH,
    tags: list = None,
    read_date: str = None,
) -> dict:
    """
    DOI → Obsidian 노트 파일 생성 전체 파이프라인

    Args:
        doi: DOI 문자열 또는 https://doi.org/... URL
        vault_path: Obsidian Vault 경로
        tags: 연구 주제 태그 목록
        read_date: 독서 날짜 (기본값: 오늘)

    Returns:
        {note_path, apa_citation, metadata}
    """
    if tags is None:
        tags = []
    if read_date is None:
        read_date = date.today().isoformat()

    # 1. 메타데이터 추출
    metadata = fetch_by_doi(doi)

    # 2. APA 인용문 생성
    apa = generate_apa_citation(metadata)

    # 3. 노트 콘텐츠 빌드
    metadata["apa_citation"] = apa
    metadata["read_date"] = read_date
    metadata["tags"] = tags

    content = build_note_content(metadata)

    # 4. 파일 저장
    note_path = get_note_path(metadata, vault_path=vault_path)
    Path(note_path).write_text(content, encoding="utf-8")

    return {
        "note_path": note_path,
        "apa_citation": apa,
        "metadata": metadata,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="논문을 Obsidian Vault에 추가합니다.")
    parser.add_argument("--doi", required=True, help="DOI 또는 https://doi.org/... URL")
    parser.add_argument("--tags", nargs="*", default=[], help="연구 주제 태그 (공백 구분)")
    parser.add_argument("--date", dest="read_date", default=None, help="독서 날짜 (YYYY-MM-DD)")
    args = parser.parse_args()

    result = add_paper(doi=args.doi, tags=args.tags, read_date=args.read_date)
    print(f"[OK] 노트 생성: {result['note_path']}")
    print(f"\nAPA: {result['apa_citation']}")
