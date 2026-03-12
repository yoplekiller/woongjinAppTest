import allure


def test_search_with_valid_keyword(navigate_to_search_tab):
    """웅진마켓 검색 기능 테스트"""

    search_page = navigate_to_search_tab

    with allure.step("검색어 입력 및 검색 수행"):
        search_keyword = "책"
        search_page.enter_search_text(search_keyword)
        search_page.submit_search()

    with allure.step("검색 결과 확인"):
        assert search_page.is_result_present(search_keyword), "❌ 검색 페이지가 보이지 않음"
        search_page.take_screenshot("woongjin_search_page.png")


def test_search_no_results(navigate_to_search_tab):
    """웅진마켓 검색 - 결과 없는 검색어 테스트"""

    search_page = navigate_to_search_tab

    with allure.step("검색어 입력 및 검색 수행"):
        search_keyword = "asdfghjkl"
        search_page.enter_search_text(search_keyword)
        search_page.submit_search()

    with allure.step("검색 결과 없음 확인"):
        results = search_page.get_search_results()
        assert len(results) == 0, "❌ 예상과 달리 검색 결과가 존재함"
        search_page.take_screenshot("woongjin_search_no_results.png")
