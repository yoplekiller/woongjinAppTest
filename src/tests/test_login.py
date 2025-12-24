import allure
import time


def test_login(home_page, login_page, test_user_credentials):
    """웅진마켓 로그인 테스트"""
    user_id = test_user_credentials["user_id"]
    password = test_user_credentials["password"]

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
        time.sleep(5)  # 로그인 처리 대기
        take_screenshot = home_page.take_screenshot("woongjin_logged_in_home_page.png")
        print("✅ 이메일 로그인 수행 완료")