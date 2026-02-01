import pytest
import allure
from selenium.webdriver.support.ui import WebDriverWait
import time

from src.conftest import login_page


def test_category_tab(home_page, category_page):

    """웅진마켓 카테고리 테스트"""

    with allure.step("카테고리 탭 클릭"):
        home_page.click_category_tab()
        print("📂 카테고리 탭 클릭 완료")

    with allure.step("카테고리 페이지 로딩 검증"):
        assert category_page.is_category_page_visible(), "❌ 카테고리 페이지가 로드되지 않음"
        take_screenshot = category_page.take_screenshot("woongjin_category_page.png") 
        print("✅ 카테고리 페이지 로딩 검증 완료") 


def test_search_tab(home_page, search_page):
    """웅진마켓 검색 기능 테스트"""

    with allure.step("검색 버튼 클릭"):
        home_page.click_search_tab()
        print("🔍 검색 탭 클릭 완료")
   
    
    with allure.step("검색 페이지 로딩 검증"):
        assert search_page.search_page_is_visible(), "❌ 검색 페이지가 보이지 않음"
        time.sleep(2)  # 페이지 로딩 대기
        take_screenshot = search_page.take_screenshot("woongjin_search_page.png")
        print("✅ 검색 페이지 로딩 검증 완료")


def test_like_tab(home_page, login_page, like_page, test_user_credentials):
    
    user_id = test_user_credentials["user_id"]
    password = test_user_credentials["password"]

    """웅진마켓 찜 탭 테스트"""
    with allure.step("로그인 페이지로 이동"):
        home_page.click_like_tab()
        assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"
        print("✅ 로그인 페이지 노출 확인")

    with allure.step("로그인 타입 노출 확인"):
        assert login_page.login_types_are_visible(), "❌ 로그인 타입들이 보이지 않음"
        print("✅ 로그인 타입 노출 확인")
    
    with allure.step("이메일 로그인 페이지로 이동"):
        login_page.click_email_login()
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"
        print("✅ 이메일 로그인 페이지 노출 확인")
        

    with allure.step("이메일 로그인 수행"):
        login_page.email_login(user_id, password)
        time.sleep(3)  # 로그인 처리 대기
        take_screenshot = home_page.take_screenshot("woongjin_logged_in_home_page.png")
        print("✅ 이메일 로그인 수행 완료")

    
    with allure.step("찜 페이지 로딩 검증"):
        assert like_page.is_like_page_visible(), "❌ 찜 페이지가 보이지 않음"
        take_screenshot = like_page.take_screenshot("woongjin_like_page.png")
        print("✅ 찜 페이지 로딩 검증 완료")
    






    
    