"""
BasePage - 모든 페이지 객체의 기본 클래스
"""
from typing import List, Dict, Any, Optional, Tuple, Union
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from config.app_config import AppConfig
from utils.logger import get_logger
import time

logger = get_logger(__name__)

# Locator 타입을 By 또는 AppiumBy 모두 지원하도록 정의
Locator = Tuple[Union[By, AppiumBy], str]

class BasePage:
    """모든 페이지의 기본 클래스"""

    Locators = Locator

    def __init__(self, driver: WebDriver) -> None:
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, AppConfig.DEFAULT_TIMEOUT)
    
    def find_element(self, locator: Locator, timeout: int = 10) -> WebElement:
        """요소 찾기"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            logger.info(f"Element found: {locator}")
            return element
        except TimeoutException as e:
            logger.error(f"Failed to find element: {locator} - {e}")
            raise
    
    def find_elements(self, locator: Locator, timeout: int = 10) -> List[WebElement]:
        """여러 요소 찾기"""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located(locator)
        )
    
    def click(self, locator: Locator, timeout: int = 10) -> WebElement:
        """요소 클릭"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.info(f"Clicked element: {locator}")
            return element
        except (TimeoutException, Exception) as e:
            logger.error(f"Failed to click element: {locator} - {e}")
            raise
        
    def is_element_clickable(self, locator: Locator, timeout: int = 10) -> bool:
        """요소가 클릭 가능한지 확인"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            logger.info(f"Element is clickable: {locator}")
            return True
        except TimeoutException:
            logger.info(f"Element is not clickable: {locator}")
            return False
    
    def input_text(self, locator: Locator, text: str, timeout: int = 10) -> WebElement:
        """텍스트 입력"""
        try:
            element = self.find_element(locator, timeout)
            element.clear()
            element.send_keys(text)
            logger.info(f"Input text to {locator}: {text}")
            return element
        except Exception as e:
            logger.error(f"Failed to input text to {locator} - {e}")
            raise
    
    def swipe_up(self, start_x: int = 500, start_y: int = 1500, end_x: int = 500, end_y: int = 500, duration: int = 500) -> None:
        """위로 스와이프"""
        logger.debug(f"스와이프 UP: ({start_x},{start_y}) → ({end_x},{end_y})")
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        time.sleep(0.5)  # 스와이프 후 안정화 대기

    def swipe_down(self, start_x: int = 500, start_y: int = 500, end_x: int = 500, end_y: int = 1500, duration: int = 500) -> None:
        """아래로 스와이프"""
        logger.debug(f"스와이프 DOWN: ({start_x},{start_y}) → ({end_x},{end_y})")
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        time.sleep(0.5)  # 스와이프 후 안정화 대기

    def scroll_to_element(self, locator: Locator, max_scrolls: int = 5) -> WebElement:
        """요소가 나올 때까지 스크롤"""
        for i in range(max_scrolls):
            try:
                element = self.find_element(locator, timeout=2)
                logger.info(f"Element found after {i+1} scroll(s): {locator}")
                return element
            except (TimeoutException, NoSuchElementException):
                logger.info(f"Scrolling up... ({i+1}/{max_scrolls})")
                self.swipe_up()
        logger.error(f"Element not found after {max_scrolls} scrolls: {locator}")
        raise NoSuchElementException(f"Element not found after {max_scrolls} scrolls")
    
    def take_screenshot(self, name: str = "screenshot") -> Optional[str]:
        """스크린샷 저장"""
        try:
            AppConfig.ensure_directories()
            screenshot_path = f"{AppConfig.SCREENSHOT_DIR}/{name}.png"
            self.driver.get_screenshot_as_file(screenshot_path)
            logger.info(f"Screenshot saved to {screenshot_path}")
            return screenshot_path
        except Exception as e:
            logger.error(f"Failed to take screenshot: {e}")
            return None

    def get_text(self, locator: Locator, timeout: int = 10) -> str:
        """요소의 텍스트 가져오기"""
        try:
            element = self.find_element(locator, timeout)
            text = element.text
            logger.info(f"Got text from {locator}: {text}")
            return text
        except Exception as e:
            logger.error(f"Failed to get text from {locator} - {e}")
            raise

    def is_element_visible(self, locator: Locator, timeout: int = 5) -> bool:
        """요소가 보이는지 확인"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.info(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            logger.info(f"Element is not visible: {locator}")
            return False

    def check_image_loaded(self, image_locator: Locator, timeout: int = 10) -> bool:
        """이미지가 제대로 로드되었는지 확인"""
        try:
            element = self.find_element(image_locator, timeout)

            # 1. 요소 크기 확인 (0x0이면 로드 실패)
            size = element.size
            if size['width'] <= 1 or size['height'] <= 1:
                logger.warning(f"Image has invalid size: {size}")
                return False

            # 2. displayed 속성 확인
            if not element.is_displayed():
                logger.warning(f"Image is not displayed")
                return False

            logger.info(f"Image loaded successfully: {image_locator}")
            return True

        except Exception as e:
            logger.error(f"Failed to check image: {image_locator} - {e}")
            return False

    def find_broken_images(self, wait_for_load: bool = True) -> List[Dict[str, Any]]:
        """
        페이지의 모든 깨진 이미지 찾기

        Args:
            wait_for_load: 이미지 로딩 대기 여부 (기본 True)
        """
        logger.info("=" * 60)
        logger.info("이미지 검증 시작")

        broken_images = []
        valid_images = []

        try:
            # 페이지 로딩 대기
            if wait_for_load:
                logger.info("이미지 로딩 대기 중... (3초)")
                time.sleep(3)

            # 모든 ImageView 요소 찾기
            logger.info("ImageView 요소 검색 중...")
            images = self.driver.find_elements(
                AppiumBy.XPATH,
                "//android.widget.ImageView"
            )
            total_images = len(images)
            logger.info(f"총 {total_images}개의 이미지 발견")

            if total_images == 0:
                logger.warning("⚠️ 이미지가 하나도 발견되지 않음! 페이지가 제대로 로드되었는지 확인 필요")
                return []

            # 각 이미지 검증
            for idx, img in enumerate(images):
                try:
                    # 크기 확인
                    size = img.size
                    bounds = img.get_attribute('bounds')
                    resource_id = img.get_attribute('resource-id') or "Unknown"
                    content_desc = img.get_attribute('content-desc') or ""

                    logger.debug(
                        f"[{idx+1}/{total_images}] "
                        f"ID: {resource_id[:50]}, "
                        f"Size: {size['width']}x{size['height']}"
                    )

                    # 크기가 너무 작으면 깨진 이미지로 판단
                    if size['width'] <= 1 or size['height'] <= 1:
                        broken_images.append({
                            'index': idx,
                            'resource_id': resource_id,
                            'content_desc': content_desc,
                            'bounds': bounds,
                            'size': size,
                            'reason': 'Invalid size (width or height <= 1)'
                        })
                        logger.warning(
                            f"❌ 깨진 이미지 발견 [{idx+1}]: "
                            f"ID={resource_id}, Size={size}"
                        )
                    else:
                        valid_images.append({
                            'index': idx,
                            'resource_id': resource_id,
                            'size': size
                        })

                except Exception as e:
                    logger.error(f"이미지 [{idx+1}] 검증 중 에러: {e}")
                    broken_images.append({
                        'index': idx,
                        'reason': f'Error checking image: {str(e)}'
                    })

            # 결과 요약
            logger.info("=" * 60)
            logger.info(f"✅ 정상 이미지: {len(valid_images)}개")
            logger.info(f"❌ 깨진 이미지: {len(broken_images)}개")
            logger.info(f"📊 전체 검사율: {(len(valid_images) + len(broken_images)) / total_images * 100:.1f}%")
            logger.info("=" * 60)

            return broken_images

        except Exception as e:
            logger.error(f"❌ 이미지 검증 실패: {e}", exc_info=True)
            return []

    def find_broken_images_with_scroll(self, max_scrolls: int = 5, scroll_pause: int = 1) -> List[Dict[str, Any]]:
        """
        스크롤하며 전체 페이지의 깨진 이미지 찾기
        실무용: 긴 리스트 페이지에서 모든 상품 확인

        Args:
            max_scrolls: 최대 스크롤 횟수
            scroll_pause: 스크롤 간 대기 시간(초)
        """
        logger.info("=" * 60)
        logger.info(f"스크롤 이미지 검증 시작 (최대 {max_scrolls}회)")

        all_broken_images = []
        all_valid_images = []
        previous_page_source = None
        scroll_count = 0

        for scroll_num in range(max_scrolls + 1):  # 0번째(현재 화면) 포함
            logger.info(f"\n[스크롤 {scroll_num}/{max_scrolls}] 이미지 검증 중...")

            # 현재 화면 이미지 검증 (대기 없이)
            broken_images = self.find_broken_images(wait_for_load=False)
            all_broken_images.extend(broken_images)

            # 페이지 소스로 스크롤 끝 감지
            current_page_source = self.driver.page_source

            if previous_page_source == current_page_source:
                logger.info(f"⚠️ 페이지 끝 도달 (스크롤 {scroll_num}회 후)")
                break

            previous_page_source = current_page_source

            # 마지막 스크롤이 아니면 계속 스크롤
            if scroll_num < max_scrolls:
                logger.info(f"📜 스크롤 UP 실행...")
                self.swipe_up()
                time.sleep(scroll_pause)
                scroll_count += 1

        # 결과 요약
        logger.info("=" * 60)
        logger.info(f"✅ 총 스크롤 횟수: {scroll_count}회")
        logger.info(f"❌ 전체 깨진 이미지: {len(all_broken_images)}개")
        logger.info("=" * 60)

        return all_broken_images

    def save_broken_images_report(self, report_filename: str = "broken_images_report.txt", wait_for_load: bool = True, with_scroll: bool = False, max_scrolls: int = 5) -> Tuple[str, List[Dict[str, Any]]]:
        """
        깨진 이미지 리포트 저장

        Args:
            report_filename: 리포트 파일명
            wait_for_load: 이미지 로딩 대기 여부
            with_scroll: 스크롤하며 전체 확인 여부 (실무용)
            max_scrolls: 스크롤 최대 횟수
        """
        from datetime import datetime

        AppConfig.ensure_directories()

        logger.info(f"이미지 리포트 생성 시작: {report_filename}")

        if with_scroll:
            logger.info(f"🔄 스크롤 모드: 최대 {max_scrolls}회 스크롤하며 확인")
            broken_images = self.find_broken_images_with_scroll(max_scrolls=max_scrolls)
        else:
            broken_images = self.find_broken_images(wait_for_load=wait_for_load)

        report_path = f"{AppConfig.SCREENSHOT_DIR}/{report_filename}"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"=== Broken Images Report ===\n")
            f.write(f"생성 시간: {timestamp}\n")
            f.write(f"검증 모드: {'스크롤 전체 검증' if with_scroll else '현재 화면만'}\n")
            if with_scroll:
                f.write(f"최대 스크롤: {max_scrolls}회\n")
            f.write(f"깨진 이미지 발견: {len(broken_images)}개\n")
            f.write("=" * 70 + "\n\n")

            if broken_images:
                for img in broken_images:
                    f.write(f"Index: {img.get('index')}\n")
                    f.write(f"Resource ID: {img.get('resource_id', 'N/A')}\n")
                    f.write(f"Content-Desc: {img.get('content_desc', 'N/A')}\n")
                    f.write(f"Bounds: {img.get('bounds', 'N/A')}\n")
                    f.write(f"Size: {img.get('size', 'N/A')}\n")
                    f.write(f"Reason: {img.get('reason')}\n")
                    f.write("-" * 70 + "\n")
            else:
                f.write("✅ 깨진 이미지 없음!\n")

        logger.info(f"📄 리포트 저장 완료: {report_path}")
        return report_path, broken_images