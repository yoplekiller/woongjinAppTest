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

    def home_page_is_visible(self) -> bool:
        """홈 페이지가 보이는지 확인"""
        HOME_PAGE_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[@text='웅진마켓']")
        return self.is_element_visible(HOME_PAGE_TITLE)


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

 