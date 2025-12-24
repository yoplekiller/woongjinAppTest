import time
import allure



def test_search_with_valid_keyword(home_page, search_page):
    """웅진마켓 검색 기능 테스트"""

    with allure.step("검색 버튼 클릭"):
        home_page.click_search_tab()
        print("🔍 검색 탭 클릭 완료")

    with allure.step("검색어 입력 및 검색 수행"):
        search_keyword = "책"
        search_page.enter_search_text(search_keyword)
        search_page.submit_search()
        print(f"✅ '{search_keyword}' 검색어로 검색 수행 완료")
   
    
    with allure.step("검색 결과 확인"):
        assert search_page.is_result_present(search_keyword), "❌ 검색 페이지가 보이지 않음"
        time.sleep(2)  # 페이지 로딩 대기
        take_screenshot = search_page.take_screenshot("woongjin_search_page.png")
        print("✅ 검색 결과 확인")