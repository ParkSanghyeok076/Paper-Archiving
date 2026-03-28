"""
TDD: APA 7판 인용문 생성 테스트
테스트를 먼저 작성하고 구현은 이후에 진행합니다.
"""
import pytest
from src.generate_apa import generate_apa_citation


# --- 저자 포맷 케이스 ---

def test_single_author():
    """저자 1명: Last, F. M. (year). Title. Journal, vol(issue), pages. https://doi.org/xxx"""
    metadata = {
        "authors": [{"family": "Smith", "given": "John A."}],
        "year": 2020,
        "title": "The impact of AI on HR practices",
        "journal": "Journal of Applied Psychology",
        "volume": "105",
        "issue": "3",
        "pages": "300-320",
        "doi": "10.1037/apl0000123",
    }
    result = generate_apa_citation(metadata)
    assert result == (
        "Smith, J. A. (2020). The impact of AI on HR practices. "
        "Journal of Applied Psychology, 105(3), 300-320. "
        "https://doi.org/10.1037/apl0000123"
    )


def test_two_authors():
    """저자 2명: Author1 & Author2"""
    metadata = {
        "authors": [
            {"family": "Smith", "given": "John A."},
            {"family": "Jones", "given": "Beth"},
        ],
        "year": 2021,
        "title": "Machine learning in talent acquisition",
        "journal": "Human Resource Management",
        "volume": "60",
        "issue": "1",
        "pages": "45-60",
        "doi": "10.1002/hrm.22001",
    }
    result = generate_apa_citation(metadata)
    assert result == (
        "Smith, J. A., & Jones, B. (2021). Machine learning in talent acquisition. "
        "Human Resource Management, 60(1), 45-60. "
        "https://doi.org/10.1002/hrm.22001"
    )


def test_three_authors():
    """저자 3명: Author1, Author2, & Author3"""
    metadata = {
        "authors": [
            {"family": "Kim", "given": "Sanghyeok"},
            {"family": "Park", "given": "Jiyeon"},
            {"family": "Lee", "given": "Minjun"},
        ],
        "year": 2023,
        "title": "Predictive analytics for employee turnover",
        "journal": "Journal of Organizational Behavior",
        "volume": "44",
        "issue": "2",
        "pages": "123-145",
        "doi": "10.1002/job.2701",
    }
    result = generate_apa_citation(metadata)
    assert result == (
        "Kim, S., Park, J., & Lee, M. (2023). Predictive analytics for employee turnover. "
        "Journal of Organizational Behavior, 44(2), 123-145. "
        "https://doi.org/10.1002/job.2701"
    )


def test_twenty_authors():
    """저자 20명: 모두 표기, 마지막 앞에 &"""
    authors = [{"family": f"Author{i}", "given": f"Name{i}"} for i in range(1, 21)]
    metadata = {
        "authors": authors,
        "year": 2022,
        "title": "Large collaboration study",
        "journal": "Nature Human Behaviour",
        "volume": "6",
        "issue": "4",
        "pages": "500-510",
        "doi": "10.1038/s41562-022-01234-5",
    }
    result = generate_apa_citation(metadata)
    # 20명 모두 표기
    assert "Author20, N." in result
    assert "..." not in result
    # & 는 마지막 저자 앞에만
    assert result.count("&") == 1
    assert "& Author20, N." in result


def test_twentyone_authors():
    """저자 21명 이상: 처음 19명, ..., 마지막 저자"""
    authors = [{"family": f"Author{i}", "given": f"Name{i}"} for i in range(1, 23)]
    metadata = {
        "authors": authors,
        "year": 2022,
        "title": "Very large collaboration",
        "journal": "Science",
        "volume": "375",
        "issue": "6580",
        "pages": "100-110",
        "doi": "10.1126/science.abc1234",
    }
    result = generate_apa_citation(metadata)
    # 19번째 저자까지 포함
    assert "Author19, N." in result
    # 20번째 저자는 제외
    assert "Author20, N." not in result
    # 생략 기호 포함
    assert "..." in result
    # 마지막 저자 포함
    assert "Author22, N." in result


# --- 선택적 필드 케이스 ---

def test_no_issue_number():
    """호(issue)가 없는 경우: Journal, vol, pages 형식"""
    metadata = {
        "authors": [{"family": "Brown", "given": "Carol D."}],
        "year": 2019,
        "title": "Organizational learning and AI",
        "journal": "Academy of Management Review",
        "volume": "44",
        "issue": None,
        "pages": "210-230",
        "doi": "10.5465/amr.2019.0123",
    }
    result = generate_apa_citation(metadata)
    assert "Academy of Management Review, 44, 210-230" in result
    assert "(None)" not in result


def test_no_pages():
    """페이지 정보 없는 경우 (온라인 선행 출판 등)"""
    metadata = {
        "authors": [{"family": "Chen", "given": "Wei"}],
        "year": 2024,
        "title": "AI ethics in HRM",
        "journal": "Human Resource Management Review",
        "volume": "34",
        "issue": "1",
        "pages": None,
        "doi": "10.1016/j.hrmr.2024.100990",
    }
    result = generate_apa_citation(metadata)
    assert "Human Resource Management Review, 34(1)." in result
    assert "None" not in result


def test_doi_url_format():
    """DOI는 항상 https://doi.org/ 형식으로"""
    metadata = {
        "authors": [{"family": "Taylor", "given": "Emma R."}],
        "year": 2020,
        "title": "Remote work and performance",
        "journal": "Work and Stress",
        "volume": "34",
        "issue": "3",
        "pages": "280-295",
        "doi": "10.1080/02678373.2020.1776782",
    }
    result = generate_apa_citation(metadata)
    assert result.endswith("https://doi.org/10.1080/02678373.2020.1776782")


def test_title_not_italicized():
    """APA 7판: 논문 제목은 이탤릭 없음, 저널명은 이탤릭 (텍스트 기준 검증)"""
    metadata = {
        "authors": [{"family": "Lee", "given": "Soo Hyun"}],
        "year": 2021,
        "title": "HR analytics adoption",
        "journal": "International Journal of Human Resource Management",
        "volume": "32",
        "issue": "5",
        "pages": "1000-1020",
        "doi": "10.1080/09585192.2021.1234567",
    }
    result = generate_apa_citation(metadata)
    # 제목이 인용문 안에 정확히 포함됨
    assert "HR analytics adoption" in result
