"""
Topics 허브 노트 자동 생성
새 태그 입력 시 Topics/{tag}.md가 없으면 자동 생성
"""
from pathlib import Path


def _build_topic_content(tag: str) -> str:
    return f"""# {tag}

## 핵심 개념


## 관련 논문
<!-- Obsidian이 backlink를 자동으로 여기에 연결 -->

## 내 연구와의 연결

"""


def ensure_topic_notes(tags: list, vault_path: str) -> list:
    """
    태그 목록을 순회하며 Topics 노트가 없으면 생성

    Args:
        tags: 태그 문자열 목록
        vault_path: Obsidian Vault 경로

    Returns:
        새로 생성된 태그 목록
    """
    topics_dir = Path(vault_path) / "Topics"
    topics_dir.mkdir(parents=True, exist_ok=True)

    created = []
    for tag in tags:
        topic_path = topics_dir / f"{tag}.md"
        if not topic_path.exists():
            topic_path.write_text(_build_topic_content(tag), encoding="utf-8")
            created.append(tag)

    return created
