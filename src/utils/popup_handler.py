"""
팝업 처리 유틸리티
"""
from typing import Union
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from config.app_config import AppConfig
import time


def handle_woongjin_popups(driver: WebDriver, wait_time: Union[int, float] = 3, use_position_based: bool = True) -> None:
    """
    웅진마켓 앱 초기 팝업 처리

    Args:
        driver: WebDriver 인스턴스
        wait_time: 팝업 대기 시간 (초)
        use_position_based: 위치 기반 배너 닫기 사용 여부 (기본 True, 자주 바뀌는 배너에 권장)
    """
    
    # 앱 초기 로딩 대기
    print("⏱️ 앱 초기 로딩 대기 중... (2초)")
    time.sleep(2)

    # 권한 요청 팝업 처리
    _handle_permission_guide(driver)

    # 권한 허용 팝업 처리
    _handle_permission_allow(driver)

    # WebView 배너가 실제로 나타날 때까지 대기 (명시적 대기)
    print("\n⏱️ WebView 배너 로딩 대기 중... (최대 10초)")
    banner_loaded = _wait_for_banner_load(driver, timeout=10)

    if not banner_loaded:
        print("⚠️ 배너가 나타나지 않음 - 스킵")
        return

    # 이벤트 배너/팝업 닫기 (조합 전략)
    print("\n🎯 배너 닫기 시도 시작")

    # 전략 1: 요소 찾기 (content-desc='닫기') - 가장 안정적
    print("\n📍 전략 1: content-desc='닫기'로 요소 찾기")
    success = _close_banner_by_element(driver)

    if success:
        print("✅ 요소 찾기 성공!")
        return

    # 전략 2: 위치 기반 클릭 (요소 찾기 실패 시)
    if use_position_based:
        print("\n📍 전략 2: 위치 기반 클릭으로 재시도")
        for attempt in range(3):
            print(f"\n🎯 위치 기반 {attempt+1}차 시도")
            success = _close_banner_by_position(driver, wait_time=0.3)
            if success:
                print("✅ 위치 기반 클릭 성공!")
                return
            time.sleep(0.5)

    print("\n⚠️ 모든 배너 닫기 시도 실패")


def _wait_for_banner_load(driver: WebDriver, timeout: int = 15) -> bool:
    """
    배너가 실제로 로드될 때까지 명시적으로 대기

    Args:
        driver: WebDriver 인스턴스
        timeout: 최대 대기 시간 (초)

    Returns:
        배너 로드 성공 여부 (bool)
    """
    # 배너 관련 요소들 (하나라도 나타나면 배너 로드됨)
    banner_indicators = [
        (AppiumBy.ID, "groobeeWrap"),           # 배너 컨테이너
        (AppiumBy.ID, "grb-close-x"),           # 닫기 버튼
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'innerWrap')]"),  # 내부 래퍼
    ]

    for indicator_by, indicator_locator in banner_indicators:
        try:
            print(f"  🔍 배너 요소 확인 중: {indicator_locator[:50]}...")
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((indicator_by, indicator_locator))
            )
            print(f"  ✅ 배너 로드 완료! (감지: {indicator_locator[:50]})")
            time.sleep(1)  # 배너 애니메이션 안정화 대기
            return True
        except TimeoutException:
            continue

    print(f"  ⚠️ {timeout}초 동안 배너가 나타나지 않음")
    return False


def _handle_permission_guide(driver: WebDriver, timeout: int = 5) -> None:
    """권한 안내 팝업 처리"""
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "com.wjthinkbig.woongjinbooks:id/btnPermGuideOk")
            )
        ).click()
        print("✅ 권한 안내 팝업 처리 완료")
    except (TimeoutException, NoSuchElementException):
        print("ℹ️ 권한 안내 팝업 없음")


def _handle_permission_allow(driver: WebDriver, timeout: int = 5) -> None:
    """권한 허용 팝업 처리"""
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button")
            )
        ).click()
        print("✅ 권한 허용 팝업 처리 완료")
    except (TimeoutException, NoSuchElementException):
        print("ℹ️ 권한 허용 팝업 없음")


def _close_banner_by_element(driver: WebDriver, timeout: int = 2) -> bool:
    """
    요소 속성으로 배너 닫기 버튼 찾아서 클릭

    Args:
        driver: WebDriver 인스턴스
        timeout: 요소 찾기 타임아웃 (초)

    Returns:
        성공 여부 (bool)
    """
    # 닫기 버튼 찾기 패턴 (우선순위 순)
    close_button_patterns = [
        # 1순위: Groobee 배너 닫기 (웅진마켓 실제 배너)
        (AppiumBy.ID, "grb-close-x"),
        (AppiumBy.XPATH, "//*[@resource-id='grb-close-x']"),
        (AppiumBy.ID, "ifp1"),  # 배너 닫기 이미지

        # 2순위: 일반적인 content-desc
        (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='닫기']"),
        (AppiumBy.ACCESSIBILITY_ID, "닫기"),

        # 3순위: 다른 타입의 닫기 버튼
        (AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='닫기']"),
        (AppiumBy.XPATH, "//android.widget.Button[@content-desc='닫기']"),

        # 4순위: 영어 패턴
        (AppiumBy.ACCESSIBILITY_ID, "close"),
        (AppiumBy.ACCESSIBILITY_ID, "Close"),

        # 5순위: 부분 일치
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'close')]"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, '닫기')]"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'close')]"),

        # 6순위: text 속성
        (AppiumBy.XPATH, "//*[@text='닫기']"),
        (AppiumBy.XPATH, "//*[@text='X']"),
    ]

    for idx, (by, locator) in enumerate(close_button_patterns):
        try:
            print(f"  [{idx+1}/{len(close_button_patterns)}] 시도: {locator[:60]}...")

            # timeout 짧게 설정 (빠른 실패)
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, locator))
            )

            # 요소 찾았으면 클릭 시도
            element.click()
            print(f"  ✅ 닫기 버튼 클릭 성공! (패턴: {idx+1})")
            time.sleep(0.5)  # 클릭 후 안정화
            return True

        except (TimeoutException, NoSuchElementException):
            print(f"  ✗ 패턴 {idx+1} 실패")
            continue
        except Exception as e:
            print(f"  ✗ 클릭 실패: {str(e)[:50]}")
            continue

    print("  ⚠️ 모든 요소 찾기 패턴 실패")
    return False


def _close_banner_by_position(driver: WebDriver, wait_time: float = 1.0) -> bool:
    """
    화면 특정 위치 클릭으로 배너 닫기 (자주 바뀌는 배너에 최적화)
    배너 닫기 버튼이 보통 우측/좌측 상단에 위치한다는 것을 활용

    Args:
        driver: WebDriver 인스턴스
        wait_time: 배너 로딩 대기 시간 (초)

    Returns:
        성공 여부 (bool)
    """
    print("=== 위치 기반 배너 닫기 시도 ===")

    # 배너가 완전히 로드될 때까지 대기
    time.sleep(wait_time)

    try:
        # 화면 크기 동적으로 가져오기
        screen_size = driver.get_window_size()
        width = screen_size['width']
        height = screen_size['height']

        print(f"📱 화면 크기: {width}x{height}")

        # 닫기 버튼이 위치할 가능성이 높은 좌표들 (우선순위 순)
        # 웅진마켓 실제 위치: (88.5%, 31%) 기준
        close_button_positions = [
            # 1순위: 웅진마켓 배너 실제 위치 (분석 결과 기반)
            (int(width * 0.885), int(height * 0.31)),  # 실제 위치
            (int(width * 0.88), int(height * 0.30)),   # 약간 왼쪽 위
            (int(width * 0.89), int(height * 0.32)),   # 약간 오른쪽 아래

            # 2순위: 일반적인 우측 상단
            (int(width * 0.95), int(height * 0.05)),
            (int(width * 0.93), int(height * 0.08)),
            (int(width * 0.90), int(height * 0.10)),

            # 3순위: 좌측 상단
            (int(width * 0.05), int(height * 0.05)),
            (int(width * 0.07), int(height * 0.08)),

            # 4순위: 중앙 상단
            (int(width * 0.50), int(height * 0.05)),

            # 5순위: 우측 중앙
            (int(width * 0.95), int(height * 0.50)),
        ]

        for idx, (x, y) in enumerate(close_button_positions):
            try:
                print(f"  [{idx+1}/{len(close_button_positions)}] 위치 클릭 시도: ({x}, {y})")
                driver.tap([(x, y)])
                time.sleep(0.3)
                print(f"  ✅ 위치 ({x}, {y}) 클릭 성공!")
                return True
            except Exception as e:
                print(f"  ✗ 실패: {str(e)[:50]}")
                continue

        print("  ⚠️ 모든 위치 클릭 실패")
        return False

    except Exception as e:
        print(f"  ❌ 화면 크기 확인 실패: {e}")
        return False


# def _close_banner_if_exists(driver: WebDriver) -> bool:
#     """
#     이벤트 배너/팝업 닫기 (여러 방법 시도)
#     실무용: 모든 가능한 방법으로 팝업 닫기
#     """
#     print("\n=== 팝업 닫기 시도 ===")

#     # 방법 1: 닫기 버튼 찾기 (여러 패턴)
#     close_buttons = [
#         (AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='닫기']"),
#         (AppiumBy.ACCESSIBILITY_ID, "닫기"),
#         (AppiumBy.ACCESSIBILITY_ID, "close"),
#         (AppiumBy.XPATH, "//android.widget.ImageButton[@content-desc='닫기']"),
#         (AppiumBy.XPATH, "//*[@content-desc='닫기']"),
#         (AppiumBy.XPATH, "//*[@text='닫기']"),
#         (AppiumBy.XPATH, "//*[contains(@content-desc, '닫기')]"),
#         (AppiumBy.XPATH, "//*[contains(@text, '닫기')]"),
#         (AppiumBy.ID, "com.wjthinkbig.woongjinbooks:id/btn_close"),
#         (AppiumBy.ID, "btn_close"),
#         (AppiumBy.XPATH, "//android.widget.ImageView[@clickable='true'][1]"),  # 첫 번째 클릭 가능한 이미지
#     ]

#     for idx, (by, locator) in enumerate(close_buttons):
#         try:
#             print(f"  [{idx+1}] 시도: {locator[:50]}...")
#             close_btn = driver.find_element(by, locator)
#             close_btn.click()
#             print("  ✅ 닫기 버튼 클릭 성공!")
#             time.sleep(0.5)
#             return True
#         except Exception as e:
#             print(f"  ✗ 실패: {str(e)[:50]}")
#             continue

#     # 방법 2: 뒤로가기
#     try:
#         print("  [방법 2] 뒤로가기 시도...")
#         driver.back()
#         time.sleep(0.5)
#         print("  ✅ 뒤로가기 성공!")
#         return True
#     except Exception as e:
#         print(f"  ✗ 뒤로가기 실패: {e}")

#     # 방법 3: 화면 바깥쪽 탭 (팝업 바깥을 탭하면 닫히는 경우)
#     try:
#         print("  [방법 3] 화면 상단 탭 시도...")
#         driver.tap([(100, 100)])  # 좌상단
#         time.sleep(0.5)
#         print("  ✅ 화면 탭 성공!")
#         return True
#     except Exception as e:
#         print(f"  ✗ 화면 탭 실패: {e}")

#     # 방법 4: 화면 중앙 바깥 탭
#     try:
#         print("  [방법 4] 화면 오른쪽 상단 탭 시도...")
#         screen_size = driver.get_window_size()
#         driver.tap([(screen_size['width'] - 100, 100)])  # 우상단
#         time.sleep(0.5)
#         print("  ✅ 우상단 탭 성공!")
#         return True
#     except Exception as e:
#         print(f"  ✗ 우상단 탭 실패: {e}")

#     # 방법 5: ESC 키 (일부 앱에서 작동)
#     try:
#         print("  [방법 5] ESC 키 시도...")
#         driver.press_keycode(4)  # Android BACK 키코드
#         time.sleep(0.5)
#         print("  ✅ ESC 키 성공!")
#         return True
#     except Exception as e:
#         print(f"  ✗ ESC 키 실패: {e}")

#     print("  ⚠️ 모든 방법 실패 - 팝업이 없거나 다른 방법 필요")
#     return False
