"""
웅진마켓 앱 페이지 소스 추출 및 분석 테스트
"""
import pytest
from utils.page_source_helper import (
    save_page_source,
    print_all_elements,
    print_elements_with_content_desc,
    print_elements_with_text
)


def test_woongjin_extract_source(driver):
    """웅진마켓 앱 소스 정보 추출 테스트"""
    # XML 형식으로 저장
    save_page_source(driver, "woongjin_app_source.xml")

    # 콘솔에 요소 정보 출력
    print("\n=== 화면의 모든 요소 ===")
    print_all_elements(driver)

    print("\n=== Content-desc 요소들 ===")
    print_elements_with_content_desc(driver)

    print("\n=== Text 요소들 ===")
    print_elements_with_text(driver)
