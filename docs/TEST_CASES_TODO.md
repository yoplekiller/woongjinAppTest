# 추가해야 할 테스트 케이스 목록

## 📊 현황
- **현재 테스트 케이스:** 5개
- **목표 테스트 케이스:** 16개
- **추가 필요:** 11개

---

## ✅ 현재 존재하는 테스트 (5개)

### test_gnb_tab.py (3개)
- `test_category_tab()` - 카테고리 탭 클릭 → 화면 노출 확인
- `test_search_tab()` - 검색 탭 클릭 → 화면 노출 확인
- `test_like_tab()` - 찜 탭 클릭 → 로그인 → 찜 화면 확인

### test_image_validation.py (1개)
- `test_check_broken_images_on_home()` - 홈 화면 이미지 검증

### test_login.py (1개)
- `test_login()` - 로그인 성공 케이스

---

## 🔴 추가해야 할 테스트 (11개)

### 1. 네거티브 로그인 테스트 (3개)
**파일명:** `src/tests/test_login_negative.py`

#### 1.1 `test_login_with_wrong_password()`
```python
def test_login_with_wrong_password(login_page, test_user_credentials):
    """잘못된 비밀번호 입력 → 에러 메시지 확인"""
```

**테스트 단계:**
1. 로그인 페이지 이동
2. 올바른 이메일 + 잘못된 비밀번호 입력
3. 로그인 버튼 클릭
4. **검증:** 에러 메시지 노출 확인
5. **검증:** 로그인 실패 (홈 화면 이동 안 됨)
6. 스크린샷 저장

**필요한 요소:**
- 에러 메시지 텍스트 또는 팝업

---

#### 1.2 `test_login_with_empty_email()`
```python
def test_login_with_empty_email(login_page):
    """이메일 미입력 → 에러 메시지 확인"""
```

**테스트 단계:**
1. 로그인 페이지 이동
2. 이메일 필드 비우기
3. 비밀번호만 입력
4. 로그인 버튼 클릭
5. **검증:** "이메일을 입력하세요" 메시지 확인
6. **검증:** 로그인 버튼 비활성화 또는 에러
7. 스크린샷 저장

**필요한 요소:**
- 이메일 필드 유효성 검사 메시지

---

#### 1.3 `test_login_with_empty_password()`
```python
def test_login_with_empty_password(login_page, test_user_credentials):
    """비밀번호 미입력 → 에러 메시지 확인"""
```

**테스트 단계:**
1. 로그인 페이지 이동
2. 이메일만 입력
3. 비밀번호 필드 비우기
4. 로그인 버튼 클릭
5. **검증:** "비밀번호를 입력하세요" 메시지 확인
6. **검증:** 로그인 실패
7. 스크린샷 저장

**필요한 요소:**
- 비밀번호 필드 유효성 검사 메시지

---

### 2. 검색 기능 테스트 (3개)
**파일명:** `src/tests/test_search.py`

**필요한 페이지 객체:** `SearchPage` (pages 폴더에 추가 필요)

#### 2.1 `test_search_with_valid_keyword()`
```python
def test_search_with_valid_keyword(home_page, search_page):
    """정상 검색 → 결과 노출"""
```

**테스트 단계:**
1. 홈 화면에서 검색 탭 클릭
2. 검색어 입력 (예: "책", "동화책")
3. 검색 버튼 클릭 또는 엔터
4. **검증:** 검색 결과 리스트 노출
5. **검증:** 최소 1개 이상 상품 존재
6. **검증:** 검색어가 상품명에 포함되는지
7. 스크린샷 저장

**필요한 요소:**
- 검색 입력 필드
- 검색 버튼
- 검색 결과 리스트

---

#### 2.2 `test_search_no_results()`
```python
def test_search_no_results(home_page, search_page):
    """존재하지 않는 키워드 검색 → '결과 없음' 메시지"""
```

**테스트 단계:**
1. 홈 화면에서 검색 탭 클릭
2. 존재하지 않는 키워드 입력 (예: "zxcvbnmasdfghjkl123")
3. 검색 실행
4. **검증:** "검색 결과가 없습니다" 메시지 확인
5. **검증:** 빈 리스트 또는 안내 메시지
6. **검증:** 앱 크래시 없음
7. 스크린샷 저장

**필요한 요소:**
- "결과 없음" 메시지 텍스트

---

#### 2.3 `test_search_with_special_characters()`
```python
def test_search_with_special_characters(home_page, search_page):
    """특수문자 입력 → 에러 없이 처리"""
```

**테스트 단계:**
1. 홈 화면에서 검색 탭 클릭
2. 특수문자 입력 (예: "!@#$%^&*()")
3. 검색 실행
4. **검증:** 앱 크래시 없음
5. **검증:** 결과 없음 또는 정상 처리
6. **검증:** 에러 메시지 노출되지 않음
7. 스크린샷 저장

**필요한 요소:**
- 특수문자 처리 로직

---

### 3. 상품 관련 테스트 (3개)
**파일명:** `src/tests/test_product.py`

**필요한 페이지 객체:** `ProductPage` (pages 폴더에 추가 필요)

#### 3.1 `test_product_price_is_positive()`
```python
def test_product_price_is_positive(home_page):
    """홈 화면 모든 상품 가격 > 0 확인"""
```

**테스트 단계:**
1. 홈 화면 이동
2. 화면에 노출된 모든 상품 리스트 추출
3. 각 상품의 가격 텍스트 파싱
4. **검증:** 모든 가격이 0보다 큰지 확인
5. **검증:** 가격 형식 확인 (숫자, 콤마 포함)
6. **검증:** 음수 가격 없음
7. 스크린샷 저장

**필요한 요소:**
- 상품 가격 텍스트 요소
- 가격 파싱 로직 (BasePage 또는 utils에 추가)

---

#### 3.2 `test_product_has_valid_image()`
```python
def test_product_has_valid_image(home_page):
    """상품 이미지 로드 확인"""
```

**테스트 단계:**
1. 홈 화면 이동
2. 첫 번째 상품의 ImageView 요소 찾기
3. **검증:** ImageView 크기 확인 (width > 1px, height > 1px)
4. **검증:** 엑박(broken image) 아님
5. 스크린샷 저장

**필요한 요소:**
- 상품 이미지 ImageView
- find_broken_images() 메서드 재사용

---

#### 3.3 `test_product_detail_navigation()`
```python
def test_product_detail_navigation(home_page, product_page):
    """상품 클릭 → 상세 페이지 이동"""
```

**테스트 단계:**
1. 홈 화면 이동
2. 첫 번째 상품 클릭
3. **검증:** 상세 페이지 노출 확인
4. **검증:** 상품명 존재
5. **검증:** 가격 존재
6. **검증:** 상품 이미지 존재
7. 스크린샷 저장

**필요한 요소:**
- 상품 클릭 가능한 요소
- 상세 페이지 식별 요소 (title, price 등)

---

### 4. 에러 핸들링 테스트 (2개)
**파일명:** `src/tests/test_error_handling.py`

#### 4.1 `test_handle_network_timeout()`
```python
def test_handle_network_timeout(driver, home_page):
    """네트워크 타임아웃 시 에러 메시지"""
```

**테스트 단계:**
1. 홈 화면 이동
2. 네트워크 차단 (비행기 모드 활성화)
   - `driver.set_network_connection(0)` 사용
3. 화면 새로고침 또는 다른 페이지 이동 시도
4. **검증:** "네트워크 연결을 확인하세요" 메시지
5. **검증:** 앱 크래시 없음
6. 네트워크 복구
7. 스크린샷 저장

**필요한 요소:**
- 네트워크 에러 메시지

**주의사항:**
- 테스트 후 반드시 네트워크 복구

---

#### 4.2 `test_handle_invalid_screen()`
```python
def test_handle_invalid_screen(home_page, login_page):
    """비로그인 상태에서 로그인 필요 페이지 접근 → 처리 확인"""
```

**테스트 단계:**
1. 로그아웃 상태 확인 (필요시 로그아웃)
2. 찜 탭 클릭 (로그인 필요 기능)
3. **검증:** 로그인 페이지로 리다이렉트 또는
4. **검증:** "로그인이 필요합니다" 메시지
5. **검증:** 앱 크래시 없음
6. 스크린샷 저장

**필요한 요소:**
- 로그아웃 기능
- 로그인 유도 메시지 또는 페이지

---

## 📁 추가 필요한 파일 및 코드

### 1. 새로운 테스트 파일 (4개)
```
src/tests/
├── test_login_negative.py     (신규)
├── test_search.py              (신규)
├── test_product.py             (신규)
└── test_error_handling.py      (신규)
```

### 2. 새로운 페이지 객체 (2개)
```
src/pages/
├── search_page.py              (신규)
└── product_page.py             (신규)
```

### 3. conftest.py에 추가할 fixture
```python
@pytest.fixture
def search_page(driver):
    from src.pages.search_page import SearchPage
    return SearchPage(driver)

@pytest.fixture
def product_page(driver):
    from src.pages.product_page import ProductPage
    return ProductPage(driver)

@pytest.fixture
def invalid_credentials():
    return {
        "user_id": os.getenv("TEST_USER_ID"),
        "wrong_password": "wrongpassword123"
    }
```

---

## 🎯 작업 체크리스트

### Phase 1: 페이지 객체 생성
- [ ] `SearchPage` 클래스 작성
  - [ ] 검색 입력 필드 locator
  - [ ] 검색 버튼 locator
  - [ ] 검색 결과 리스트 locator
  - [ ] "결과 없음" 메시지 locator
- [ ] `ProductPage` 클래스 작성
  - [ ] 상품명 locator
  - [ ] 가격 locator
  - [ ] 이미지 locator
  - [ ] 상세 페이지 확인 메서드

### Phase 2: conftest.py 업데이트
- [ ] `search_page` fixture 추가
- [ ] `product_page` fixture 추가
- [ ] `invalid_credentials` fixture 추가

### Phase 3: 테스트 케이스 작성
- [ ] **test_login_negative.py (3개)**
  - [ ] test_login_with_wrong_password
  - [ ] test_login_with_empty_email
  - [ ] test_login_with_empty_password
- [ ] **test_search.py (3개)**
  - [ ] test_search_with_valid_keyword
  - [ ] test_search_no_results
  - [ ] test_search_with_special_characters
- [ ] **test_product.py (3개)**
  - [ ] test_product_price_is_positive
  - [ ] test_product_has_valid_image
  - [ ] test_product_detail_navigation
- [ ] **test_error_handling.py (2개)**
  - [ ] test_handle_network_timeout
  - [ ] test_handle_invalid_screen

### Phase 4: 테스트 실행 및 검증
- [ ] 전체 테스트 실행: `pytest src/tests/`
- [ ] 실패한 테스트 디버깅
- [ ] Allure 리포트 생성: `pytest --alluredir=allure-results`
- [ ] 리포트 확인: `allure serve allure-results`

---

## 📊 테스트 작성 후 예상 결과

| 항목 | 현재 | 추가 후 |
|------|------|---------|
| **총 테스트 케이스** | 5개 | 16개 |
| **긍정 케이스 (Happy Path)** | 5개 | 8개 |
| **부정 케이스 (Negative)** | 0개 | 5개 |
| **경계값/에러 케이스** | 0개 | 3개 |
| **포트폴리오 적합성** | ❌ 부족 | ✅ 충분 |
| **프로젝트 평점** | 7.5/10 | 8.5/10 |

---

## 💡 테스트 작성 시 주의사항

### 1. Allure 어노테이션 사용
```python
import allure

@allure.feature("로그인")
@allure.story("네거티브 테스트")
@allure.severity(allure.severity_level.CRITICAL)
def test_login_with_wrong_password():
    with allure.step("잘못된 비밀번호로 로그인 시도"):
        # 테스트 코드
    with allure.step("에러 메시지 확인"):
        # 검증 코드
```

### 2. Assertion 메시지 명확하게
```python
assert element.is_displayed(), "에러 메시지가 노출되지 않음"
assert len(results) > 0, f"검색 결과가 0개입니다. 기대값: 1개 이상"
```

### 3. 스크린샷 필수
```python
# 테스트 마지막에 항상 추가
page.take_screenshot("test_name.png")
```

### 4. 예외 처리
```python
try:
    element = driver.find_element(...)
except NoSuchElementException:
    logger.error("요소를 찾을 수 없음")
    pytest.fail("필수 요소가 화면에 없습니다")
```

---

## 📝 참고 자료

### 기존 코드 참고
- `test_login.py` - 로그인 테스트 구조 참고
- `test_gnb_tab.py` - 탭 전환 테스트 참고
- `base_page.py` - 공통 메서드 활용

### Locator 찾기
- Appium Inspector 사용
- `test_woongjin_extract_source.py` 참고 (페이지 소스 추출)

---

**작성일:** 2025-12-24
**예상 작업 시간:** 6-8시간
**우선순위:** 포트폴리오 완성을 위한 필수 작업
