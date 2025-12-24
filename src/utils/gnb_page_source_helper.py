"""
페이지 소스 관련 유틸리티
"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from appium.webdriver.webdriver import WebDriver
from config.app_config import AppConfig
import xml.etree.ElementTree as ET


def save_page_source(driver: WebDriver, filename: str = "page_source.xml") -> str:
    """현재 화면의 UI 계층 구조를 XML 파일로 저장"""
    AppConfig.ensure_directories()

    source = driver.page_source
    filepath = f"{AppConfig.PAGE_SOURCE_DIR}/{filename}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(source)

    print(f"Page source saved to {filepath}")
    return source


def save_gnb_source(driver: WebDriver, filename: str = "gnb_source.xml") -> str:
    """
    GNB(Global Navigation Bar) 영역만 추출하여 저장
    
    Args:
        driver: WebDriver 인스턴스
        filename: 저장할 파일명
        
    Returns:
        추출된 GNB XML 문자열
    """
    AppConfig.ensure_directories()
    
    source = driver.page_source
    
    try:
        # XML 파싱
        root = ET.fromstring(source)
        
        # GNB 영역 찾기 (여러 패턴 시도)
        gnb_patterns = [
            ".//android.widget.LinearLayout[@resource-id='com.wjthinkbig.woongjinbooks:id/ll_gnb']",
            ".//android.widget.LinearLayout[@resource-id='com.wjthinkbig.woongjinbooks:id/bottom_navigation']",
            ".//*[@resource-id='com.wjthinkbig.woongjinbooks:id/ll_gnb']",
            ".//*[contains(@resource-id, 'gnb')]",
            ".//*[contains(@resource-id, 'bottom')]",
            ".//*[contains(@resource-id, 'navigation')]",
        ]
        
        gnb_element = None
        for pattern in gnb_patterns:
            gnb_element = root.find(pattern)
            if gnb_element is not None:
                print(f"✅ GNB 영역 발견: {pattern}")
                break
        
        if gnb_element is None:
            print("⚠️ GNB 영역을 찾을 수 없습니다. 전체 소스를 저장합니다.")
            gnb_xml = source
        else:
            # GNB 요소를 XML 문자열로 변환
            gnb_xml = ET.tostring(gnb_element, encoding='unicode')
        
        # 파일 저장
        filepath = f"{AppConfig.PAGE_SOURCE_DIR}/{filename}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(gnb_xml)
        
        print(f"📄 GNB source saved to {filepath}")
        return gnb_xml
        
    except Exception as e:
        print(f"❌ GNB 추출 실패: {e}")
        print("전체 소스를 저장합니다.")
        return save_page_source(driver, filename)


def print_gnb_elements(driver: WebDriver) -> None:
    """GNB 영역의 모든 요소 출력"""
    from appium.webdriver.common.appiumby import AppiumBy
    
    print("\n=== GNB 영역 요소 분석 ===\n")
    
    # GNB 영역 찾기
    gnb_selectors = [
        (AppiumBy.ID, "com.wjthinkbig.woongjinbooks:id/ll_gnb"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'gnb')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'bottom')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'navigation')]"),
    ]
    
    gnb_container = None
    for by, selector in gnb_selectors:
        try:
            gnb_container = driver.find_element(by, selector)
            print(f"✅ GNB 컨테이너 발견: {selector}")
            break
        except:
            continue
    
    if gnb_container is None:
        print("⚠️ GNB 컨테이너를 찾을 수 없습니다.")
        return
    
    # GNB 내부의 모든 요소 찾기
    try:
        elements = gnb_container.find_elements(AppiumBy.XPATH, ".//*")
        print(f"\n📊 GNB 내부 요소 수: {len(elements)}\n")
        
        for idx, elem in enumerate(elements):
            try:
                tag = elem.tag_name
                resource_id = elem.get_attribute('resource-id') or ""
                text = elem.get_attribute('text') or ""
                content_desc = elem.get_attribute('content-desc') or ""
                clickable = elem.get_attribute('clickable') or ""
                
                print(f"[{idx+1}] {tag}")
                if resource_id:
                    print(f"    ├─ Resource-ID: {resource_id}")
                if text:
                    print(f"    ├─ Text: {text}")
                if content_desc:
                    print(f"    ├─ Content-desc: {content_desc}")
                if clickable == "true":
                    print(f"    └─ ✅ Clickable")
                print()
                
            except Exception as e:
                print(f"[{idx+1}] Error: {e}\n")
                
    except Exception as e:
        print(f"❌ GNB 요소 분석 실패: {e}")


def print_all_elements(driver: WebDriver) -> None:
    """화면의 모든 요소 정보 출력"""

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