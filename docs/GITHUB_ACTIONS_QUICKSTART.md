# GitHub Actions 자동 실행 가이드

## 🎯 핵심 개념

**질문:** "GitHub에 push만 하면 자동으로 돌아간다는 것임?"

**답변:** ✅ **네, 정확합니다!**

### 작동 조건
`.github/workflows/` 폴더에 YAML 파일이 있으면 **자동으로** 실행됩니다.

---

## 🔄 전체 흐름 (애니메이션)

```
1. 코드 작성 (로컬 PC)
   ↓
2. git push
   ↓
3. GitHub이 자동 감지 👀
   ↓
4. Actions 탭에서 실행 시작 🚀
   ↓
5. 에뮬레이터 생성 + 테스트 실행 🤖
   ↓
6. 결과 확인 (성공 ✅ / 실패 ❌)
   ↓
7. 이메일 알림 (옵션) 📧
```

**사용자는 아무것도 안 해도 됨!** push만 하면 끝!

---

## 📝 최소 설정 (5분)

### 1단계: 폴더 생성
```bash
# 프로젝트 루트에서
mkdir -p .github/workflows
```

### 2단계: YAML 파일 생성

**파일:** `.github/workflows/appium-test.yml`

**최소 버전 (테스트만):**
```yaml
name: Appium Test

# 🔥 핵심: 언제 실행할지 정의
on:
  push:              # push 할 때마다
    branches:
      - main         # main 브랜치만
  pull_request:      # PR 생성 시에도
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest  # GitHub이 Ubuntu 서버 자동 생성

    steps:
      # 1. 코드 가져오기
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. Python 설치
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      # 3. 의존성 설치
      - name: Install dependencies
        run: pip install -r requirements.txt

      # 4. Node.js 설치 (Appium용)
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      # 5. Appium 설치
      - name: Install Appium
        run: |
          npm install -g appium@2.0
          appium driver install uiautomator2

      # 6. 에뮬레이터 + 테스트 실행 (핵심!)
      - name: Run tests on emulator
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          target: google_apis
          arch: x86_64
          script: |
            appium &
            sleep 5
            pytest src/tests/test_login.py -v
```

### 3단계: Push
```bash
git add .github/workflows/appium-test.yml
git commit -m "Add GitHub Actions workflow"
git push origin main
```

### 4단계: GitHub에서 확인

**웹 브라우저에서:**
1. GitHub 저장소로 이동
2. 상단 **"Actions"** 탭 클릭
3. **"Appium Test"** 워크플로우 자동 실행 중 확인! 🎉

---

## 🖥️ GitHub Actions 탭 화면

### 실행 중
```
Actions
  ├── All workflows
  │   └── Appium Test  🟡 (실행 중)
  │
  └── Recent workflow runs
      └── Add GitHub Actions workflow
          ├── test / ubuntu-latest  🟡 In progress
          │   ├── ✅ Checkout code (완료)
          │   ├── ✅ Setup Python (완료)
          │   ├── ✅ Install dependencies (완료)
          │   ├── ✅ Setup Node.js (완료)
          │   ├── ✅ Install Appium (완료)
          │   └── 🟡 Run tests on emulator (진행 중...)
          │       ├── Starting emulator...
          │       ├── Waiting for device...
          │       └── Running pytest...
```

### 성공 시
```
Actions
  └── Appium Test  ✅ (성공)
      └── test
          └── All steps completed ✅

          실행 시간: 12분 34초
```

### 실패 시
```
Actions
  └── Appium Test  ❌ (실패)
      └── test
          ├── ✅ Checkout code
          ├── ✅ Setup Python
          └── ❌ Run tests on emulator
              └── Error: Test failed at line 45

          스크린샷 다운로드 가능
```

---

## 🎮 트리거 옵션 (언제 실행할까?)

### 옵션 1: Push할 때마다 (기본)
```yaml
on:
  push:
    branches:
      - main
      - develop  # 여러 브랜치 가능
```

### 옵션 2: PR 생성 시
```yaml
on:
  pull_request:
    branches:
      - main
```

### 옵션 3: 스케줄 (매일 자동)
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # 매일 자정 (UTC)
    # 0 9 * * * → 매일 오전 9시 (UTC, 한국 시간 18시)
```

### 옵션 4: 수동 실행
```yaml
on:
  workflow_dispatch:  # Actions 탭에서 버튼 클릭으로 실행
```

### 옵션 5: 전부 조합
```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'
  workflow_dispatch:
```

---

## 🧪 실제 테스트 시나리오

### 시나리오 1: 코드 수정 → 자동 테스트
```bash
# 1. 로컬에서 test_login.py 수정
vim src/tests/test_login.py

# 2. 커밋 & Push
git add .
git commit -m "로그인 테스트 수정"
git push

# 3. 자동 실행! (아무것도 안 해도 됨)
# GitHub Actions가 알아서:
#   - 에뮬레이터 생성
#   - 테스트 실행
#   - 결과 리포트
```

### 시나리오 2: PR 리뷰 전 자동 검증
```bash
# 1. 새 브랜치 생성
git checkout -b feature/new-test

# 2. 코드 작성 후 Push
git push origin feature/new-test

# 3. GitHub에서 PR 생성
# → 자동으로 테스트 실행!
# → 테스트 통과해야 Merge 가능
```

### 시나리오 3: 매일 밤 자동 회귀 테스트
```yaml
on:
  schedule:
    - cron: '0 15 * * *'  # 매일 자정 (KST)

# 매일 밤 자동으로 전체 테스트 실행
# 문제 발견 시 이메일 알림
```

---

## 📧 알림 설정

### GitHub 기본 알림 (자동)
- ❌ 테스트 실패 시: **자동 이메일 발송**
- ✅ 테스트 성공 시: 알림 없음 (옵션으로 활성화 가능)

### 알림 설정 변경
**GitHub → Settings → Notifications → Actions**
- ✅ Failed workflows only (기본)
- ✅ All workflows
- ❌ None

---

## 💰 비용 (무료 한도)

### Public 저장소
- ✅ **무제한 무료!**
- 제한 없이 사용 가능

### Private 저장소
| 플랜 | 월 무료 시간 | 초과 시 비용 |
|------|-------------|------------|
| **Free** | 2,000분 | $0.008/분 |
| **Pro** | 3,000분 | $0.008/분 |
| **Team** | 3,000분 | $0.008/분 |

**계산 예시:**
- 테스트 1회 = 15분
- 2,000분 ÷ 15분 = **133회/월 무료**
- 하루 4~5회 실행 가능

---

## 🔍 실행 로그 확인

### 로그 보는 법
1. **Actions 탭** 클릭
2. 실행된 워크플로우 클릭
3. **test** job 클릭
4. 각 step 클릭하면 상세 로그 확인

### 로그 예시
```
Run pytest src/tests/test_login.py -v
============================= test session starts ==============================
platform linux -- Python 3.11.0, pytest-7.4.0
collected 1 item

src/tests/test_login.py::test_login PASSED                              [100%]

============================== 1 passed in 12.34s ==============================
```

### 에러 로그
```
Run pytest src/tests/test_login.py -v
src/tests/test_login.py::test_login FAILED                              [100%]

E   AssertionError: 로그인 실패
E   assert False

src/tests/test_login.py:45: AssertionError
```

---

## 🛠️ 고급 기능

### 1. 아티팩트 (파일 다운로드)
```yaml
- name: Upload screenshots
  if: failure()  # 실패 시에만
  uses: actions/upload-artifact@v4
  with:
    name: screenshots
    path: screenshots/
```

**확인:**
- Actions → 실행된 워크플로우 → 하단 "Artifacts" 섹션
- 스크린샷 ZIP 다운로드 가능

### 2. 캐싱 (속도 향상)
```yaml
- name: Cache pip
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

**효과:**
- 첫 실행: 15분
- 캐싱 후: 10분 (30% 단축)

### 3. 매트릭스 (여러 버전 테스트)
```yaml
strategy:
  matrix:
    python-version: [3.9, 3.10, 3.11]
    api-level: [30, 31, 33]

steps:
  - uses: actions/setup-python@v4
    with:
      python-version: ${{ matrix.python-version }}
```

**효과:**
- Python 3개 버전 × API 3개 레벨 = 9번 자동 실행

---

## ⚠️ 주의사항

### 1. Secrets 관리
**민감한 정보는 절대 YAML에 직접 작성 금지!**

**잘못된 예:**
```yaml
env:
  PASSWORD: mypassword123  # ❌ 절대 금지!
```

**올바른 예:**
```yaml
env:
  PASSWORD: ${{ secrets.TEST_PASSWORD }}
```

**설정 방법:**
- GitHub 저장소 → **Settings → Secrets and variables → Actions**
- **New repository secret** 클릭
- Name: `TEST_PASSWORD`
- Secret: `실제비밀번호`

### 2. APK 파일 처리
**저장소에 APK 직접 커밋 금지** (용량 큼)

**방법 A: 외부 다운로드**
```yaml
- name: Download APK
  run: curl -o app.apk https://your-server.com/app.apk
```

**방법 B: GitHub Releases 사용**
```yaml
- name: Download from Release
  uses: robinraju/release-downloader@v1
  with:
    repository: "username/repo"
    tag: "v1.0.0"
    fileName: "app.apk"
```

### 3. 실행 시간 제한
- **최대 실행 시간:** 6시간 (초과 시 자동 종료)
- **권장 실행 시간:** 30분 이내
- **Timeout 설정:**
```yaml
jobs:
  test:
    timeout-minutes: 30  # 30분 초과 시 강제 종료
```

---

## ✅ 체크리스트

### 최소 설정 (5분)
- [ ] `.github/workflows/` 폴더 생성
- [ ] `appium-test.yml` 파일 작성
- [ ] `git push`
- [ ] Actions 탭에서 실행 확인

### 권장 설정 (30분)
- [ ] 실패 시 스크린샷 업로드
- [ ] 캐싱 설정 (속도 향상)
- [ ] Secrets 설정 (계정 정보)
- [ ] Allure 리포트 자동 배포
- [ ] Slack 알림 연동

---

## 🎯 FAQ

### Q1: 로컬에서 테스트 안 해도 되나요?
**A:** 아니요, 로컬 테스트 필수입니다!
- 로컬: 빠른 개발/디버깅
- GitHub Actions: 최종 검증/자동화

### Q2: 에뮬레이터가 느린데 속도 향상 방법은?
**A:**
```yaml
# 애니메이션 비활성화
disable-animations: true

# API 레벨 낮추기 (30 → 29)
api-level: 29

# 캐싱 사용
- uses: actions/cache@v3
```

### Q3: Private 저장소인데 무료 한도 초과하면?
**A:**
- Self-hosted Runner 사용 (무료)
- 테스트 실행 빈도 조절 (PR만, 매일 1회 등)

### Q4: iOS 테스트도 가능한가요?
**A:** 가능하지만 비용 발생
```yaml
runs-on: macos-latest  # macOS runner (유료)
```
- macOS runner: 분당 $0.08 (10배 비용)

---

## 🚀 다음 단계

### 1. 기본 설정 완료 후
- [ ] README에 뱃지 추가
- [ ] Slack 알림 연동
- [ ] Allure 리포트 자동 배포

### 2. README 뱃지 예시
```markdown
![Tests](https://github.com/username/repo/workflows/Appium%20Test/badge.svg)
```

**결과:**
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

---

**작성일:** 2025-12-24
**핵심:** .github/workflows/YAML 파일만 있으면 자동 실행!
