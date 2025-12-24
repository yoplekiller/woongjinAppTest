from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage




class WoongjinAppCategoryPage(BasePage):
    def is_category_page_visible(self) -> bool:
        """카테고리 페이지가 보이는지 확인"""
        CATEGORY_PAGE_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[@text='카테고리']")
        return self.is_element_visible(CATEGORY_PAGE_TITLE)