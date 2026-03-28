"""
Reading Log 자동 업데이트
논문 추가 시 Reading Log/{date}.md에 항목 추가
"""
from pathlib import Path


def get_log_path(date: str, vault_path: str) -> str:
    """날짜 → Reading Log 파일 경로 (디렉토리 자동 생성)"""
    log_dir = Path(vault_path) / "Reading Log"
    log_dir.mkdir(parents=True, exist_ok=True)
    return str(log_dir / f"{date}.md")


def append_to_reading_log(entry: dict, date: str, vault_path: str) -> None:
    """
    Reading Log에 논문 항목 추가

    Args:
        entry: {title, note_path, tags, apa_citation}
        date: YYYY-MM-DD 날짜 문자열
        vault_path: Obsidian Vault 경로
    """
    log_path = Path(get_log_path(date, vault_path))

    title = entry.get("title", "")
    note_path = entry.get("note_path", "")
    tags = entry.get("tags", [])

    # 위키링크용 경로: .md 확장자 제거
    wiki_path = note_path.replace("\\", "/").removesuffix(".md")
    tags_str = ", ".join(tags) if tags else ""

    new_item = f"\n- [[{wiki_path}]] — {title} — {tags_str}\n"

    if not log_path.exists():
        # 새 파일: 헤더 + 항목
        log_path.write_text(
            f"# Reading Log — {date}\n{new_item}",
            encoding="utf-8"
        )
    else:
        existing = log_path.read_text(encoding="utf-8")
        # 헤더 중복 방지: 헤더 없으면 추가
        if f"# Reading Log — {date}" not in existing:
            log_path.write_text(
                f"# Reading Log — {date}\n{existing}{new_item}",
                encoding="utf-8"
            )
        else:
            log_path.write_text(existing + new_item, encoding="utf-8")
