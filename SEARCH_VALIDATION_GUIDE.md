# 검색 결과 검증 가이드

## 🎯 목표
검색어로 검색한 결과가 실제로 해당 키워드를 포함하는지 검증

---

## 📋 검증 방법 (3가지)

### 방법 1: 상품명에 검색어 포함 여부 확인 (기본)

#### SearchPage에 메서드 추가

**파일:** `src/pages/woongjin_app_search_page.py`

```python
from typing import List

class WoongjinAppSearchPage(BasePage):

    # Locators
    SEARCH_INPUT = (AppiumBy.ID, "search_input")
    SEARCH_BUTTON = (AppiumBy.ID, "search_button")
    SEARCH_RESULT_ITEMS = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='product_name']")
    # 실제 앱의 상품명 요소 locator로 변경 필요

    def get_search_results(self) -> List[str]:
        """검색 결과 상품명 리스트 반환"""
        elements = self.find_elements(self.SEARCH_RESULT_ITEMS)
        return [element.text for element in elements]

    def verify_search_results_contain_keyword(self, keyword: str) -> bool:
        """모든 검색 결과가 키워드를 포함하는지 확인"""
        results = self.get_search_results()

        if not results:
            logger.warning("검색 결과가 없습니다")
            return False

        keyword_lower = keyword.lower()

        for product_name in results:
            if keyword_lower not in product_name.lower():
                logger.warning(f"키워드 미포함 상품 발견: {product_name}")
                return False

        logger.info(f"✅ 모든 상품({len(results)}개)이 '{keyword}' 포함")
        return True

    def get_results_containing_keyword(self, keyword: str) -> List[str]:
        """키워드를 포함하는 상품만 필터링"""
        results = self.get_search_results()
        keyword_lower = keyword.lower()

        matching = [name for name in results if keyword_lower in name.lower()]

        logger.info(f"검색 결과: 전체 {len(results)}개 중 {len(matching)}개 일치")
        return matching
```

---

### 방법 2: 일부만 포함되도록 검증 (실용적)

실제 앱에서는 연관 상품도 나오므로 100% 일치는 어려움

```python
def verify_search_results_relevance(self, keyword: str, threshold: float = 0.7) -> bool:
    """
    검색 결과 중 일정 비율 이상이 키워드를 포함하는지 확인

    Args:
        keyword: 검색 키워드
        threshold: 최소 일치 비율 (0.7 = 70% 이상)

    Returns:
        bool: 기준 충족 여부
    """
    results = self.get_search_results()

    if not results:
        return False

    matching = self.get_results_containing_keyword(keyword)
    match_rate = len(matching) / len(results)

    logger.info(f"일치율: {match_rate:.1%} (기준: {threshold:.0%})")

    return match_rate >= threshold
```

---

### 방법 3: 상세 검증 (상품명 + 설명)

```python
# Locators 추가
PRODUCT_CARDS = (AppiumBy.XPATH, "//android.view.ViewGroup[@resource-id='product_card']")
PRODUCT_NAME = (AppiumBy.ID, "product_name")
PRODUCT_DESCRIPTION = (AppiumBy.ID, "product_description")

def get_detailed_search_results(self) -> List[dict]:
    """검색 결과 상세 정보 반환"""
    product_cards = self.find_elements(self.PRODUCT_CARDS)
    results = []

    for card in product_cards:
        try:
            name = card.find_element(*self.PRODUCT_NAME).text
            description = card.find_element(*self.PRODUCT_DESCRIPTION).text

            results.append({
                "name": name,
                "description": description
            })
        except Exception as e:
            logger.warning(f"상품 정보 추출 실패: {e}")

    return results

def verify_keyword_in_name_or_description(self, keyword: str) -> bool:
    """상품명 또는 설명에 키워드 포함 여부 확인"""
    results = self.get_detailed_search_results()
    keyword_lower = keyword.lower()

    all_match = True
    for product in results:
        name_match = keyword_lower in product["name"].lower()
        desc_match = keyword_lower in product["description"].lower()

        if not (name_match or desc_match):
            logger.warning(f"키워드 미포함: {product['name']}")
            all_match = False

    return all_match
```

---

## 🧪 테스트 케이스 예시

### 예시 1: 기본 검증

**파일:** `src/tests/test_search.py`

```python
import allure
import pytest
from utils.logger import get_logger

logger = get_logger(__name__)


@allure.feature("검색")
@allure.story("검색 결과 검증")
def test_search_results_contain_keyword(home_page, search_page):
    """검색 결과가 검색어를 포함하는지 확인"""
    keyword = "동화책"

    with allure.step(f"'{keyword}' 검색"):
        home_page.click_search_tab()
        search_page.enter_search_keyword(keyword)
        search_page.click_search_button()

    with allure.step("검색 결과 확인"):
        results = search_page.get_search_results()
        assert len(results) > 0, "검색 결과가 없습니다"
        logger.info(f"검색 결과: {len(results)}개")

    with allure.step("키워드 포함 여부 검증"):
        # 모든 결과가 키워드 포함하는지
        assert search_page.verify_search_results_contain_keyword(keyword), \
            f"일부 상품이 '{keyword}'를 포함하지 않습니다"

    with allure.step("스크린샷 저장"):
        search_page.take_screenshot(f"search_{keyword}.png")
```

---

### 예시 2: 일치율 기반 검증 (실용적)

```python
@pytest.mark.parametrize("keyword,min_match_rate", [
    ("책", 0.7),        # 70% 이상 일치
    ("동화", 0.6),      # 60% 이상 일치
    ("그림책", 0.8),    # 80% 이상 일치
])
def test_search_results_relevance(home_page, search_page, keyword, min_match_rate):
    """검색 결과 관련성 확인 (일치율 기반)"""

    with allure.step(f"'{keyword}' 검색"):
        home_page.click_search_tab()
        search_page.enter_search_keyword(keyword)
        search_page.click_search_button()

    with allure.step(f"일치율 {min_match_rate:.0%} 이상 확인"):
        assert search_page.verify_search_results_relevance(keyword, min_match_rate), \
            f"검색 결과 일치율이 {min_match_rate:.0%} 미만입니다"
```

---

### 예시 3: 개별 상품 검증

```python
def test_search_results_detailed(home_page, search_page):
    """검색 결과 상세 검증"""
    keyword = "동화책"

    with allure.step(f"'{keyword}' 검색"):
        home_page.click_search_tab()
        search_page.enter_search_keyword(keyword)
        search_page.click_search_button()

    with allure.step("각 상품 검증"):
        results = search_page.get_search_results()
        keyword_lower = keyword.lower()

        matched_count = 0
        for i, product_name in enumerate(results, 1):
            if keyword_lower in product_name.lower():
                logger.info(f"✅ [{i}] {product_name}")
                matched_count += 1
            else:
                logger.warning(f"❌ [{i}] {product_name} (키워드 미포함)")

        # 최소 70% 이상 일치해야 통과
        match_rate = matched_count / len(results)
        assert match_rate >= 0.7, \
            f"일치율 {match_rate:.1%} (기준: 70% 이상)"

        allure.attach(
            f"일치: {matched_count}/{len(results)} ({match_rate:.1%})",
            name="검증 결과",
            attachment_type=allure.attachment_type.TEXT
        )
```

---

## 🔍 고급 검증 방법

### 1. 한글 자모 분리 검증 (초성 검색)

```python
def normalize_korean(text: str) -> str:
    """한글 정규화 (자모 분리)"""
    import unicodedata
    return unicodedata.normalize('NFC', text)

def verify_search_with_korean(self, keyword: str) -> bool:
    """한글 검색 시 정규화 후 비교"""
    results = self.get_search_results()
    keyword_normalized = normalize_korean(keyword.lower())

    for product in results:
        product_normalized = normalize_korean(product.lower())
        if keyword_normalized not in product_normalized:
            return False

    return True
```

---

### 2. 유사도 기반 검증 (추천)

```python
from difflib import SequenceMatcher

def calculate_similarity(text1: str, text2: str) -> float:
    """두 텍스트 간 유사도 계산 (0.0 ~ 1.0)"""
    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

def verify_search_by_similarity(self, keyword: str, threshold: float = 0.3) -> bool:
    """
    유사도 기반 검색 결과 검증

    Args:
        keyword: 검색 키워드
        threshold: 최소 유사도 (0.3 = 30% 이상)
    """
    results = self.get_search_results()

    for product_name in results:
        similarity = calculate_similarity(keyword, product_name)

        if similarity < threshold:
            logger.warning(f"유사도 낮음: {product_name} ({similarity:.1%})")
            return False

    return True
```

---

### 3. 스크롤하며 전체 결과 검증

```python
def get_all_search_results_with_scroll(self, max_scrolls: int = 5) -> List[str]:
    """스크롤하며 전체 검색 결과 수집"""
    all_results = []
    previous_count = 0

    for i in range(max_scrolls):
        # 현재 화면의 결과 수집
        current_results = self.get_search_results()
        all_results.extend(current_results)

        # 중복 제거
        all_results = list(dict.fromkeys(all_results))

        # 더 이상 새로운 결과가 없으면 종료
        if len(all_results) == previous_count:
            logger.info(f"더 이상 결과 없음 (스크롤 {i}회)")
            break

        previous_count = len(all_results)

        # 스크롤
        self.swipe_up()
        self.wait(1)

    logger.info(f"전체 검색 결과: {len(all_results)}개")
    return all_results

def test_search_all_results(home_page, search_page):
    """전체 검색 결과 검증 (스크롤 포함)"""
    keyword = "책"

    with allure.step(f"'{keyword}' 검색"):
        home_page.click_search_tab()
        search_page.enter_search_keyword(keyword)
        search_page.click_search_button()

    with allure.step("스크롤하며 전체 결과 수집"):
        all_results = search_page.get_all_search_results_with_scroll()
        assert len(all_results) >= 10, "검색 결과가 너무 적습니다"

    with allure.step("키워드 포함 여부 검증"):
        matching = [r for r in all_results if keyword in r.lower()]
        match_rate = len(matching) / len(all_results)

        logger.info(f"일치: {len(matching)}/{len(all_results)} ({match_rate:.1%})")
        assert match_rate >= 0.5, f"일치율이 50% 미만입니다 ({match_rate:.1%})"
```

---

## 💡 실무 권장 방법

### 추천 조합

```python
def test_search_comprehensive(home_page, search_page):
    """검색 기능 종합 테스트"""
    keyword = "동화책"

    with allure.step("1. 검색 실행"):
        home_page.click_search_tab()
        search_page.enter_search_keyword(keyword)
        search_page.click_search_button()

    with allure.step("2. 결과 존재 확인"):
        results = search_page.get_search_results()
        assert len(results) > 0, "검색 결과가 없습니다"
        logger.info(f"✅ 검색 결과: {len(results)}개")

    with allure.step("3. 관련성 확인 (70% 이상)"):
        match_rate = search_page.verify_search_results_relevance(keyword, 0.7)
        assert match_rate, "검색 결과 관련성이 낮습니다"

    with allure.step("4. 상위 3개 상품 검증"):
        top_3 = results[:3]
        for i, product in enumerate(top_3, 1):
            logger.info(f"상위 {i}위: {product}")
            # 상위 3개는 반드시 키워드 포함해야 함
            assert keyword.lower() in product.lower(), \
                f"상위 {i}위 상품이 '{keyword}'를 포함하지 않음: {product}"

    with allure.step("5. 스크린샷 저장"):
        search_page.take_screenshot(f"search_{keyword}.png")
```

---

## 📊 검증 전략 비교

| 방법 | 엄격도 | 실용성 | 추천 사용처 |
|------|--------|--------|------------|
| **100% 일치** | ⭐⭐⭐⭐⭐ | ⭐ | 테스트 환경만 |
| **70% 일치** | ⭐⭐⭐ | ⭐⭐⭐⭐ | **실무 추천** |
| **유사도 기반** | ⭐⭐ | ⭐⭐⭐ | 오타 허용 필요 시 |
| **상위 N개만** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | **포트폴리오 추천** |

---

## ✅ 체크리스트

### SearchPage 구현
- [ ] `get_search_results()` 메서드 추가
- [ ] `verify_search_results_contain_keyword()` 메서드 추가
- [ ] `verify_search_results_relevance()` 메서드 추가
- [ ] 검색 입력/버튼 Locator 추가

### 테스트 작성
- [ ] 기본 검색 테스트
- [ ] 일치율 기반 검증 테스트
- [ ] 네거티브 케이스 (검색 결과 없음)

---

**작성일:** 2025-12-24
**추천:** 70% 일치율 + 상위 3개 필수 포함 방식
