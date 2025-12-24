from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage




class WoongjinAppMyTabPage(BasePage):
    """웅진씽크빅 앱 - 마이탭 페이지"""

    # Locators
    MY_TAB_PAGE_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'마이페이지')]")
    

    def is_my_tab_page_visible(self) -> bool:
        """마이탭 페이지가 보이는지 확인"""
        return self.is_element_visible(self.MY_TAB_PAGE_TITLE)