# Appium CI/CD 연동 가이드

## 🤔 문제 상황
**질문:** "Appium도 CI/CD 연동이 가능한가? 웹 테스트는 GitHub Actions에 넣으면 자동으로 돌아가는데, Appium은 기기가 필요하잖아?"

**답변:** ✅ 가능합니다! 하지만 웹 테스트보다 복잡합니다.

---

## 📱 Appium CI/CD 연동 방법 (4가지)

### 방법 비교표

| 방법 | 비용 | 난이도 | 실행 속도 | 포트폴리오 추천 |
|------|------|--------|-----------|----------------|
| **1. GitHub Actions + 에뮬레이터** | 무료 | 중간 | 느림 (10-15분) | ⭐⭐⭐⭐⭐ **추천** |
| **2. Self-hosted Runner** | 무료 | 높음 | 빠름 (3-5분) | ⭐⭐⭐ |
| **3. 클라우드 서비스** | 유료 | 쉬움 | 빠름 (3-5분) | ⭐⭐⭐⭐ |
| **4. Docker + 에뮬레이터** | 무료 | 높음 | 중간 (7-10분) | ⭐⭐ |

---

## 🥇 추천: GitHub Actions + Android 에뮬레이터

### 장점
- ✅ **완전 무료** (GitHub Actions 월 2,000분 무료)
- ✅ **설정 간단** (YAML 파일 하나만)
- ✅ **포트폴리오에 좋음** (실무에서 많이 사용)
- ✅ **실제 기기 없이 실행 가능**

### 단점
- ❌ 느림 (에뮬레이터 부팅 5분 + 테스트 5-10분)
- ❌ macOS runner 필요 시 분당 비용 발생 (iOS 테스트용)
- ❌ Flaky 테스트 가능성 (클라우드 환경)

---

## 🔧 구현 방법 1: GitHub Actions + Android Emulator

### 1.1 GitHub Actions Workflow 파일 생성

**파일:** `.github/workflows/appium-test.yml`

```yaml
name: Appium Mobile Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    # 매일 오전 9시 자동 실행 (KST 기준)
    - cron: '0 0 * * *'

jobs:
  android-test:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      # 1. 코드 체크아웃
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. Python 설정
      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      # 3. 의존성 캐싱 (빌드 속도 향상)
      - name: Cache pip dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      # 4. Python 의존성 설치
      - name: Install Python dependencies
        run: |
          pip install -r requirements.txt

      # 5. Node.js 설정 (Appium 실행용)
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      # 6. Appium 설치
      - name: Install Appium
        run: |
          npm install -g appium@2.0
          appium driver install uiautomator2

      # 7. Java 설정 (Android 빌드용)
      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      # 8. Android SDK 설정
      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      # 9. Android 에뮬레이터 실행 (핵심!)
      - name: Run Android Emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          target: google_apis
          arch: x86_64
          profile: pixel_6
          disable-animations: true
          emulator-options: -no-snapshot-save -no-window -gpu swiftshader_indirect -noaudio -no-boot-anim
          script: |
            # 에뮬레이터 부팅 대기
            adb wait-for-device
            adb devices

            # Appium 서버 백그라운드 실행
            appium &
            sleep 5

            # APK 설치 (앱이 있는 경우)
            # adb install -r app-debug.apk

            # 테스트 실행
            pytest src/tests/ --reruns 2 --alluredir=allure-results -v

      # 10. 테스트 실패 시 스크린샷 업로드
      - name: Upload screenshots on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-screenshots
          path: screenshots/
          retention-days: 7

      # 11. Allure 리포트 생성
      - name: Generate Allure Report
        if: always()
        run: |
          pip install allure-pytest
          allure generate allure-results -o allure-report --clean

      # 12. Allure 리포트 배포 (GitHub Pages)
      - name: Deploy Allure Report to GitHub Pages
        if: always()
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./allure-report
          publish_branch: gh-pages
          destination_dir: allure-report
```

---

### 1.2 conftest.py 수정 (CI/CD 환경 대응)

**파일:** `src/conftest.py`

```python
import os
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

def is_ci_environment():
    """CI 환경인지 확인"""
    return os.getenv("CI") == "true" or os.getenv("GITHUB_ACTIONS") == "true"

@pytest.fixture(scope="session")
def driver():
    """Appium 드라이버 초기화"""

    options = UiAutomator2Options()

    if is_ci_environment():
        # CI 환경: 에뮬레이터 사용
        options.platform_name = "Android"
        options.platform_version = "13.0"  # API 33
        options.device_name = "emulator-5554"
        options.automation_name = "UiAutomator2"
        options.app_package = "com.woongjin.market"  # 실제 패키지명
        options.app_activity = ".MainActivity"  # 실제 액티비티명
        options.no_reset = True
        options.full_reset = False

        # CI 환경 최적화
        options.new_command_timeout = 300
        options.adb_exec_timeout = 30000

    else:
        # 로컬 환경: 실제 디바이스 사용
        options.platform_name = "Android"
        options.platform_version = os.getenv("PLATFORM_VERSION", "14.0")
        options.device_name = os.getenv("DEVICE_NAME", "R3CX70ALSLB")
        options.automation_name = "UiAutomator2"
        options.app_package = "com.woongjin.market"
        options.app_activity = ".MainActivity"
        options.no_reset = True
        options.full_reset = False

    # Appium 서버 URL
    appium_server_url = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723")

    driver = webdriver.Remote(appium_server_url, options=options)
    driver.implicitly_wait(10)

    yield driver

    driver.quit()
```

---

### 1.3 .env 파일 GitHub Secrets로 관리

**GitHub 저장소 → Settings → Secrets and variables → Actions**

```
TEST_USER_ID=your_email@example.com
TEST_USER_PASSWORD=your_password
APPIUM_SERVER=http://127.0.0.1:4723
```

**conftest.py에서 사용:**
```python
import os
from dotenv import load_dotenv

if not is_ci_environment():
    load_dotenv()  # 로컬에서만 .env 로드

@pytest.fixture
def test_user_credentials():
    return {
        "user_id": os.getenv("TEST_USER_ID"),
        "password": os.getenv("TEST_USER_PASSWORD")
    }
```

---

## 🏠 구현 방법 2: Self-hosted Runner (로컬 기기 연결)

### 장점
- ✅ **실제 기기 사용 가능** (에뮬레이터보다 빠름)
- ✅ **무료** (자신의 PC 사용)
- ✅ **로컬 환경과 동일**

### 단점
- ❌ PC를 24시간 켜둬야 함
- ❌ 네트워크 안정성 필요
- ❌ 보안 문제 (GitHub에 로컬 접근 권한 제공)

### 설정 방법

**1. GitHub 저장소 → Settings → Actions → Runners → New self-hosted runner**

**2. 로컬 PC에 Runner 설치 (Windows 예시)**
```bash
# 1. Runner 다운로드 및 설치
mkdir actions-runner && cd actions-runner
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-win-x64-2.311.0.zip -OutFile actions-runner-win-x64-2.311.0.zip
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory("$PWD/actions-runner-win-x64-2.311.0.zip", "$PWD")

# 2. Runner 등록
./config.cmd --url https://github.com/YOUR_USERNAME/YOUR_REPO --token YOUR_TOKEN

# 3. Runner 실행
./run.cmd
```

**3. Workflow 파일 수정**
```yaml
jobs:
  android-test:
    runs-on: self-hosted  # ubuntu-latest 대신 self-hosted

    steps:
      - name: Start Appium Server
        run: |
          appium &
          sleep 5

      - name: Run Tests
        run: |
          pytest src/tests/ --reruns 2 -v
```

---

## ☁️ 구현 방법 3: 클라우드 테스트 서비스

### 3.1 BrowserStack (유료)
- **비용:** 월 $29~ (100분 테스트)
- **장점:** 실제 기기 2,000대 이상, iOS/Android 모두 지원

**Workflow 예시:**
```yaml
- name: Run BrowserStack Tests
  env:
    BROWSERSTACK_USERNAME: ${{ secrets.BROWSERSTACK_USERNAME }}
    BROWSERSTACK_ACCESS_KEY: ${{ secrets.BROWSERSTACK_ACCESS_KEY }}
  run: |
    pytest src/tests/ --browserstack -v
```

### 3.2 Firebase Test Lab (Google, 유료)
- **비용:** 무료 할당량 있음 (하루 5회 테스트)
- **장점:** Google 서비스, 실제 기기 사용

**명령어:**
```bash
gcloud firebase test android run \
  --type instrumentation \
  --app app-debug.apk \
  --test app-debug-androidTest.apk \
  --device model=Pixel6,version=33
```

### 3.3 Sauce Labs (유료)
- **비용:** 월 $39~
- **장점:** 병렬 실행 지원, 비디오 녹화

---

## 🐳 구현 방법 4: Docker + Android Emulator (고급)

### 장점
- ✅ 로컬/CI 환경 통일
- ✅ 재현 가능한 환경

### 단점
- ❌ 설정 복잡
- ❌ 성능 낮음 (중첩 가상화)

**Dockerfile 예시:**
```dockerfile
FROM budtmo/docker-android:emulator_13.0

# Appium 설치
RUN npm install -g appium@2.0
RUN appium driver install uiautomator2

# Python 설치
RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

CMD ["appium"]
```

---

## 🎯 포트폴리오를 위한 추천 구성

### 최소 구성 (1-2시간)
```yaml
# .github/workflows/appium-test.yml
name: Appium Test

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          script: pytest src/tests/test_login.py -v
```

### 권장 구성 (3-4시간)
- GitHub Actions + Android Emulator
- Allure 리포트 자동 생성
- 실패 시 스크린샷 업로드
- Slack 알림 (다음 섹션)

---

## 📊 실행 시간 비교

| 환경 | 에뮬레이터 부팅 | 테스트 실행 | 총 시간 |
|------|----------------|------------|---------|
| **로컬 (실제 기기)** | 0분 | 3-5분 | **3-5분** |
| **GitHub Actions** | 5-7분 | 5-10분 | **10-17분** |
| **Self-hosted Runner** | 0분 | 3-5분 | **3-5분** |
| **BrowserStack** | 1분 | 3-5분 | **4-6분** |

---

## ⚠️ 주의사항

### 1. APK 파일 준비
GitHub Actions에서는 앱 APK가 필요합니다.

**옵션 A:** APK를 저장소에 커밋 (비추천, 용량 큼)
**옵션 B:** APK를 다운로드 (추천)
```yaml
- name: Download APK
  run: |
    curl -o app.apk https://your-server.com/app.apk
    adb install -r app.apk
```

**옵션 C:** 이미 설치된 앱 사용 (appPackage/appActivity만 사용)

### 2. 테스트 안정성
- 에뮬레이터는 느려서 timeout 늘려야 함
- `implicitly_wait(15)` → `implicitly_wait(30)`
- `--reruns 2` 옵션으로 Flaky 테스트 대응

### 3. GitHub Actions 무료 한도
- **Public 저장소:** 무제한
- **Private 저장소:** 월 2,000분
- 테스트 1회 = 15분이면, **월 133회 실행 가능**

---

## 🎓 결론: 어떤 방법을 선택할까?

### 포트폴리오용 (추천)
**→ GitHub Actions + Android Emulator**
- 무료, 설정 간단, 면접에서 어필 가능
- "CI/CD 구축 경험 있음" 증명 가능

### 실무 프로젝트용
**→ BrowserStack/Firebase Test Lab + Self-hosted Runner 병행**
- 빠른 피드백 (Self-hosted)
- 다양한 기기 테스트 (클라우드)

### 학습용
**→ 로컬에서만 실행**
- CI/CD 없이 수동 실행
- 복잡도 낮음

---

## 📌 다음 단계

1. **GitHub Actions 워크플로우 작성** (.github/workflows/appium-test.yml)
2. **conftest.py CI 환경 분기 처리**
3. **Slack 알림 연동** (다음 문서 참고)
4. **README에 CI/CD 뱃지 추가**

```markdown
# README.md
![Appium Tests](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Appium%20Test/badge.svg)
```

---

**작성일:** 2025-12-24
**참고:** GitHub Actions 무료 한도 확인 필수
