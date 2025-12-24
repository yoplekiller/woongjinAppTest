"""
커스텀 예외 클래스
실무용: 의미있는 에러 메시지
"""


class AppiumTestError(Exception):
    """기본 테스트 에러"""
    pass


class ElementNotFoundError(AppiumTestError):
    """요소를 찾을 수 없음"""

    def __init__(self, locator, timeout=10):
        self.locator = locator
        self.timeout = timeout
        super().__init__(
            f"요소를 찾을 수 없습니다: {locator} (타임아웃: {timeout}초)"
        )


class ElementNotClickableError(AppiumTestError):
    """요소를 클릭할 수 없음"""

    def __init__(self, locator, reason=""):
        self.locator = locator
        self.reason = reason
        msg = f"요소를 클릭할 수 없습니다: {locator}"
        if reason:
            msg += f" (이유: {reason})"
        super().__init__(msg)


class PageLoadError(AppiumTestError):
    """페이지 로드 실패"""

    def __init__(self, page_name, timeout=30):
        self.page_name = page_name
        self.timeout = timeout
        super().__init__(
            f"페이지 로드 실패: {page_name} (타임아웃: {timeout}초)"
        )


class PopupHandleError(AppiumTestError):
    """팝업 처리 실패"""

    def __init__(self, popup_name, reason=""):
        self.popup_name = popup_name
        self.reason = reason
        msg = f"팝업 처리 실패: {popup_name}"
        if reason:
            msg += f" (이유: {reason})"
        super().__init__(msg)


class BrokenImageFoundError(AppiumTestError):
    """깨진 이미지 발견"""

    def __init__(self, broken_count, total_count=0):
        self.broken_count = broken_count
        self.total_count = total_count
        msg = f"깨진 이미지 {broken_count}개 발견"
        if total_count > 0:
            msg += f" (전체: {total_count}개)"
        super().__init__(msg)


class AppConnectionError(AppiumTestError):
    """앱 연결 실패"""

    def __init__(self, package_name, activity=""):
        self.package_name = package_name
        self.activity = activity
        msg = f"앱 연결 실패: {package_name}"
        if activity:
            msg += f"/{activity}"
        super().__init__(msg)
