import allure


def test_login_wrong_password(navigate_to_email_login, test_user_credentials, wrong_user_credentials):
    """로그인 - 잘못된 비밀번호 입력 시 오류 메시지 확인"""
    email_login_page = navigate_to_email_login
    valid_user = test_user_credentials["user_id"]
    wrong_password = wrong_user_credentials["password"]

    with allure.step("잘못된 비밀번호로 로그인 시도"):
        email_login_page.email_login(valid_user, wrong_password)
        assert email_login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"

    with allure.step("오류 메시지 확인 및 팝업 닫기"):
        assert "일치하는 계정 정보가 없습니다." in email_login_page.get_error_message()
        email_login_page.close_error_popup()
        print("✅ 잘못된 비밀번호 오류 메시지 확인 완료")


def test_login_invalid_account(navigate_to_email_login, wrong_user_credentials, test_user_credentials):
    """로그인 - 존재하지 않는 계정 입력 시 오류 메시지 확인"""
    email_login_page = navigate_to_email_login
    invalid_user = wrong_user_credentials["user_id"]
    valid_password = test_user_credentials["password"]

    with allure.step("존재하지 않는 계정으로 로그인 시도"):
        email_login_page.email_login(invalid_user, valid_password)
        assert email_login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"

    with allure.step("오류 메시지 확인 및 팝업 닫기"):
        assert "일치하는 계정 정보가 없습니다" in email_login_page.get_error_message()
        email_login_page.close_error_popup()
        print("✅ 존재하지 않는 계정 오류 메시지 확인 완료")


def test_login_empty_fields(navigate_to_email_login):
    """로그인 - 빈 입력 필드로 로그인 시도 시 오류 메시지 확인"""
    email_login_page = navigate_to_email_login

    with allure.step("빈 입력 필드로 로그인 시도"):
        email_login_page.email_login("", "")
        assert email_login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"
    with allure.step("오류 메시지 확인 및 팝업 닫기"):
        assert "일치하는 계정 정보가 없습니다" in email_login_page.get_error_message()
        email_login_page.close_error_popup()
        print("✅ 빈 입력 필드 오류 메시지 확인 완료")
