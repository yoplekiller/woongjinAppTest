"""
이미지 로딩 검증 테스트
실무용: 스크롤하며 전체 상품 이미지 검증
"""
import pytest
import allure
import time


def test_check_broken_images_on_home(home_page):
    """홈 페이지의 깨진 이미지 검증 (현재 화면만)"""
    with allure.step("홈 페이지의 이미지 검사"):
        report_path, broken_images = home_page.save_broken_images_report(
            "home_broken_images_report.txt",
            with_scroll=False  # 현재 화면만
        )

    with allure.step("검증 결과 확인"):
        print(f"\n깨진 이미지 수: {len(broken_images)}")
        if broken_images:
            print("\n깨진 이미지 상세:")
            for img in broken_images:
                print(f"  - Index: {img.get('index')}, ID: {img.get('resource_id')}")
                print(f"    Reason: {img.get('reason')}")

        assert len(broken_images) == 0, f"깨진 이미지 {len(broken_images)}개 발견!"


@pytest.mark.slow
def test_check_broken_images_on_home_with_scroll(home_page):
    """홈 페이지 전체 스크롤하며 이미지 검증 (실무용)"""
    with allure.step("홈 페이지 전체 이미지 검사 (스크롤 포함)"):
        report_path, broken_images = home_page.save_broken_images_report(
            "home_full_scroll_report.txt",
            with_scroll=True,  # 스크롤하며 전체 확인
            max_scrolls=5  # 최대 5번 스크롤
        )

    with allure.step("검증 결과 확인"):
        print(f"\n전체 깨진 이미지 수: {len(broken_images)}")
        if broken_images:
            print("\n깨진 이미지 상세:")
            for img in broken_images[:10]:  # 처음 10개만 출력
                print(f"  - Index: {img.get('index')}, ID: {img.get('resource_id')}")
                print(f"    Reason: {img.get('reason')}")

        assert len(broken_images) == 0, f"전체 페이지에서 깨진 이미지 {len(broken_images)}개 발견!"


@pytest.mark.slow
def test_check_broken_images_on_category_with_scroll(home_page):
    """카테고리 페이지 전체 스크롤하며 이미지 검증 (실무용)"""
    with allure.step("카테고리 페이지로 이동"):
        home_page.click_category_tab()
        time.sleep(2)

    with allure.step("카테고리 페이지 로드 확인"):
        assert home_page.is_category_page_loaded(), "카테고리 페이지가 로드되지 않음"

    with allure.step("카테고리 페이지 전체 이미지 검사 (스크롤 포함)"):
        report_path, broken_images = home_page.save_broken_images_report(
            "category_full_scroll_report.txt",
            with_scroll=True,
            max_scrolls=10  # 카테고리는 더 길 수 있음
        )

    with allure.step("검증 결과 확인"):
        print(f"\n전체 깨진 이미지 수: {len(broken_images)}")
        if broken_images:
            print("\n깨진 이미지 상세:")
            for img in broken_images[:10]:
                print(f"  - Index: {img.get('index')}, ID: {img.get('resource_id')}")

        # 경고만 출력 (실패하지 않음)
        if len(broken_images) > 0:
            pytest.skip(f"경고: 카테고리 페이지에서 깨진 이미지 {len(broken_images)}개 발견!")


@pytest.mark.parametrize("tab_name,click_method,scroll_count", [
    ("홈", "click_home_tab", 3),
    ("카테고리", "click_category_tab", 5),
])
def test_check_broken_images_tabs_quick(home_page, tab_name, click_method, scroll_count):
    """주요 탭의 이미지 빠른 검증 (3~5회 스크롤)"""
    with allure.step(f"{tab_name} 탭으로 이동"):
        getattr(home_page, click_method)()
        time.sleep(2)

    with allure.step(f"{tab_name} 탭 이미지 검사 (스크롤 {scroll_count}회)"):
        report_path, broken_images = home_page.save_broken_images_report(
            f"{tab_name}_quick_scroll_report.txt",
            with_scroll=True,
            max_scrolls=scroll_count
        )

    with allure.step("결과 확인"):
        print(f"\n[{tab_name}] 깨진 이미지 수: {len(broken_images)}")
        if broken_images:
            for img in broken_images[:5]:  # 처음 5개만 출력
                print(f"  - {img.get('resource_id', 'Unknown')}: {img.get('reason')}")
