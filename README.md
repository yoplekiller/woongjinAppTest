# Appium 모바일 앱 테스트 자동화

**한국어** | [English](./README.en.md)

[![Appium](https://img.shields.io/badge/Appium-663399?style=for-the-badge&logo=appium&logoColor=white)](https://appium.io/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://pytest.org/)

> 웅진마켓 Android 앱 E2E 테스트 자동화 프로젝트

---

## 프로젝트 소개

QA 엔지니어 포트폴리오 프로젝트입니다. Python + Appium 기반으로 실제 운영 중인 웅진마켓 Android 앱을 대상으로 모바일 테스트 자동화를 구현했습니다.

### 주요 특징

| 특징 | 설명 |
|------|------|
| **Page Object Model** | 6개 페이지 클래스로 구조화 |
| **이미지 검증** | 엑박(깨진 이미지) 자동 탐지 |
| **자동 스크린샷** | 실패 시 스크린샷 + 페이지 소스 저장 |
| **재시도 로직** | Flaky test 대응 (pytest-rerunfailures) |
| **로깅 시스템** | 파일 + 콘솔 중앙 로깅 |
| **Allure 리포트** | 시각적 테스트 결과 제공 |

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| Framework | Appium 2.x |
| Language | Python 3.11+ |
| Test Runner | Pytest 8.x |
| Reporting | Allure Report |
| Parallel | pytest-xdist |
| Retry | pytest-rerunfailures |

---

## 프로젝트 구조

```
woongjinAppTest/
├── src/
│   ├── config/
│   │   └── app_config.py          # 앱 설정 (드라이버, 타임아웃)
│   │
│   ├── pages/                     # Page Object Model
│   │   ├── base_page.py           # 공통 메서드
│   │   ├── woongjin_app_home_page.py
│   │   ├── woongjin_app_category_page.py
│   │   ├── woongjin_app_search_page.py
│   │   ├── woongjin_app_login_page.py
│   │   ├── woongjin_app_like_page.py
│   │   └── woongjin_app_my_tab.py
│   │
│   ├── tests/                     # 테스트 케이스 (10개 파일)
│   │   ├── test_home.py           # 홈 페이지 (로딩, 스크롤, 이미지)
│   │   ├── test_category.py       # 카테고리 페이지
│   │   ├── test_search.py         # 검색 기능
│   │   ├── test_login.py          # 로그인 (정상)
│   │   ├── test_login_negative.py # 로그인 (실패 케이스)
│   │   ├── test_my_tab.py         # 마이탭 페이지
│   │   ├── test_gnb_tab.py        # GNB 탭 네비게이션
│   │   ├── test_navigation.py     # 전체 네비게이션 통합
│   │   └── test_image_validation.py # 이미지 엑박 검증
│   │
│   ├── utils/
│   │   ├── popup_handler.py       # 팝업 자동 처리
│   │   ├── page_source_helper.py  # 페이지 소스 분석
│   │   ├── logger.py              # 로깅 시스템
│   │   └── exceptions.py          # 커스텀 예외
│   │
│   └── conftest.py                # Pytest 픽스처
│
├── docs/                          # 문서
├── requirements.txt
└── pytest.ini
```

---

## 설치 및 실행

```bash
# 저장소 클론
git clone https://github.com/YopleKiller/woongjinAppTest.git
cd woongjinAppTest

# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt

# Appium 서버 실행 (별도 터미널)
appium

# 테스트 실행
pytest src/tests/ --reruns 1 -v
```

### 환경변수 (.env)

```env
APPIUM_SERVER_URL=http://127.0.0.1:4723
DEVICE_NAME=your_device_name
```

---

## 테스트 케이스 (10개 파일, 15+ 테스트)

| 테스트 | 검증 내용 |
|--------|-----------|
| `test_home` | 홈 페이지 로딩, 스크롤, 이미지 검증 |
| `test_category` | 카테고리 진입, 홈 복귀 |
| `test_search` | 상품 검색 기능 |
| `test_login` | 정상 로그인 플로우 |
| `test_login_negative` | 로그인 실패 케이스 (잘못된 비밀번호 등) |
| `test_my_tab` | 마이탭 진입 (로그인/비로그인) |
| `test_gnb_tab` | GNB 탭 개별 네비게이션 |
| `test_navigation` | 전체 GNB 순회, 빠른 탭 전환 |
| `test_image_validation` | 앱 내 이미지 엑박 자동 탐지 |

---

## 주요 구현

### Page Object Model

```
BasePage (공통: find_element, click, swipe, take_screenshot, find_broken_images)
  ├── WoongjinAppHomePage      홈 화면
  ├── WoongjinAppCategoryPage  카테고리
  ├── WoongjinAppSearchPage    검색
  ├── WoongjinAppLoginPage     로그인
  ├── WoongjinAppLikePage      찜
  └── WoongjinAppMyTab         MY 탭
```

### 이미지 엑박 검증

```python
def test_check_broken_images(home_page):
    broken_images = home_page.find_broken_images()
    report_path, broken = home_page.save_broken_images_report("report.txt")
    assert len(broken_images) == 0, f"깨진 이미지 {len(broken_images)}개 발견"
```

**검증 원리:**
1. 모든 `ImageView` 요소 탐색
2. width/height가 1px 이하면 엑박으로 판단
3. resource-id, bounds 정보 수집
4. 리포트 파일 저장

### 팝업 자동 처리

```python
# utils/popup_handler.py
def handle_woongjin_popups(driver):
    """앱 실행 시 나타나는 팝업 자동 닫기"""
```

---

## 실패 시 자동 캡처

테스트 실패 시 자동으로 저장:
- `screenshots/` - 스크린샷
- `page_sources/` - 페이지 소스 XML

---

## 배운 점

- **Appium**: 모바일 앱 자동화, 요소 탐색 전략 (xpath, accessibility id, resource-id)
- **이미지 검증**: 엑박 탐지 로직 구현, 실무에서 활용 가능한 품질 검증
- **안정성**: 재시도 로직, 팝업 처리로 Flaky test 감소
- **디버깅**: 페이지 소스 분석을 통한 요소 탐색

---

## 관련 프로젝트

- [QATEST](https://github.com/yoplekiller/QATEST) - Python/Selenium Web + API 테스트
- [PlaywrightQA](https://github.com/yoplekiller/PlaywrightQA) - TypeScript/Playwright Web 테스트

---

## 작성자

**LIM JAE MIN**
- GitHub: [@YopleKiller](https://github.com/YopleKiller)
- Email: jmlim9244@gmail.com

---

## License

MIT License
