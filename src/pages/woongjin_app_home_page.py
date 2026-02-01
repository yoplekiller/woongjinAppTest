from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time


class WoongjinAppHomePage(BasePage):
    """웅진마켓 앱 홈페이지 Page Object"""

    # Locators
    SEARCH_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@content-desc='검색어를 입력해 주세요.']")
    CATEGORY_TAB = (AppiumBy.ACCESSIBILITY_ID, "카테고리")
    SEARCH_TAB = (AppiumBy.ACCESSIBILITY_ID, "검색")    
    LIKE_TAB = (AppiumBy.ACCESSIBILITY_ID, "찜")
    HOME_TAB = (AppiumBy.ACCESSIBILITY_ID, "홈")
    MY_PAGE_TAB = (AppiumBy.ACCESSIBILITY_ID, "마이")

    # 홈 화면 확인용 로케이터
    HOME_LOGO = (AppiumBy.XPATH, "//android.widget.TextView[@text='웅진마켓로고']")

    def home_page_is_visible(self) -> bool:
        """홈 페이지가 보이는지 확인"""
        return self.is_element_visible(self.HOME_LOGO)


    def click_search(self):
        """검색 버튼 클릭"""
        self.click(self.SEARCH_BUTTON)

    def click_category_tab(self):
        """카테고리 탭 클릭"""
        self.click(self.CATEGORY_TAB)

    def click_like_tab(self):
        """찜 탭 클릭"""
        self.click(self.LIKE_TAB)

    def click_home_tab(self):
        """홈 탭 클릭"""
        self.click(self.HOME_TAB)

    def click_my_page_tab(self):
        """MY 탭 클릭"""
        self.click(self.MY_PAGE_TAB)

    def click_search_tab(self):
        """검색 탭 클릭"""
        time.sleep(1)
        self.click(self.SEARCH_TAB)

    def swipe_down(self, start_x = 500, start_y = 500, end_x = 500, end_y = 1500, duration = 500):
        return super().swipe_down(start_x, start_y, end_x, end_y, duration)
    
    def swipe_up(self, start_x = 500, start_y = 1500, end_x = 500, end_y = 500, duration = 500):
        return super().swipe_up(start_x, start_y, end_x, end_y, duration)

