"""
페이지 소스 관련 유틸리티
"""
from appium.webdriver.webdriver import WebDriver
from config.app_config import AppConfig


def save_page_source(driver: WebDriver, filename: str = "page_source.xml") -> str:
    """현재 화면의 UI 계층 구조를 XML 파일로 저장"""
    AppConfig.ensure_directories()

    source = driver.page_source
    filepath = f"{AppConfig.PAGE_SOURCE_DIR}/{filename}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(source)

    print(f"Page source saved to {filepath}")
    return source


def print_all_elements(driver: WebDriver) -> None:
    """화면의 모든 요소 정보 출력"""
    from appium.webdriver.common.appiumby import AppiumBy

    elements = driver.find_elements(AppiumBy.XPATH, "//*")
    print(f"\n=== 전체 요소 수: {len(elements)} ===\n")

    for idx, elem in enumerate(elements[:50]):  # 처음 50개만 출력
        try:
            tag = elem.tag_name
            resource_id = elem.get_attribute('resource-id') or ""
            text = elem.get_attribute('text') or ""
            content_desc = elem.get_attribute('content-desc') or ""

            if resource_id or text or content_desc:
                print(f"[{idx}] Tag: {tag}")
                if resource_id:
                    print(f"    Resource-ID: {resource_id}")
                if text:
                    print(f"    Text: {text}")
                if content_desc:
                    print(f"    Content-desc: {content_desc}")
                print()
        except Exception as e:
            print(f"[{idx}] Error: {e}")


def print_elements_with_content_desc(driver: WebDriver) -> None:
    """content-desc가 있는 요소만 출력"""
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.common.exceptions import StaleElementReferenceException

    elements = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc and @content-desc!='']")
    print(f"\n=== Content-desc가 있는 요소 ({len(elements)}개) ===\n")

    for elem in elements:
        try:
            desc = elem.get_attribute('content-desc')
            if desc:
                print(f"  - '{desc}'")
        except StaleElementReferenceException:
            continue


def print_elements_with_text(driver: WebDriver, limit: int = 20) -> None:
    """text가 있는 요소만 출력"""
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.common.exceptions import StaleElementReferenceException

    elements = driver.find_elements(AppiumBy.XPATH, "//*[@text and @text!='']")
    print(f"\n=== Text가 있는 요소 (처음 {limit}개) ===\n")

    count = 0
    for elem in elements:
        if count >= limit:
            break
        try:
            text = elem.get_attribute('text')
            if text:
                print(f"  - '{text}'")
                count += 1
        except StaleElementReferenceException:
            continue
