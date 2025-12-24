"""
화면 상태 디버깅 테스트
검은 화면 원인 파악용
"""
import pytest
import time
from appium.webdriver.common.appiumby import AppiumBy
from utils.page_source_helper import save_page_source


def test_screen_state_debug(driver):
    """현재 화면 상태 디버깅"""

    print("\n" + "=" * 80)
    print("🔍 화면 상태 디버깅 시작")
    print("=" * 80)

    # 1. 현재 activity 확인
    current_activity = driver.current_activity
    current_package = driver.current_package
    print(f"\n📱 현재 Activity: {current_package}/{current_activity}")

    # 2. 화면 크기 확인
    screen_size = driver.get_window_size()
    print(f"📏 화면 크기: {screen_size['width']}x{screen_size['height']}")

    # 3. 즉시 스크린샷 저장
    screenshot_path = "./screenshots/current_screen.png"
    driver.get_screenshot_as_file(screenshot_path)
    print(f"📸 스크린샷 저장: {screenshot_path}")

    # 4. 페이지 소스 저장
    save_page_source(driver, "current_screen.xml")
    print("📄 페이지 소스 저장: page_sources/current_screen.xml")

    # 5. 모든 보이는 요소 개수 확인
    all_elements = driver.find_elements(AppiumBy.XPATH, "//*")
    print(f"\n📊 전체 요소 개수: {len(all_elements)}개")

    # 6. View/ViewGroup 확인
    views = driver.find_elements(AppiumBy.XPATH, "//android.view.View")
    viewgroups = driver.find_elements(AppiumBy.XPATH, "//android.view.ViewGroup")
    print(f"   - View: {len(views)}개")
    print(f"   - ViewGroup: {len(viewgroups)}개")

    # 7. TextView 요소 확인 (텍스트가 있는지)
    textviews = driver.find_elements(AppiumBy.XPATH, "//android.widget.TextView")
    print(f"   - TextView: {len(textviews)}개")

    if textviews:
        print("\n📝 상위 5개 TextView 내용:")
        for idx, tv in enumerate(textviews[:5]):
            text = tv.get_attribute('text') or ""
            resource_id = tv.get_attribute('resource-id') or ""
            if text:
                print(f"   [{idx+1}] {text[:50]} (id: {resource_id})")

    # 8. 클릭 가능한 요소 확인
    clickable = driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
    print(f"\n🖱️ 클릭 가능한 요소: {len(clickable)}개")

    # 9. WebView 확인
    webviews = driver.find_elements(AppiumBy.XPATH, "//android.webkit.WebView")
    print(f"\n🌐 WebView: {len(webviews)}개")

    # 10. ImageView 확인
    imageviews = driver.find_elements(AppiumBy.XPATH, "//android.widget.ImageView")
    print(f"🖼️ ImageView: {len(imageviews)}개")

    print("\n" + "=" * 80)
    print("✅ 디버깅 완료!")
    print("=" * 80)
    print("\n📍 다음 파일들을 확인하세요:")
    print("   1. screenshots/current_screen.png - 현재 화면")
    print("   2. page_sources/current_screen.xml - 페이지 소스")
    print("\n💡 화면이 검은색이라면:")
    print("   - 스크린샷에서 실제로 검은지 확인")
    print("   - XML에서 요소가 있는지 확인")
    print("   - WebView가 로딩 중인지 확인")
