import pytest
import allure
import time


@allure.feature("홈")
@allure.story("홈 화면 로딩")
def test_home_page_loaded(home_page):
    """앱 실행 후 홈 화면 로딩 확인"""

    with allure.step("홈 화면 로딩 확인"):
        assert home_page.home_page_is_visible(), "홈 화면이 로드되지 않음"
        home_page.take_screenshot("home_page_loaded")


@allure.feature("홈")
@allure.story("홈 화면 스크롤")
def test_home_page_scroll(home_page):
    """홈 화면 스크롤 테스트"""

    with allure.step("홈 화면 확인"):
        assert home_page.home_page_is_visible(), "홈 화면이 보이지 않음"
        home_page.take_screenshot("home_scroll_01_top")

    with allure.step("아래로 스와이프 (1회)"):
        home_page.swipe_up()
        time.sleep(1)
        home_page.take_screenshot("home_scroll_02_after_swipe1")

    with allure.step("아래로 스와이프 (2회)"):
        home_page.swipe_up()
        time.sleep(1)
        home_page.take_screenshot("home_scroll_03_after_swipe2")

    with allure.step("위로 스와이프 (복귀)"):
        home_page.swipe_down()
        home_page.swipe_down()
        time.sleep(1)
        home_page.take_screenshot("home_scroll_04_back_to_top")

