import allure


def test_category_tab(home_page, category_page):
    """웅진마켓 카테고리 테스트"""

    with allure.step("카테고리 탭 클릭"):
        home_page.click_category_tab()

    with allure.step("카테고리 페이지 로딩 검증"):
        assert category_page.is_category_page_visible(), "❌ 카테고리 페이지가 로드되지 않음"
        category_page.take_screenshot("woongjin_category_page.png")


def test_search_tab(home_page, search_page):
    """웅진마켓 검색 기능 테스트"""

    with allure.step("검색 탭 클릭"):
        home_page.click_search_tab()

    with allure.step("검색 페이지 로딩 검증"):
        assert search_page.search_page_is_visible(), "❌ 검색 페이지가 보이지 않음"
        search_page.take_screenshot("woongjin_search_page.png")


def test_like_tab(home_page, login_page, like_page, test_user_credentials):
    user_id = test_user_credentials["user_id"]
    password = test_user_credentials["password"]

    """웅진마켓 찜 탭 테스트"""
    with allure.step("로그인 페이지로 이동"):
        home_page.click_like_tab()
        assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"

    with allure.step("로그인 타입 노출 확인"):
        assert login_page.login_types_are_visible(), "❌ 로그인 타입들이 보이지 않음"

    with allure.step("이메일 로그인 페이지로 이동"):
        login_page.click_email_login()
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"

    with allure.step("이메일 로그인 수행"):
        login_page.email_login(user_id, password)
        assert home_page.home_page_is_visible(), "❌ 로그인 후 홈페이지가 보이지 않음"
        home_page.take_screenshot("woongjin_logged_in_home_page.png")

    with allure.step("찜 페이지 로딩 검증"):
        assert like_page.is_like_page_visible(), "❌ 찜 페이지가 보이지 않음"
        like_page.take_screenshot("woongjin_like_page.png")
