# test_login_negative.py 코드 리뷰

**평가일:** 2025-12-24
**파일:** `src/tests/test_login_negative.py`
**리뷰어:** Claude Code

---

## 📊 종합 평가

| 항목 | 점수 | 설명 |
|------|------|------|
| **테스트 설계** | 9/10 | 네거티브 케이스 3개 적절히 선정 |
| **코드 구조** | 8/10 | Allure step 활용 우수 |
| **실행 가능성** | 3/10 | 🔴 **치명적 문제 발견** |
| **문서화** | 8/10 | Docstring 명확함 |
| **유지보수성** | 6/10 | 코드 중복 존재 |

### **총점: 6.8/10** ⚠️ 수정 필요

---

## ✅ 잘한 점

### 1. 네거티브 테스트 케이스 선정 ⭐⭐⭐⭐⭐
```python
✓ test_login_wrong_password      # 잘못된 비밀번호
✓ test_login_invalid_account     # 존재하지 않는 계정
✓ test_login_empty_fields         # 빈 입력 필드
```

**강점:**
- 실무에서 가장 중요한 네거티브 케이스 3개 선정
- 각 케이스가 명확하게 구분됨
- 포트폴리오에 적합한 선택

---

### 2. Allure Step 활용 우수 ⭐⭐⭐⭐⭐
```python
with allure.step("로그인 페이지 열기"):
    home_page.click_like_tab()
    assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"
```

**강점:**
- 각 단계별 명확한 분리
- 실패 시 어느 단계에서 실패했는지 즉시 파악 가능
- Allure 리포트에서 시각적으로 보기 좋음

---

### 3. Assertion 메시지 명확 ⭐⭐⭐⭐
```python
assert get_error_message == "아이디 또는 비밀번호를 확인해주세요!.", \
    f"예상 오류 메시지와 다름: {get_error_message}"
```

**강점:**
- 실패 시 예상값과 실제값 모두 표시
- 디버깅 시간 단축
- f-string 활용으로 가독성 향상

---

### 4. Docstring 작성 ⭐⭐⭐⭐
```python
def test_login_wrong_password(login_page, home_page, user_credentials, wrong_user_credentials):
    """로그인 - 잘못된 비밀번호 입력 시 오류 메시지 확인"""
```

**강점:**
- 각 테스트의 목적 명확
- 한글로 작성하여 이해 쉬움

---

## 🔴 치명적 문제

### 문제 1: Fixture 이름 불일치 (실행 불가!) 💥

**현재 코드:**
```python
# test_login_negative.py (5번째 줄)
def test_login_wrong_password(login_page, home_page, user_credentials, wrong_user_credentials):
    #                                              ^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^
    #                                              문제 발생!
```

**conftest.py:**
```python
@pytest.fixture(scope="function")
def test_user_credentials() -> dict:    # ← test_user_credentials
    return { ... }

@pytest.fixture(scope="function")
def wrong_user_credentials() -> dict:   # ← 이것만 일치
    return { ... }
```

**문제점:**
- `user_credentials` fixture가 정의되어 있지 않음
- **테스트 실행 시 에러 발생** (pytest fixture not found)

**해결 방법:**
```python
# 옵션 A: 테스트 파일 수정 (권장)
def test_login_wrong_password(login_page, home_page, test_user_credentials, wrong_user_credentials):
    valid_user = test_user_credentials["user_id"]  # ← 수정
    #            ^^^^^^^^^^^^^^^^^^^^^

# 옵션 B: conftest.py에 별칭 추가
@pytest.fixture(scope="function")
def user_credentials() -> dict:
    """test_user_credentials의 별칭"""
    return {
        "user_id": os.getenv("TEST_USER_ID"),
        "password": os.getenv("TEST_USER_PASSWORD")
    }
```

---

### 문제 2: 메서드 누락 (실행 불가!) 💥

**현재 코드:**
```python
# test_login_negative.py (22-24번째 줄)
login_page.enter_username(valid_user)      # ❌ 메서드 없음
login_page.enter_password(wrong_password)  # ❌ 메서드 없음
login_page.click_login_button()            # ❌ 메서드 없음
```

**login_page.py 확인 결과:**
```python
# woongjin_app_login_page.py
class WoongjinAppLoginPage(BasePage):
    def email_login(self, username: str, password: str) -> None:  # ← 이것만 있음
        # 통합 메서드
```

**문제점:**
- `enter_username()`, `enter_password()`, `click_login_button()` 메서드가 구현되어 있지 않음
- **AttributeError 발생 확실**

**해결 방법 A: LoginPage에 메서드 추가 (권장)**

**파일:** `src/pages/woongjin_app_login_page.py`

```python
def enter_username(self, username: str) -> None:
    """사용자 이름 입력"""
    self.click(self.ID_INPUT)
    self.input_text(self.ID_INPUT, username)

def enter_password(self, password: str) -> None:
    """비밀번호 입력"""
    self.click(self.PASSWORD_INPUT)
    self.input_text(self.PASSWORD_INPUT, password)

def click_login_button(self) -> None:
    """로그인 버튼 클릭"""
    self.driver.hide_keyboard()
    self.click(self.LOGIN_BUTTON)
```

**해결 방법 B: 테스트 코드 수정 (차선책)**

```python
# test_login_negative.py
with allure.step("잘못된 비밀번호로 로그인 시도"):
    # 기존 email_login 메서드 사용하되, 유효성 검사 우회 필요
    # (email_login에는 비밀번호 8자 이상 검증이 있음)

    # 직접 요소 조작
    login_page.click(login_page.ID_INPUT)
    login_page.input_text(login_page.ID_INPUT, valid_user)
    login_page.click(login_page.PASSWORD_INPUT)
    login_page.input_text(login_page.PASSWORD_INPUT, wrong_password)
    login_page.driver.hide_keyboard()
    login_page.click(login_page.LOGIN_BUTTON)
```

---

## ⚠️ 개선 필요 사항

### 1. 코드 중복 (DRY 원칙 위반)

**현재 상태:**
```python
# 3개 테스트에서 동일한 코드 반복
with allure.step("로그인 페이지 열기"):
    home_page.click_like_tab()
    assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"
    print("✅ 로그인 페이지 노출 확인")

with allure.step("이메일 로그인 페이지로 이동"):
    login_page.click_email_login()
    assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"
    print("✅ 이메일 로그인 페이지 노출 확인")
```

**문제점:**
- 같은 코드가 3번 반복됨
- 수정 시 3곳을 모두 수정해야 함

**개선 방법 A: Fixture 활용 (권장)**

**conftest.py에 추가:**
```python
@pytest.fixture
def navigate_to_email_login(home_page, login_page):
    """이메일 로그인 페이지로 이동하는 fixture"""
    with allure.step("로그인 페이지 열기"):
        home_page.click_like_tab()
        assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"

    with allure.step("이메일 로그인 페이지로 이동"):
        login_page.click_email_login()
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"

    return login_page
```

**test_login_negative.py 수정:**
```python
def test_login_wrong_password(navigate_to_email_login, test_user_credentials, wrong_user_credentials):
    """로그인 - 잘못된 비밀번호 입력 시 오류 메시지 확인"""
    login_page = navigate_to_email_login  # 이미 로그인 페이지로 이동됨

    with allure.step("잘못된 비밀번호로 로그인 시도"):
        # 로그인 시도...
```

**개선 방법 B: Helper 메서드 (차선책)**

```python
# test_login_negative.py 상단에 추가
def navigate_to_login_page(home_page, login_page):
    """로그인 페이지로 이동"""
    with allure.step("로그인 페이지 열기"):
        home_page.click_like_tab()
        assert login_page.is_login_page_visible()

    with allure.step("이메일 로그인 페이지로 이동"):
        login_page.click_email_login()
        assert login_page.email_login_page_is_visible()

# 각 테스트에서 호출
def test_login_wrong_password(...):
    navigate_to_login_page(home_page, login_page)
    # 이후 로직...
```

---

### 2. Print 문 사용 (비추천)

**현재 코드:**
```python
print("✅ 로그인 페이지 노출 확인")
print("✅ 이메일 로그인 페이지 노출 확인")
print("✅ 잘못된 비밀번호 오류 메시지 확인 완료")
```

**문제점:**
- pytest에서 print는 `-s` 옵션 없이는 보이지 않음
- Allure 리포트에 포함되지 않음
- 로깅 시스템과 분리됨

**개선 방법:**

```python
from utils.logger import get_logger

logger = get_logger(__name__)

with allure.step("로그인 페이지 열기"):
    home_page.click_like_tab()
    assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"
    logger.info("✅ 로그인 페이지 노출 확인")  # ← print 대신
```

**또는 Allure attach 사용:**
```python
with allure.step("로그인 페이지 열기"):
    home_page.click_like_tab()
    assert login_page.is_login_page_visible()
    allure.attach("로그인 페이지 노출됨", name="검증 결과", attachment_type=allure.attachment_type.TEXT)
```

---

### 3. 에러 메시지 하드코딩

**현재 코드:**
```python
assert get_error_message == "아이디 또는 비밀번호를 확인해주세요!.", \
    f"예상 오류 메시지와 다름: {get_error_message}"
```

**문제점:**
- 앱 업데이트 시 메시지 변경되면 테스트 실패
- 메시지가 여러 곳에 하드코딩됨

**개선 방법:**

**app_config.py 또는 별도 파일에 상수 정의:**
```python
# config/test_data.py
class ErrorMessages:
    INVALID_CREDENTIALS = "아이디 또는 비밀번호를 확인해주세요!."
    INVALID_ACCOUNT = "일치하는 계정 정보가 없습니다."
```

**테스트 코드:**
```python
from config.test_data import ErrorMessages

with allure.step("오류 메시지 확인"):
    get_error_message = login_page.get_error_message()
    assert get_error_message == ErrorMessages.INVALID_CREDENTIALS, \
        f"예상 오류 메시지와 다름: {get_error_message}"
```

---

### 4. 스크린샷 미저장

**현재 상태:**
- 테스트에서 스크린샷을 저장하지 않음
- 실패 시에만 자동 저장 (conftest.py의 hook)

**개선 방법:**

```python
with allure.step("오류 팝업 닫기"):
    login_page.close_error_popup()
    login_page.take_screenshot("login_wrong_password_error.png")  # ← 추가
    logger.info("✅ 잘못된 비밀번호 오류 메시지 확인 완료")
```

---

## 🎯 우선순위별 수정 사항

### 🔥 최우선 (테스트 실행 필수)

#### 1. Fixture 이름 수정
```python
# test_login_negative.py (전체 파일)

# 기존
def test_login_wrong_password(login_page, home_page, user_credentials, wrong_user_credentials):
    valid_user = user_credentials["user_id"]

# 수정
def test_login_wrong_password(login_page, home_page, test_user_credentials, wrong_user_credentials):
    valid_user = test_user_credentials["user_id"]

# test_login_invalid_account도 동일하게 수정
def test_login_invalid_account(login_page, home_page, wrong_user_credentials, test_user_credentials):
    valid_password = test_user_credentials["password"]
```

#### 2. LoginPage 메서드 추가

**파일:** `src/pages/woongjin_app_login_page.py`

```python
def enter_username(self, username: str) -> None:
    """사용자 이름 입력 (네거티브 테스트용)"""
    self.click(self.ID_INPUT)
    self.input_text(self.ID_INPUT, username)

def enter_password(self, password: str) -> None:
    """비밀번호 입력 (네거티브 테스트용)"""
    self.click(self.PASSWORD_INPUT)
    self.input_text(self.PASSWORD_INPUT, password)

def click_login_button(self) -> None:
    """로그인 버튼 클릭"""
    self.driver.hide_keyboard()
    self.click(self.LOGIN_BUTTON)
```

---

### ⚠️ 권장 (코드 품질 향상)

#### 3. 코드 중복 제거 (Fixture)

**conftest.py에 추가:**
```python
@pytest.fixture
def navigate_to_email_login(home_page, login_page):
    """이메일 로그인 페이지로 이동"""
    with allure.step("로그인 페이지 열기"):
        home_page.click_like_tab()
        assert login_page.is_login_page_visible(), "❌ 로그인 페이지가 보이지 않음"

    with allure.step("이메일 로그인 페이지로 이동"):
        login_page.click_email_login()
        assert login_page.email_login_page_is_visible(), "❌ 이메일 로그인 페이지가 보이지 않음"

    return login_page
```

#### 4. Print → Logger 변경

```python
from utils.logger import get_logger
logger = get_logger(__name__)

# print("✅ ...") → logger.info("✅ ...")
```

---

### 💡 선택 (추가 개선)

#### 5. 에러 메시지 상수화

**config/test_data.py 생성:**
```python
class ErrorMessages:
    INVALID_CREDENTIALS = "아이디 또는 비밀번호를 확인해주세요!."
    INVALID_ACCOUNT = "일치하는 계정 정보가 없습니다."
```

#### 6. 스크린샷 추가

```python
with allure.step("오류 팝업 닫기"):
    login_page.close_error_popup()
    login_page.take_screenshot("login_error.png")
```

---

## 📝 수정된 완성 코드 예시

```python
import allure
from utils.logger import get_logger

logger = get_logger(__name__)


def test_login_wrong_password(navigate_to_email_login, test_user_credentials, wrong_user_credentials):
    """로그인 - 잘못된 비밀번호 입력 시 오류 메시지 확인"""
    login_page = navigate_to_email_login
    valid_user = test_user_credentials["user_id"]
    wrong_password = wrong_user_credentials["password"]

    with allure.step("잘못된 비밀번호로 로그인 시도"):
        login_page.enter_username(valid_user)
        login_page.enter_password(wrong_password)
        login_page.click_login_button()

    with allure.step("오류 메시지 확인"):
        error_message = login_page.get_error_message()
        assert error_message == "아이디 또는 비밀번호를 확인해주세요!.", \
            f"예상 오류 메시지와 다름: {error_message}"
        logger.info(f"✅ 오류 메시지 확인: {error_message}")

    with allure.step("오류 팝업 닫기"):
        login_page.close_error_popup()
        login_page.take_screenshot("login_wrong_password.png")
        logger.info("✅ 잘못된 비밀번호 테스트 완료")


def test_login_invalid_account(navigate_to_email_login, wrong_user_credentials, test_user_credentials):
    """로그인 - 존재하지 않는 계정 입력 시 오류 메시지 확인"""
    login_page = navigate_to_email_login
    invalid_user = wrong_user_credentials["user_id"]
    valid_password = test_user_credentials["password"]

    with allure.step("존재하지 않는 계정으로 로그인 시도"):
        login_page.enter_username(invalid_user)
        login_page.enter_password(valid_password)
        login_page.click_login_button()

    with allure.step("오류 메시지 확인"):
        error_message = login_page.get_error_message()
        assert error_message == "일치하는 계정 정보가 없습니다.", \
            f"예상 오류 메시지와 다름: {error_message}"
        logger.info(f"✅ 오류 메시지 확인: {error_message}")

    with allure.step("오류 팝업 닫기"):
        login_page.close_error_popup()
        login_page.take_screenshot("login_invalid_account.png")
        logger.info("✅ 존재하지 않는 계정 테스트 완료")


def test_login_empty_fields(navigate_to_email_login):
    """로그인 - 빈 입력 필드로 로그인 시도 시 오류 메시지 확인"""
    login_page = navigate_to_email_login

    with allure.step("빈 입력 필드로 로그인 시도"):
        login_page.enter_username("")
        login_page.enter_password("")
        login_page.click_login_button()

    with allure.step("오류 메시지 확인"):
        error_message = login_page.get_error_message()
        assert error_message == "아이디 또는 비밀번호를 확인해주세요!.", \
            f"예상 오류 메시지와 다름: {error_message}"
        logger.info(f"✅ 오류 메시지 확인: {error_message}")

    with allure.step("오류 팝업 닫기"):
        login_page.close_error_popup()
        login_page.take_screenshot("login_empty_fields.png")
        logger.info("✅ 빈 입력 필드 테스트 완료")
```

---

## ✅ 수정 체크리스트

### 필수 (테스트 실행 가능하게)
- [ ] Fixture 이름 수정: `user_credentials` → `test_user_credentials`
- [ ] LoginPage에 메서드 추가:
  - [ ] `enter_username(username: str)`
  - [ ] `enter_password(password: str)`
  - [ ] `click_login_button()`

### 권장 (코드 품질)
- [ ] Fixture로 중복 코드 제거: `navigate_to_email_login`
- [ ] Print → Logger 변경
- [ ] 스크린샷 추가

### 선택 (추가 개선)
- [ ] 에러 메시지 상수화 (`config/test_data.py`)
- [ ] Allure attach 활용

---

## 🎓 최종 평가

### 긍정적 평가
**테스트 설계가 우수합니다!**
- 네거티브 케이스 3개 적절히 선정
- Allure step 활용 훌륭
- Assertion 메시지 명확

### 부정적 평가
**실행 불가능한 코드입니다!**
- Fixture 이름 불일치로 실행 안 됨
- 필요한 메서드가 구현되지 않음
- 코드 중복 많음

### 개선 후 예상 점수
**6.8/10 → 8.5/10** (수정 후)

---

## 🚀 다음 단계

1. **긴급:** LoginPage 메서드 구현 (30분)
2. **긴급:** Fixture 이름 수정 (5분)
3. **권장:** 코드 중복 제거 (20분)
4. **선택:** Logger, 상수화 등 추가 개선 (30분)

**예상 작업 시간:** 1-2시간

---

**리뷰 완료일:** 2025-12-24
**다음 리뷰 권장:** 수정 완료 후
