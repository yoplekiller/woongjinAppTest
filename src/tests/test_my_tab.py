"""
마이탭 페이지 테스트
"""
import pytest
import allure
import time


@allure.feature("마이탭")
@allure.story("마이탭 페이지 진입 (비로그인)")
def test_my_tab_requires_login(home_page, login_page):
    """비로그인 상태에서 마이탭 클릭 시 로그인 페이지 노출"""

    with allure.step("홈 페이지 확인"):
        assert home_page.home_page_is_visible(), "홈 페이지가 보이지 않음"

    with allure.step("마이탭 클릭"):
        home_page.click_my_page_tab()
        time.sleep(1)

    with allure.step("로그인 페이지 노출 확인"):
        assert login_page.is_login_page_visible(), "로그인 페이지가 보이지 않음"
        login_page.take_screenshot("my_tab_login_required")


@allure.feature("마이탭")
@allure.story("마이탭 페이지 진입 (로그인)")
def test_my_tab_after_login(home_page, login_page, my_tab_page, test_user_credentials):
    """로그인 후 마이탭 페이지 진입 테스트"""

    user_id = test_user_credentials["user_id"]
    password = test_user_credentials["password"]

    with allure.step("마이탭 클릭 → 로그인 페이지"):
        home_page.click_my_page_tab()
        time.sleep(1)
        assert login_page.is_login_page_visible(), "로그인 페이지가 보이지 않음"

    with allure.step("이메일 로그인 수행"):
        login_page.click_email_login()
        login_page.email_login(user_id, password)
        time.sleep(3)

    with allure.step("마이탭 페이지 확인"):
        assert my_tab_page.is_my_tab_page_visible(), "마이탭 페이지가 보이지 않음"
        my_tab_page.take_screenshot("my_tab_page_logged_in")
