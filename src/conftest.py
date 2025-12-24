"""
pytest conftest.py - 테스트 픽스처 및 설정
"""
from typing import Generator
import pytest
from appium import webdriver
from appium.webdriver.webdriver import WebDriver
from appium.options.android import UiAutomator2Options
from pages.woongjin_app_home_page import WoongjinAppHomePage
from pages.woongjin_app_search_page import WoongjinAppSearchPage
from pages.woongjin_app_category_page import WoongjinAppCategoryPage
from pages.woongjin_app_like_page import WoongjinAppLikePage
from pages.woongjin_app_login_page import WoongjinAppLoginPage
from config.app_config import AppConfig
from src.pages.woongjin_app_my_tab import WoongjinAppMyTabPage
from utils.popup_handler import handle_woongjin_popups
from utils.page_source_helper import save_page_source, print_all_elements
from utils.logger import get_logger
from datetime import datetime
import os
from dotenv import load_dotenv

logger = get_logger(__name__)
load_dotenv()


@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    """웅진마켓 앱 드라이버"""
    # 설정에서 capabilities 가져오기
    caps = AppConfig.get_capabilities("woongjin")
    options = UiAutomator2Options().load_capabilities(caps)

    # Appium 드라이버 생성
    driver = webdriver.Remote(AppConfig.APPIUM_SERVER_URL, options=options)

    # 초기 팝업 처리
    handle_woongjin_popups(driver, wait_time=AppConfig.POPUP_WAIT)

    yield driver

    # 테스트 종료 후 드라이버 종료
    driver.quit()


@pytest.fixture(scope="function")
def home_page(driver: WebDriver) -> WoongjinAppHomePage:
    """웅진마켓 홈페이지 Page Object"""
    return WoongjinAppHomePage(driver)

@pytest.fixture(scope="function")
def search_page(driver: WebDriver) -> WoongjinAppSearchPage:
    """웅진마켓 검색 페이지 Page Object"""
    return WoongjinAppSearchPage(driver)

@pytest.fixture(scope="function")
def category_page(driver: WebDriver) -> WoongjinAppCategoryPage:
    """웅진마켓 카테고리 페이지 Page Object"""
    return WoongjinAppCategoryPage(driver)

@pytest.fixture(scope="function")
def like_page(driver: WebDriver) -> WoongjinAppLikePage:
    """웅진마켓 찜 페이지 Page Object"""
    return WoongjinAppLikePage(driver)

@pytest.fixture(scope="function")
def my_tab_page(driver: WebDriver) -> WoongjinAppMyTabPage:
    """웅진마켓 마이탭 페이지 Page Object"""
    return WoongjinAppMyTabPage(driver)

@pytest.fixture(scope="function")
def login_page(driver: WebDriver) -> WoongjinAppLoginPage:
    """웅진마켓 로그인 페이지 Page Object"""
    return WoongjinAppLoginPage(driver)

@pytest.fixture(scope="function")
def test_user_credentials() -> dict:
    """테스트 사용자 자격 증명"""
    return {
        "user_id": os.getenv("TEST_USER_ID"),
        "password": os.getenv("TEST_USER_PASSWORD")
    }

@pytest.fixture(scope="function")
def wrong_user_credentials() -> dict:
    """잘못된 테스트 사용자 자격 증명"""
    return {
        "user_id": os.getenv("WRONG_TEST_USER_ID"),
        "password": os.getenv("WRONG_TEST_USER_PASSWORD")
    }
    
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment() -> Generator[None, None, None]:
    """테스트 환경 초기 설정"""
    # 필요한 디렉토리 생성
    AppConfig.ensure_directories()
    logger.info("=" * 80)
    logger.info("테스트 환경 설정 완료")
    logger.info("=" * 80)
    yield
    logger.info("테스트 환경 정리 완료")


# === 실패 시 자동 캡처 ===
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    테스트 실패 시 자동으로 스크린샷 + 페이지 소스 저장
    실무 필수 기능
    """
    outcome = yield
    rep = outcome.get_result()

    # 테스트 실패 시에만 실행
    if rep.when == "call" and rep.failed:
        # driver fixture가 있는지 확인
        if "driver" in item.funcargs:
            driver = item.funcargs["driver"]

            try:
                # 타임스탬프
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.nodeid.replace("::", "_").replace("/", "_")

                # 스크린샷 저장
                screenshot_dir = AppConfig.SCREENSHOT_DIR
                os.makedirs(screenshot_dir, exist_ok=True)

                screenshot_path = f"{screenshot_dir}/FAILED_{test_name}_{timestamp}.png"
                driver.get_screenshot_as_file(screenshot_path)
                logger.error(f"📸 실패 스크린샷 저장: {screenshot_path}")

                # 페이지 소스 저장
                page_source_dir = AppConfig.PAGE_SOURCE_DIR
                os.makedirs(page_source_dir, exist_ok=True)

                source_path = f"{page_source_dir}/FAILED_{test_name}_{timestamp}.xml"
                with open(source_path, 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                logger.error(f"📄 실패 페이지 소스 저장: {source_path}")

                # 현재 액티비티 정보
                current_activity = driver.current_activity
                current_package = driver.current_package
                logger.error(f"📱 현재 화면: {current_package}/{current_activity}")

            except Exception as e:
                logger.error(f"실패 캡처 중 에러: {e}")


# === 실패 시 자동 캡처 ===
def pytest_configure(config):
    """pytest 설정 - 재시도 마커 등록"""
    config.addinivalue_line(
        "markers",
        "flaky(reruns=3): 불안정한 테스트, 실패 시 재시도"
    )