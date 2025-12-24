from appium.webdriver.common.appiumby import AppiumBy
from src.pages.base_page import BasePage


class WoongjinAppLikePage(BasePage):


    LIKE_PAGE_TITLE = (AppiumBy.XPATH, "//android.widget.TextView[contains(@text,'찜한')]")
    LIKE_ADD_PRODUCT_BUTTON = (AppiumBy.XPATH, "//android.widget.TextView[@text='담기']")
    
    def is_like_page_visible(self) -> bool:
        """찜 페이지가 보이는지 확인"""
        return self.is_element_visible(self.LIKE_PAGE_TITLE)