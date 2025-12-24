import allure
import time



def test_login_wrong_password(login_page, home_page, test_user_credentials, wrong_user_credentials):
    """로그인 - 잘못된 비밀번호 입력 시 오류 메시지 확인"""
    valid_user = test_user_credentials["user_id"]
    wrong_password = wrong_user_credentials["password"]

    
    with allure.step("로그인 페이지 열기"):
        home_page.click_like_tab()
        assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"
        print("✅ 로그인 페이지 노출 확인")

    with allure.step("이메일 로그인 페이지로 이동"):
        login_page.click_email_login()
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"
        print("✅ 이메일 로그인 페이지 노출 확인")

    with allure.step("잘못된 비밀번호로 로그인 시도"):
        login_page.email_login(valid_user, wrong_password)
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"
        print("✅ 잘못된 비밀번호로 로그인 시도 완료")
        

    with allure.step("오류 메시지 확인"):
        get_error_message = login_page.get_error_message()
        assert "일치하는 계정 정보가 없습니다." in get_error_message, f"예상 오류 메시지와 다름: {get_error_message}"    
    
    with allure.step("오류 팝업 닫기"):
        login_page.close_error_popup()
        print("✅ 잘못된 비밀번호 오류 메시지 확인 완료")

def test_login_invalid_account(login_page, home_page, wrong_user_credentials, test_user_credentials):  
    """로그인 - 존재하지 않는 계정 입력 시 오류 메시지 확인"""
    invalid_user = wrong_user_credentials["user_id"]
    valid_password = test_user_credentials["password"]

    with allure.step("로그인 페이지 열기"):
        home_page.click_like_tab()
        assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"
        print("✅ 로그인 페이지 노출 확인")

    with allure.step("이메일 로그인 페이지로 이동"):
        login_page.click_email_login()
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"
        print("✅ 이메일 로그인 페이지 노출 확인")

    with allure.step("존재하지 않는 계정으로 로그인 시도"):
        login_page.email_login(invalid_user, valid_password)
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"
        print("✅ 존재하지 않는 계정으로 로그인 시도 완료")
        time.sleep(2)

    with allure.step("오류 메시지 확인"):
        get_error_message = login_page.get_error_message()
        assert  "일치하는 계정 정보가 없습니다" in get_error_message, f"예상 오류 메시지와 다름: {get_error_message}"

    with allure.step("오류 팝업 닫기"):
        login_page.close_error_popup()
        print("✅ 존재하지 않는 계정 오류 메시지 확인 완료")


def test_login_empty_fields(login_page, home_page):  
    """로그인 - 빈 입력 필드로 로그인 시도 시 오류 메시지 확인"""

    with allure.step("로그인 페이지 열기"):
        home_page.click_like_tab()
        assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"
        print("✅ 로그인 페이지 노출 확인")

    with allure.step("이메일 로그인 페이지로 이동"):
        login_page.click_email_login()
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"
        print("✅ 이메일 로그인 페이지 노출 확인")

    with allure.step("빈 입력 필드로 로그인 시도"):
        login_page.email_login("", "")
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"
        print("✅ 빈 입력 필드로 로그인 시도 완료")

    with allure.step("오류 메시지 확인"):
        get_error_message = login_page.get_error_message()
        assert  "일치하는 계정 정보가 없습니다" in get_error_message, f"예상 오류 메시지와 다름: {get_error_message}"

    with allure.step("오류 팝업 닫기"):
        login_page.close_error_popup()
        print("✅ 빈 입력 필드 오류 메시지 확인 완료")   