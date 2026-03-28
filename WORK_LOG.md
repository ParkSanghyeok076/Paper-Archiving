# Work Log — Paper Archiving System

## 프로젝트 개요
HR/AI 대학원 연구자를 위한 논문 관리 시스템.
DOI/URL 입력 → CrossRef API → APA 7판 인용 자동 생성 → Obsidian 노트 저장 → Graph View 연결

**Vault 경로**: `C:\Users\User\Documents\Obsidian Vault`
**프로젝트 경로**: `C:\Users\User\Desktop\Claude\paper-archiving`
**GitHub**: https://github.com/ParkSanghyeok076/Paper-Archiving

---

## 구현 현황

### [완료] Step 1 — CrossRef API + APA 7판 생성
- `src/fetch_metadata.py`: DOI → CrossRef API 호출, 메타데이터 파싱, JATS XML 태그 제거
- `src/generate_apa.py`: APA 7판 저자 포맷 (1~20명 전체, 21명+ 생략 규칙)
- `tests/test_fetch_metadata.py`: 15개 테스트
- `tests/test_generate_apa.py`: 9개 테스트

### [완료] Step 2 — Obsidian Vault 구조 + 노트 생성
- `src/create_note.py`: 메타데이터 → Obsidian 마크다운 노트 (YAML frontmatter, APA 섹션, Topics 위키링크)
- `src/setup_vault.py`: Vault 폴더 구조 초기화, 기본 Topics 허브 노트 생성
- `config.py`: Vault 경로 및 폴더 설정
- `tests/test_create_note.py`: 16개 테스트
- Obsidian Vault에 `Topics/HR Analytics.md`, `Topics/AI in HRM.md`, `_MOC/Research MOC.md` 생성됨

**전체 테스트**: 40/40 통과

---

## 다음 작업 (Step 3~7)

### [대기] Step 3 — 통합 CLI `add_paper.py`
DOI/URL 입력 한 번으로 전체 파이프라인 실행:
```
python add_paper.py --doi "10.xxxx/xxxxx"
```
- `fetch_metadata.py` → `generate_apa.py` → `create_note.py` 연결
- Obsidian vault에 노트 파일 직접 저장

### [대기] Step 4 — Reading Log 자동 업데이트
논문 추가 시 `Reading Log/{date}.md`에 자동 항목 추가

### [대기] Step 5 — Topics 허브 노트 자동 연결
새 태그 입력 시 `Topics/{tag}.md` 없으면 자동 생성

### [대기] Step 6 — PDF 메타데이터 추출 (선택)
PDF 파일에서 DOI 추출 후 Step 3 파이프라인 연결

### [대기] Step 7 — Zotero .bib 연동 (선택)

---

## 실행 방법

```bash
# 의존성 설치
pip install pytest pytest-mock requests

# 테스트 실행
cd paper-archiving
python -m pytest tests/ -v

# Vault 구조 초기화 (최초 1회)
PYTHONPATH="." python src/setup_vault.py
```
