"""
GNB 네비게이션 통합 테스트
"""
import pytest
import allure
import time


@allure.feature("네비게이션")
@allure.story("전체 GNB 탭 순회")
def test_gnb_full_navigation(home_page, category_page, search_page):
    """홈 → 카테고리 → 검색 → 홈 순회 테스트"""

    with allure.step("1. 홈 페이지 확인"):
        assert home_page.home_page_is_visible(), "홈 페이지가 보이지 않음"
        home_page.take_screenshot("nav_01_home")

    with allure.step("2. 카테고리 탭 이동"):
        home_page.click_category_tab()
        time.sleep(1)
        assert category_page.is_category_page_visible(), "카테고리 페이지가 보이지 않음"
        category_page.take_screenshot("nav_02_category")

    with allure.step("3. 검색 탭 이동"):
        home_page.click_search_tab()
        time.sleep(1)
        assert search_page.search_page_is_visible(), "검색 페이지가 보이지 않음"
        search_page.take_screenshot("nav_03_search")

    with allure.step("4. 홈 탭 복귀"):
        home_page.click_home_tab()
        time.sleep(1)
        assert home_page.home_page_is_visible(), "홈 페이지로 복귀하지 않음"
        home_page.take_screenshot("nav_04_home_return")


@allure.feature("네비게이션")
@allure.story("탭 연속 클릭")
def test_rapid_tab_switching(home_page, category_page, search_page):
    """빠른 탭 전환 안정성 테스트"""

    with allure.step("홈 페이지 시작"):
        assert home_page.home_page_is_visible(), "홈 페이지가 보이지 않음"

    with allure.step("빠른 탭 전환 (3회)"):
        for i in range(3):
            home_page.click_category_tab()
            time.sleep(0.5)
            home_page.click_search_tab()
            time.sleep(0.5)
            home_page.click_home_tab()
            time.sleep(0.5)

    with allure.step("최종 홈 페이지 확인"):
        assert home_page.home_page_is_visible(), "빠른 탭 전환 후 홈 페이지가 보이지 않음"
        home_page.take_screenshot("rapid_tab_switching_complete")
