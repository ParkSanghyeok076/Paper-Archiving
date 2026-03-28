# 논문 관리 시스템 — 구현 계획

**작성일**: 2026-03-28
**대상**: HR/AI 대학원생 연구자
**핵심 목표**: DOI/PDF → Obsidian 노트 자동 생성, APA 7판 인용, 연구 주제별 Graph 연결

---

## Requirements Summary

| 요구사항 | 우선순위 |
|---------|---------|
| 논문 독서 날짜/내용 기록 | 필수 |
| APA 7판 인용문 자동 생성 | 필수 |
| 서지 정보 구조화 저장 | 필수 |
| 연구 주제별 연결 (Graph View) | 핵심 |
| DOI/URL → 메타데이터 자동 추출 | 핵심 |
| PDF에서 정보 추출 | 선택 |
| Zotero 연동 | 선택 |

---

## Acceptance Criteria

- [ ] DOI 또는 URL 입력 시 30초 내 완성된 Obsidian 노트 생성
- [ ] 생성된 노트에 APA 7판 인용문이 정확하게 포함됨 (저자, 연도, 제목, 저널, 권호, DOI 형식)
- [ ] 모든 논문 노트에 YAML frontmatter로 `read_date`, `tags`, `doi`, `status` 포함
- [ ] Obsidian Graph View에서 같은 태그/주제 노트 간 연결 시각화 가능
- [ ] Claude Code에서 단일 명령으로 전체 워크플로우 실행 가능
- [ ] 연구 주제 허브 노트에서 관련 논문 목록 자동 역링크 확인 가능

---

## 시스템 아키텍처

```
DOI/URL 입력
    │
    ▼
CrossRef API (메타데이터 추출)
    │
    ▼
APA 7판 인용문 생성 (Python 스크립트)
    │
    ▼
Obsidian MCP → Vault에 노트 생성
    │
    ├── /Papers/{year}/{slug}.md   ← 논문 노트
    ├── /Topics/{topic}.md         ← 주제 허브 (자동 업데이트)
    └── /Reading Log/{date}.md     ← 날짜별 독서 기록
```

---

## Implementation Steps

### Step 1: Obsidian Vault 구조 설계

**파일**: Obsidian Vault 내 폴더 생성 (Obsidian MCP로)

```
📁 Research Vault/
├── 📁 Papers/
│   ├── 📁 2024/
│   └── 📁 2025/
├── 📁 Topics/          ← 연구 주제 허브 노트
├── 📁 Authors/         ← 저자 노트 (선택)
├── 📁 Reading Log/     ← 날짜별 독서 기록
├── 📁 Templates/       ← Obsidian 템플릿
└── 📁 _MOC/            ← Map of Content (주제 지도)
```

**논문 노트 템플릿** (`Templates/paper-template.md`):
```markdown
---
title: "{{title}}"
authors: [{{authors}}]
year: {{year}}
journal: "{{journal}}"
volume: {{volume}}
issue: {{issue}}
pages: "{{pages}}"
doi: "{{doi}}"
url: "{{url}}"
read_date: {{read_date}}
tags: [{{tags}}]
status: reading  # reading | done | revisit
relevance: medium  # low | medium | high
---

# {{title}}

## APA Citation
{{apa_citation}}

## Abstract Summary
> {{abstract}}

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
- [[Topics/]]
```

---

### Step 2: Claude Code 자동화 스크립트 구축

**파일**: `C:/Users/User/Desktop/Claude/paper-manager/`

#### 2a. `fetch_metadata.py` — CrossRef API로 서지 정보 추출
```python
# 입력: DOI 또는 URL
# 출력: JSON 메타데이터 (title, authors, year, journal, volume, issue, pages, abstract, doi)
# API: https://api.crossref.org/works/{doi}
```

#### 2b. `generate_apa.py` — APA 7판 인용문 생성
```python
# APA 7판 규칙:
# 저자(성, 이름이니셜). (연도). 제목. 저널명, 권(호), 시작페이지-끝페이지. https://doi.org/xxx
# 저자 3명 이하: 모두 표기
# 저자 20명 이하: 모두 표기 후 마지막에 & 추가
# 저자 21명 이상: 19명 후 ... 마지막 저자
```

#### 2c. `create_note.py` — Obsidian MCP로 노트 생성
```python
# 템플릿에 메타데이터 채워서 Obsidian vault에 노트 생성
# 파일명: {year}-{first_author_lastname}-{title_slug}.md
# 경로: Papers/{year}/
```

#### 2d. `add_paper.py` — 메인 진입점 (통합 CLI)
```bash
# 사용법:
python add_paper.py --doi "10.xxxx/xxxxx"
python add_paper.py --url "https://journals.example.com/..."
python add_paper.py --pdf "path/to/paper.pdf"
```

---

### Step 3: Obsidian MCP 설정

**설정 파일**: `~/.claude/settings.json`에 Obsidian MCP 추가

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "mcp-obsidian", "--vault-path", "C:/Users/User/path/to/vault"]
    }
  }
}
```

Obsidian MCP가 제공하는 기능:
- `obsidian_create_note`: 노트 생성
- `obsidian_read_note`: 노트 읽기
- `obsidian_search`: 노트 검색
- `obsidian_update_note`: 노트 업데이트

---

### Step 4: Topics 허브 노트 자동 연결

**개념**: Obsidian의 `[[wikilink]]` + 태그 시스템 활용

논문 노트에서:
```markdown
## Related Topics
- [[Topics/HR Analytics]]
- [[Topics/AI in HRM]]
- [[Topics/Turnover Prediction]]
```

Topics 허브 노트 (`Topics/HR Analytics.md`):
```markdown
# HR Analytics

## 관련 논문
<!-- Obsidian이 backlink를 자동으로 Graph View에 표시 -->

## 핵심 키워드
- ...

## 내 연구와의 연결
- ...
```

Graph View에서 Topics 노트가 허브가 되어 관련 논문들이 클러스터 형성.

---

### Step 5: Reading Log 자동 기록

논문 추가 시 해당 날짜의 Reading Log 자동 업데이트:
```markdown
# Reading Log — 2026-03-28

## 오늘 읽은 논문
1. [[Papers/2024/2024-Kim-turnover-prediction]] — HR Analytics, ML
   - 핵심 인사이트:

## 이번 주 통계
- 읽은 논문: 3편
- 주요 주제: HR Analytics (2), NLP (1)
```

---

### Step 6: Zotero 선택적 연동

Zotero Better BibTeX 플러그인으로 `.bib` 파일 자동 내보내기 → `add_paper.py`에서 로컬 `.bib` 파일도 입력 소스로 사용 가능.

---

## Risks and Mitigations

| 리스크 | 완화 방법 |
|--------|----------|
| CrossRef API에 없는 논문 (학회 발표, 프리프린트) | 수동 입력 폼 제공, arXiv API 추가 지원 |
| PDF에서 메타데이터 추출 부정확 | DOI 우선, PDF는 보조 수단으로 사용 |
| Obsidian MCP 버전 호환성 | 설치 시 버전 고정, README에 명시 |
| APA 규칙 예외 케이스 (편집본, 번역서 등) | 생성된 인용문 수동 검토 단계 안내 |

---

## Verification Steps

1. `python add_paper.py --doi "10.1037/0003-066X.59.1.29"` 실행 → Obsidian에 노트 생성 확인
2. 생성된 APA 인용문을 [APA Style 공식 사이트](https://apastyle.apa.org/)와 대조 검증
3. Obsidian Graph View에서 같은 `[[Topics/...]]` 를 가진 논문 노트 간 연결선 확인
4. Reading Log에 오늘 날짜로 항목 추가되었는지 확인
5. 3편 이상 논문 추가 후 주제 클러스터 형성 확인

---

## 구현 순서 (우선순위)

| 단계 | 내용 | 예상 복잡도 |
|------|------|-----------|
| 1 | CrossRef API 연동 + APA 생성 스크립트 | 낮음 |
| 2 | Obsidian Vault 폴더 구조 + 템플릿 생성 | 낮음 |
| 3 | Obsidian MCP 설정 + 노트 자동 생성 | 중간 |
| 4 | Reading Log 자동 업데이트 | 낮음 |
| 5 | Topics 허브 노트 자동 연결 | 중간 |
| 6 | PDF 메타데이터 추출 (선택) | 높음 |
| 7 | Zotero .bib 연동 (선택) | 중간 |
