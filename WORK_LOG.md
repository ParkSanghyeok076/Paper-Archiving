# Work Log — Paper Archiving System

## 프로젝트 개요
HR/AI 대학원 연구자를 위한 논문 관리 시스템.
DOI/URL 입력 → CrossRef API → APA 7판 인용 자동 생성 → Obsidian 노트 저장 → Graph View 연결

**Vault 경로**: `C:\Users\User\Documents\Obsidian Vault`
**프로젝트 경로**: `C:\Users\User\Desktop\Claude\paper-archiving`
**GitHub**: https://github.com/ParkSanghyeok076/Paper-Archiving

---

## 실행 방법

```bash
# 의존성 설치 (최초 1회)
pip install pytest pytest-mock requests anthropic

# Vault 구조 초기화 (최초 1회)
cd paper-archiving
PYTHONPATH="." python src/setup_vault.py

# 논문 추가
PYTHONPATH="." python src/add_paper.py --doi "10.xxxx/xxxxx" --tags "HR Analytics" "AI"

# 논문 노트 자동 요약 (API 키 필요)
export ANTHROPIC_API_KEY="sk-ant-..."
PYTHONPATH="." python src/fill_note.py "C:/Users/User/Documents/Obsidian Vault/Papers/노트이름.md"

# 테스트 실행
python -m pytest tests/ -v
```

---

## 구현 현황

### [완료] Step 1 — CrossRef API + APA 7판 생성
- `src/fetch_metadata.py`: DOI → CrossRef API 호출, JATS XML 태그 제거
- `src/generate_apa.py`: APA 7판 저자 포맷 (1~20명 전체, 21명+ 생략 규칙)

### [완료] Step 2 — Obsidian Vault 구조 + 노트 생성
- `src/create_note.py`: 메타데이터 → Obsidian 마크다운 노트
- `src/setup_vault.py`: Vault 폴더 구조 초기화
- `config.py`: Vault 경로 설정
- **노트 템플릿**: 핵심 주장 / 이론적 배경 / 연구 방법 표 / 주요 결과 / 한계점 / 내 연구와의 연결

### [완료] Step 3 — 통합 CLI `add_paper.py`
- DOI → 전체 파이프라인 one-shot 실행

### [완료] Step 4 — Reading Log 자동 업데이트
- `src/reading_log.py`: `Reading Log/{date}.md`에 항목 자동 추가 (Vault 기준 상대 경로)

### [완료] Step 5 — Topics 허브 노트 자동 생성
- `src/topics.py`: 새 태그 → `Topics/{tag}.md` 자동 생성

### [완료] Step 6 — Claude API 자동 요약
- `src/fill_note.py`: Claude Haiku로 빈 섹션 자동 채우기
- 완료 후 `status: reading → done` 자동 변경
- **⚠️ 실행 전 `ANTHROPIC_API_KEY` 환경변수 설정 필요**

**전체 테스트**: 74/74 통과

---

## 다음 작업 (선택 사항)

### [대기] Step 7 — PDF 메타데이터 추출
PDF 파일에서 DOI 추출 후 파이프라인 연결
- `pdfplumber` 라이브러리 활용

### [대기] Step 8 — Zotero .bib 연동
Zotero Better BibTeX `.bib` 파일 파싱 후 파이프라인 연결
