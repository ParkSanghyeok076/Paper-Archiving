"""
Obsidian Vault 초기 구조 생성
"""
from pathlib import Path
from config import VAULT_PATH, VAULT_DIRS


MOC_CONTENT = """# Research Map of Content

## 연구 주제
- [[Topics/HR Analytics]]
- [[Topics/AI in HRM]]
- [[Topics/Turnover Prediction]]
- [[Topics/NLP]]

## 최근 읽은 논문
<!-- Reading Log 폴더에서 최신 날짜 항목 확인 -->

## 통계
<!-- 전체 논문 수, 주제별 분포 -->
"""

HR_ANALYTICS_TOPIC = """# HR Analytics

## 핵심 개념
- 데이터 기반 HR 의사결정
- 예측 분석 (이직, 성과, 채용)
- HR 메트릭스 및 KPI

## 관련 논문
<!-- Obsidian이 backlink를 자동으로 여기에 연결 -->

## 내 연구와의 연결

"""

AI_HRM_TOPIC = """# AI in HRM

## 핵심 개념
- 채용 자동화 및 AI 스크리닝
- 성과 관리 알고리즘
- AI 편향성 및 공정성

## 관련 논문
<!-- Obsidian이 backlink를 자동으로 여기에 연결 -->

## 내 연구와의 연결

"""


def setup_vault(vault_path: str = VAULT_PATH) -> None:
    """Vault 폴더 구조 및 초기 노트 생성"""
    root = Path(vault_path)

    # 기본 폴더 생성
    for folder in VAULT_DIRS:
        (root / folder).mkdir(parents=True, exist_ok=True)
        print(f"  [OK] {folder}/")

    # 초기 MOC 노트
    moc_path = root / "_MOC" / "Research MOC.md"
    if not moc_path.exists():
        moc_path.write_text(MOC_CONTENT, encoding="utf-8")
        print("  [OK] _MOC/Research MOC.md")

    # 기본 Topics 허브 노트
    topics = {
        "HR Analytics.md": HR_ANALYTICS_TOPIC,
        "AI in HRM.md": AI_HRM_TOPIC,
    }
    for filename, content in topics.items():
        topic_path = root / "Topics" / filename
        if not topic_path.exists():
            topic_path.write_text(content, encoding="utf-8")
            print(f"  [OK] Topics/{filename}")

    print(f"\nVault 초기화 완료: {vault_path}")


if __name__ == "__main__":
    print("Obsidian Vault 구조 생성 중...")
    setup_vault()
