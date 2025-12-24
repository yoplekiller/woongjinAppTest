# 실무용 테스트 실행 가이드

## 빠른 시작

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. Appium 서버 실행
```bash
appium
```

### 3. 기본 테스트 실행
```bash
# 전체 테스트 (로그 포함)
pytest src/tests/ -v

# 이미지 검증만
pytest src/tests/test_image_validation.py -v

# 특정 테스트만
pytest src/tests/test_woongjin_refactored.py::test_woongjin_home_page_load -v
```

## 실무 기능

### 🔁 재시도 (Flaky Test 대응)

```bash
# 실패 시 2번 재시도
pytest src/tests/ --reruns 2

# 재시도 간 1초 대기
pytest src/tests/ --reruns 2 --reruns-delay 1
```

**코드에서 사용:**
```python
import pytest

@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_unstable_feature(home_page):
    """네트워크 이슈로 불안정한 테스트"""
    home_page.click_search()
```

### 📸 실패 시 자동 캡처

테스트 실패 시 자동으로 저장됩니다:
- **스크린샷**: `screenshots/FAILED_테스트명_시간.png`
- **페이지 소스**: `page_sources/FAILED_테스트명_시간.xml`
- **현재 액티비티 정보**: 로그에 기록

### 📝 로깅

**로그 파일 위치:**
- 전체 로그: `logs/test_YYYYMMDD_HHMMSS.log`
- 에러만: `logs/error_YYYYMMDD_HHMMSS.log`
- pytest 로그: `logs/pytest.log`

**로그 레벨:**
```python
from utils.logger import get_logger

logger = get_logger(__name__)

logger.debug("상세 디버그 정보")
logger.info("일반 정보")
logger.warning("경고")
logger.error("에러")
```

### 🚀 병렬 실행 (시간 단축)

```bash
# 2개 프로세스로 병렬 실행
pytest src/tests/ -n 2

# CPU 코어 수만큼 자동 병렬
pytest src/tests/ -n auto
```

**주의:** 디바이스가 2개 이상 연결되어야 병렬 실행 가능!

## 이미지 검증 테스트

### 기본 실행
```bash
pytest src/tests/test_image_validation.py -v
```

### 마커로 실행
```bash
# 이미지 검증 테스트만
pytest -m image_validation -v
```

### 리포트 확인
```
screenshots/
├── home_broken_images_report.txt
├── category_broken_images_report.txt
└── ...
```

## Allure 리포트

```bash
# 1. Allure 결과 생성
pytest src/tests/ --alluredir=allure-results

# 2. 리포트 확인
allure serve allure-results
```

브라우저에서 자동으로 열립니다.

## 로그 확인 방법

### 실시간 로그 보기
```bash
# 콘솔에 INFO 레벨 이상 출력
pytest src/tests/ -v --log-cli-level=INFO

# DEBUG 레벨까지 모두 출력
pytest src/tests/ -v --log-cli-level=DEBUG
```

### 테스트 후 로그 파일 확인
```bash
# 최신 로그 파일
ls -lt logs/

# 에러 로그만 보기
tail -f logs/error_*.log
```

## 문제 해결

### ❌ 테스트가 바로 종료됨

**원인:** 팝업 처리 실패 또는 페이지 로딩 전 테스트 종료

**해결:**
1. 로그 확인: `logs/test_*.log`
2. 실패 스크린샷 확인: `screenshots/FAILED_*.png`
3. 팝업 처리 로직 확인

### ❌ 이미지가 0개로 나옴

**원인:** 페이지 로딩 전에 이미지 검증

**해결:**
```python
# wait_for_load=True로 3초 대기
broken_images = home_page.find_broken_images(wait_for_load=True)
```

### ❌ Element not found

**원인:** Locator 변경 또는 타이밍 이슈

**해결:**
1. 페이지 소스 확인: `pytest src/tests/test_woongjin_extract_source.py`
2. XML 파일에서 정확한 locator 확인: `page_sources/`
3. 대기 시간 증가 또는 재시도 사용

### ❌ Appium 연결 실패

**체크리스트:**
```bash
# 1. Appium 서버 실행 확인
ps aux | grep appium

# 2. 디바이스 연결 확인
adb devices

# 3. 앱 패키지명 확인
adb shell pm list packages | grep woongjin
```

## 모범 사례

### ✅ 테스트 작성 시

```python
import pytest
from utils.logger import get_logger
import allure

logger = get_logger(__name__)


@pytest.mark.flaky(reruns=2)  # 불안정하면 재시도
def test_example(home_page):
    """테스트 설명 작성"""

    logger.info("테스트 시작: 검색 기능")

    with allure.step("검색 버튼 클릭"):
        home_page.click_search()

    with allure.step("검색 페이지 로딩 확인"):
        assert home_page.is_element_visible(locator)

    logger.info("테스트 성공")
```

### ✅ Page Object 작성 시

```python
from utils.logger import get_logger
from utils.exceptions import ElementNotFoundError

logger = get_logger(__name__)


class MyPage(BasePage):

    def click_button(self):
        logger.info("버튼 클릭 시도")
        try:
            self.click(self.BUTTON_LOCATOR)
            logger.info("버튼 클릭 성공")
        except TimeoutException:
            logger.error("버튼을 찾을 수 없음")
            raise ElementNotFoundError(self.BUTTON_LOCATOR)
```

## CI/CD 통합

### GitHub Actions 예시
```yaml
name: Mobile Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.14'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest src/tests/ --reruns 2 --alluredir=allure-results
      - name: Upload Allure results
        uses: actions/upload-artifact@v2
        with:
          name: allure-results
          path: allure-results
```

## 성능 팁

### 병렬 실행
```bash
# 빠르게: 여러 디바이스에서 동시 실행
pytest src/tests/ -n 4 --dist loadgroup
```

### 실패한 테스트만 재실행
```bash
# 1. 첫 실행
pytest src/tests/ --lf

# 2. 실패한 것만 다시
pytest --lf
```

### 특정 마커만 실행
```bash
# 빠른 테스트만
pytest -m "not slow" -v

# 이미지 검증 제외
pytest -m "not image_validation" -v
```

## 디버깅

### 상세 로그로 실행
```bash
pytest src/tests/test_image_validation.py -v -s --log-cli-level=DEBUG
```

### 브레이크포인트 사용
```python
def test_debug(home_page):
    home_page.click_search()
    import pdb; pdb.set_trace()  # 여기서 멈춤
    # 디버깅...
```

### 페이지 소스 덤프
```python
from utils.page_source_helper import save_page_source

def test_debug(driver):
    save_page_source(driver, "debug_screen.xml")
    # page_sources/debug_screen.xml 확인
```

## 요약

**매일 실행:**
```bash
pytest src/tests/ --reruns 1 -v
```

**릴리즈 전:**
```bash
pytest src/tests/ --reruns 2 -n auto --alluredir=allure-results
allure serve allure-results
```

**문제 발생 시:**
1. `logs/` 폴더 확인
2. `screenshots/FAILED_*.png` 확인
3. `page_sources/FAILED_*.xml` 확인
4. DEBUG 모드로 재실행
