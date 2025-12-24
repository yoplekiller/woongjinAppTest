"""
앱 테스트 설정 관리
"""
from typing import Dict, Any
import os


class AppConfig:
    """앱 테스트 설정"""

    # Appium 서버 설정
    APPIUM_SERVER_URL: str = "http://127.0.0.1:4723"

    # 웅진마켓 앱 설정
    WOONGJIN_APP: Dict[str, str] = {
        "platformName": "Android",
        "deviceName": "R3CX70ALSLB",
        "appPackage": "com.wjthinkbig.woongjinbooks",
        "appActivity": ".view.IntroActivity",
        "automationName": "UiAutomator2",
    }

    # 타임아웃 설정
    DEFAULT_TIMEOUT: int = 10
    LONG_TIMEOUT: int = 30
    SHORT_TIMEOUT: int = 5

    # 대기 시간 설정
    POPUP_WAIT: float = 1.5
    APP_LOADING_WAIT: int = 8
    BANNER_WAIT: int = 10  # 배너 로딩 대기 시간 (하드코딩)

    # 스크린샷 설정
    SCREENSHOT_DIR: str = "./screenshots"

    # 페이지 소스 저장 경로
    PAGE_SOURCE_DIR: str = "./page_sources"

    @staticmethod
    def get_capabilities(app_name: str = "woongjin") -> Dict[str, str]:
        """앱별 capabilities 반환"""
        if app_name == "woongjin":
            return AppConfig.WOONGJIN_APP
        else:
            raise ValueError(f"Unknown app name: {app_name}")

    @staticmethod
    def ensure_directories() -> None:
        """필요한 디렉토리 생성"""
        os.makedirs(AppConfig.SCREENSHOT_DIR, exist_ok=True)
        os.makedirs(AppConfig.PAGE_SOURCE_DIR, exist_ok=True)
