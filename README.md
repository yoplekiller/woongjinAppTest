# Appium 모바일 앱 테스트 프로젝트 (실무용)

웅진마켓 Android 앱 자동화 테스트 프로젝트입니다.

## 🌟 주요 기능 (실무용)

- ✅ Page Object Model 패턴
- ✅ **이미지 엑박 자동 검증** (상세 로깅)
- ✅ **실패 시 자동 스크린샷 + 페이지 소스 저장**
- ✅ **재시도 로직** (Flaky test 대응)
- ✅ **중앙 로깅 시스템** (파일 + 콘솔)
- ✅ 병렬 실행 지원 (pytest-xdist)
- ✅ Allure 리포트
- ✅ 커스텀 Exception
- ✅ 모듈화된 구조

## 빠른 시작

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. Appium 서버 실행
appium

# 3. 테스트 실행 (재시도 포함)
pytest src/tests/ --reruns 1 -v

# 4. 이미지 검증
pytest src/tests/test_image_validation.py -v
```

**📖 상세 가이드:** [TESTING_GUIDE.md](TESTING_GUIDE.md)

## 프로젝트 구조

```
Project/
├── src/
│   ├── config/                  # 설정 파일
│   │   ├── __init__.py
│   │   └── app_config.py       # 앱 설정 (드라이버, 타임아웃 등)
│   │
│   ├── pages/                   # Page Object 패턴
│   │   ├── __init__.py
│   │   ├── base_page.py        # 기본 페이지 클래스 (공통 메서드)
│   │   └── woongjin_app_home_page.py  # 웅진마켓 홈 페이지
│   │
│   ├── utils/                   # 유틸리티 함수
│   │   ├── __init__.py
│   │   ├── popup_handler.py    # 팝업 처리
│   │   └── page_source_helper.py  # 페이지 소스 저장/분석
│   │
│   ├── tests/                   # 테스트 케이스
│   │   ├── __init__.py
│   │   ├── test_woongjin_refactored.py   # 주요 기능 테스트
│   │   ├── test_gnb_tab.py               # GNB 탭 테스트
│   │   ├── test_image_validation.py      # 이미지 검증 테스트
│   │   ├── test_woongjin_extract_source.py  # 소스 추출 테스트
│   │   └── test_asdf.py                  # 디버깅 테스트
│   │
│   └── conftest.py              # pytest 픽스처 설정
│
├── screenshots/                 # 스크린샷 저장 폴더
├── page_sources/                # 페이지 소스 저장 폴더
├── allure-results/              # Allure 리포트 결과
├── requirements.txt             # Python 패키지 의존성
└── pytest.ini                   # pytest 설정

```

## 설치 및 실행

### 1. 환경 설정

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. Appium 서버 실행

```bash
appium
```

### 3. 테스트 실행

```bash
# 전체 테스트 실행
pytest src/tests/ -v

# 특정 테스트 파일 실행
pytest src/tests/test_woongjin_refactored.py -v

# 이미지 검증 테스트만 실행
pytest src/tests/test_image_validation.py -v

# Allure 리포트와 함께 실행
pytest src/tests/ -v --alluredir=allure-results
allure serve allure-results
```

## 주요 클래스 및 메서드

### BasePage

모든 페이지의 기본 클래스입니다.

**주요 메서드:**
- `find_element(locator, timeout)`: 요소 찾기
- `click(locator, timeout)`: 요소 클릭
- `swipe_up()`, `swipe_down()`: 스와이프
- `take_screenshot(name)`: 스크린샷 저장
- `check_image_loaded(image_locator)`: 이미지 로딩 확인
- `find_broken_images()`: 모든 깨진 이미지 찾기
- `save_broken_images_report(filename)`: 깨진 이미지 리포트 저장

### WoongjinAppHomePage

웅진마켓 앱 홈페이지 Page Object입니다.

**주요 메서드:**
- `click_search()`: 검색 버튼 클릭
- `click_category_tab()`: 카테고리 탭 클릭
- `click_like_tab()`: 찜 탭 클릭
- `click_home_tab()`: 홈 탭 클릭
- `click_my_page_tab()`: MY 탭 클릭
- `click_lowest_price()`: 최저가도전 클릭

## 이미지 검증 기능

앱에서 깨진 이미지(엑박)를 자동으로 찾아냅니다.

### 사용 예시

```python
def test_check_broken_images(home_page):
    # 현재 페이지의 모든 깨진 이미지 찾기
    broken_images = home_page.find_broken_images()

    # 리포트 저장
    report_path, broken_images = home_page.save_broken_images_report(
        "home_broken_images_report.txt"
    )

    # 검증
    assert len(broken_images) == 0, f"깨진 이미지 {len(broken_images)}개 발견!"
```

### 이미지 검증 원리

1. 모든 `ImageView` 요소를 찾음
2. 각 이미지의 크기(`width`, `height`) 확인
3. 크기가 1px 이하면 깨진 이미지로 판단
4. `resource-id`, `bounds` 등 정보 수집
5. 리포트 파일로 저장

## 설정 관리

`src/config/app_config.py`에서 설정을 중앙 관리합니다.

```python
class AppConfig:
    APPIUM_SERVER_URL = "http://127.0.0.1:4723"
    DEFAULT_TIMEOUT = 10
    SCREENSHOT_DIR = "./screenshots"
    # ...
```

## 유틸리티 함수

### popup_handler.py
- `handle_woongjin_popups(driver)`: 웅진마켓 앱 초기 팝업 자동 처리

### page_source_helper.py
- `save_page_source(driver, filename)`: 페이지 소스 XML 저장
- `print_all_elements(driver)`: 모든 요소 정보 출력
- `print_elements_with_content_desc(driver)`: content-desc가 있는 요소 출력
- `print_elements_with_text(driver)`: text가 있는 요소 출력

## 테스트 작성 가이드

### 1. 기본 테스트 작성

```python
def test_example(home_page):
    """테스트 설명"""
    with allure.step("단계 설명"):
        home_page.click_category_tab()

    with allure.step("검증"):
        home_page.take_screenshot("example")
```

### 2. 이미지 검증 테스트

```python
def test_check_images(home_page):
    """이미지 검증"""
    report_path, broken_images = home_page.save_broken_images_report()
    assert len(broken_images) == 0
```

## 문제 해결

### Appium 연결 실패
- Appium 서버가 실행 중인지 확인
- 디바이스가 연결되어 있는지 확인 (`adb devices`)
- `app_config.py`의 `deviceName` 확인

### 요소를 찾을 수 없음
- `test_asdf.py`의 `test_find_element_multiple_ways` 실행
- 페이지 소스 확인: `pytest src/tests/test_woongjin_extract_source.py`
- `page_sources/` 폴더의 XML 파일 확인

## 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.

## 라이선스

MIT License
