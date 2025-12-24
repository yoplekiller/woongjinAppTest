from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

import re


class WoongjinAppLoginPage(BasePage):
    """웅진마켓 로그인 페이지"""

    # Locators - 모두 클래스 변수로 통일
    LOGIN_PAGE_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[@text='로그인']")
    
    # 소셜 로그인 버튼
    KAKAO_LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.TextView[@text='카카오 로그인']")
    NAVER_LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.TextView[@text='네이버 로그인']")
    EMAIL_LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.TextView[@text='이메일 로그인']")
    
    # 이메일 로그인 요소
    EMAIL_LOGIN_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'이메일 로그인을 해주세요')]")
    ID_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@resource-id='username']")
    PASSWORD_INPUT = (AppiumBy.XPATH, "//android.widget.EditText[@resource-id='password']")
    LOGIN_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@resource-id='emailLoginBtn']")
    INVALID_ACCOUNT_MESSAGE = (AppiumBy.XPATH, "//android.widget.TextView[@text='일치하는 계정 정보가 없습니다.']")
    INVALID_CREDENTIALS_MESSAGE = (AppiumBy.XPATH, "//android.widget.TextView[@text='아이디 또는 비밀번호를 확인해주세요!.']")
    INVALID_POPUP_BTN = (AppiumBy.ID, "alertBtn")


    
    def is_login_page_visible(self) -> bool:
        """로그인 페이지가 보이는지 확인"""
        return self.is_element_visible(self.LOGIN_PAGE_TITLE)
    

    def login_types_are_visible(self) -> bool:
        """로그인 타입들이 보이는지 확인"""
        return (
            self.is_element_visible(self.KAKAO_LOGIN_BUTTON) and 
            self.is_element_visible(self.NAVER_LOGIN_BUTTON) and 
            self.is_element_visible(self.EMAIL_LOGIN_BUTTON)
        )
    
    def click_email_login(self) -> None:
        """이메일 로그인 클릭"""
        self.click(self.EMAIL_LOGIN_BUTTON)
    
    
    def email_login_page_is_visible(self) -> bool:
        """이메일 로그인 페이지 노출 확인"""
        return (
            self.is_element_visible(self.EMAIL_LOGIN_TITLE)
        )
    
    def enter_username(self, username: str) -> None:
        """아이디 입력"""
        self.click(self.ID_INPUT)
        self.input_text(self.ID_INPUT, username)

    def enter_password(self, password: str) -> None:
        """비밀번호 입력"""
        self.click(self.PASSWORD_INPUT)
        self.input_text(self.PASSWORD_INPUT, password)

    def click_login_button(self) -> None:
        """로그인 버튼 클릭"""
        self.click(self.LOGIN_BUTTON)

    def email_login(self, username: str, password: str) -> None:
        """이메일 로그인 수행"""

        # 2. 입력값 검증 (선택)
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', username):
            raise ValueError(f"올바른 이메일 형식이 아닙니다: {username}")
        if len(password) < 8:
            raise ValueError("비밀번호는 최소 8자 이상이어야 합니다")

        # 3. 입력 및 로그인
        self.enter_username(username)
        self.enter_password(password)
        self.driver.hide_keyboard()
        self.click_login_button()

    def get_error_message(self) -> str:
        """오류 메시지 가져오기"""
        if self.is_element_visible(self.INVALID_ACCOUNT_MESSAGE):
            return self.get_element_text(self.INVALID_ACCOUNT_MESSAGE)
        elif self.is_element_visible(self.INVALID_CREDENTIALS_MESSAGE):
            return self.get_element_text(self.INVALID_CREDENTIALS_MESSAGE)
        else:
            return ""
        
    def close_error_popup(self) -> None:
        """오류 팝업 닫기"""
        if self.is_element_clickable(self.INVALID_POPUP_BTN):
            self.click(self.INVALID_POPUP_BTN)