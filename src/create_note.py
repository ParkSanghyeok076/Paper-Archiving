"""
Obsidian 논문 노트 생성
"""
import re
from pathlib import Path


def slugify(title: str, max_length: int = 50) -> str:
    """제목 → URL-safe 슬러그"""
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)   # 특수문자 제거
    slug = re.sub(r"[\s_]+", "-", slug)     # 공백/언더스코어 → 하이픈
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:max_length].rstrip("-")


def get_note_path(metadata: dict, vault_path: str) -> str:
    """메타데이터 → 노트 파일 경로 (디렉토리 자동 생성)"""
    year = metadata.get("year", "unknown")
    authors = metadata.get("authors", [])
    first_family = authors[0]["family"] if authors else "Unknown"
    title = metadata.get("title", "untitled")

    slug = slugify(title)
    filename = f"{year}-{first_family}-{slug}.md"

    note_dir = Path(vault_path) / "Papers"
    note_dir.mkdir(parents=True, exist_ok=True)

    return str(note_dir / filename)


def build_note_content(metadata: dict) -> str:
    """메타데이터 → Obsidian 마크다운 노트 문자열"""
    title = metadata.get("title", "")
    authors = metadata.get("authors", [])
    year = metadata.get("year", "")
    journal = metadata.get("journal", "")
    volume = metadata.get("volume", "")
    issue = metadata.get("issue", "")
    pages = metadata.get("pages", "")
    doi = metadata.get("doi", "")
    abstract = metadata.get("abstract") or ""
    apa_citation = metadata.get("apa_citation", "")
    read_date = metadata.get("read_date", "")
    tags = metadata.get("tags", [])

    # 저자 목록 (YAML)
    authors_yaml = "\n".join(f'  - "{a.get("family")}, {a.get("given")}"' for a in authors)

    # 태그 목록 (YAML)
    tags_yaml = "\n".join(f"  - {t}" for t in tags)

    # Related Topics 위키링크
    topic_links = "\n".join(f"- [[Topics/{t}]]" for t in tags)

    frontmatter = f"""---
title: "{title}"
authors:
{authors_yaml}
year: {year}
journal: "{journal}"
volume: "{volume}"
issue: "{issue}"
pages: "{pages}"
doi: "{doi}"
read_date: {read_date}
tags:
{tags_yaml}
status: reading
relevance: medium
---"""

    body = f"""
# {title}

## APA Citation
{apa_citation}

## Abstract Summary
{abstract}

## Key Findings
-

## Methodology
- **연구 설계**:
- **샘플**:
- **분석 방법**:

## Personal Notes
### 이 논문이 내 연구에 주는 시사점


### 비판적 평가


## Related Papers
- [[]]

## Related Topics
{topic_links}
"""

    return frontmatter + "\n" + body
