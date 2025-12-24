from typing import List
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class WoongjinAppSearchPage(BasePage):
    """웅진마켓 앱 검색 페이지 Page Object"""

    # Locators
    SEARCH_INPUT = (AppiumBy.ID, "searchInput")
    SEARCH_PAGE_TITLE =(AppiumBy.XPATH, "//android.widget.TextView[@text='급상승 검색어']")
    BACK_BUTTON = (AppiumBy.XPATH, "//android.widget.Button[@text='뒤로가기']")
    SEARCH_RESULT_ITEMS = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='product_name']")
    def search_page_is_visible(self) -> bool:
        """검색 페이지에 진입 했는지 확인"""
        return self.is_element_visible(self.SEARCH_PAGE_TITLE)

    def enter_search_text(self, search_text: str):
        """검색어 입력"""
        try:
            self.wait_for_element(self.SEARCH_INPUT)
            logger.info(f"검색어 입력: {search_text}")
            self.click(self.SEARCH_INPUT)
            return self.input_text(self.SEARCH_INPUT, search_text)
        except Exception as e:
            logger.error(f"검색어 입력 실패: {e}")
            return False

    def submit_search(self):
        """검색어 제출"""
        self.driver.press_keycode(66)  # Android의 Enter 키 코드

    def get_search_results(self) -> List[str]:
        """검색 결과 가져오기"""
        try:
            elements = self.find_elements(self.SEARCH_RESULT_ITEMS)
            results = [element.text for element in elements]

            logger.info(f"검색 결과: {len(results)}개") 
            return results
        except Exception as e:
            logger.error(f"검색 실패: {e}")  
            return []
        
    def get_results_containing_keyword(self, keyword: str) -> List[str]:
        """특정 키워드를 포함하는 검색 결과 가져오기"""
        all_results = self.get_search_results()
        filtered_results = [result for result in all_results if keyword in result]
        logger.info(f"키워드 '{keyword}'를 포함하는 결과 수: {len(filtered_results)}")
        return filtered_results
    
    
    def is_result_present(self, keyword: str) -> bool:
        """특정 키워드가 검색 결과에 존재하는지 확인"""
        results = self.get_search_results()
        for result in results:
            if keyword in result:
                logger.info(f"키워드 '{keyword}'가 검색 결과에 존재합니다.")
                return True
        logger.info(f"키워드 '{keyword}'가 검색 결과에 존재하지 않습니다.")
        return False



