# 로컬 Android 에뮬레이터 설정 가이드 (선택사항)

## ⚠️ 주의: 이 가이드는 선택사항입니다!

**현재 상황:**
- ✅ 실제 기기(`R3CX70ALSLB`)로 테스트 정상 작동 중
- ✅ GitHub Actions에서는 자동으로 에뮬레이터 생성됨

**이 가이드가 필요한 경우:**
- ❌ 실제 기기가 없을 때
- ❌ 다양한 Android 버전 테스트 필요
- ❌ 기기를 항상 연결하기 번거로울 때

**현재 사용 중인 실제 기기가 있다면 이 가이드는 건너뛰세요!**

---

## 📦 1단계: Android Studio 설치

### Windows 기준

#### 1.1 다운로드
```
https://developer.android.com/studio
```
- 용량: 약 1GB (설치 후 10GB 이상)
- 설치 시간: 30분~1시간

#### 1.2 설치
1. 다운로드한 설치 파일 실행
2. "Standard" 설치 선택
3. 설치 경로: 기본값 권장
4. Android SDK 위치 확인
   - 기본: `C:\Users\사용자명\AppData\Local\Android\Sdk`

#### 1.3 초기 설정
- Android SDK Tools 자동 설치 진행
- 첫 실행 시 약 5-10분 소요

---

## 🔧 2단계: AVD (Android Virtual Device) 생성

### 2.1 AVD Manager 열기
1. Android Studio 실행
2. 상단 메뉴: **Tools → Device Manager**
3. 또는 툴바의 스마트폰 아이콘 클릭

### 2.2 가상 기기 생성
1. **Create Device** 클릭

2. **하드웨어 선택**
   - Category: Phone
   - 추천: **Pixel 6** (또는 Pixel 5)
   - 이유: 최신 해상도, 안정적
   - **Next** 클릭

3. **시스템 이미지 선택**
   - Release Name: **Tiramisu (API 33)** 추천
     - Android 13 버전
     - GitHub Actions 예시와 동일
   - ABI: **x86_64** (Intel/AMD CPU용)
   - **Download** 클릭 (약 1-2GB, 10-20분 소요)
   - 다운로드 완료 후 **Next**

4. **AVD 설정**
   - AVD Name: `Pixel_6_API_33` (알아보기 쉽게)
   - Startup orientation: Portrait
   - **Advanced Settings 클릭**
     - RAM: 2048 MB (권장)
     - VM heap: 256 MB
     - Internal Storage: 2048 MB
   - **Finish** 클릭

### 2.3 에뮬레이터 실행 확인
1. Device Manager에서 생성한 기기 옆 **▶ 플레이 버튼** 클릭
2. 에뮬레이터 부팅 (첫 실행: 5-10분, 이후: 2-3분)
3. 화면에 Android 홈 화면 나오면 성공 ✅

---

## 🔌 3단계: ADB 연결 확인

### 3.1 환경 변수 설정 (Windows)

**Android SDK 경로 확인:**
```
C:\Users\사용자명\AppData\Local\Android\Sdk
```

**환경 변수 추가:**
1. **시작 → "환경 변수" 검색 → 시스템 환경 변수 편집**
2. **사용자 변수 → Path 편집**
3. **새로 만들기** 클릭 후 아래 경로 추가:
   ```
   C:\Users\tbell\AppData\Local\Android\Sdk\platform-tools
   C:\Users\tbell\AppData\Local\Android\Sdk\tools
   ```
4. **확인** 클릭
5. **터미널 재시작** (중요!)

### 3.2 ADB 연결 확인

**새 터미널/PowerShell 열기:**
```bash
adb devices
```

**예상 출력:**
```
List of devices attached
emulator-5554   device
```

**만약 `adb`를 찾을 수 없다면:**
- 환경 변수 설정 다시 확인
- 터미널 재시작
- PC 재부팅

---

## ⚙️ 4단계: Appium 설정 수정

### 4.1 app_config.py 수정

**파일:** `src/config/app_config.py`

**기존 코드:**
```python
WOONGJIN_APP: Dict[str, str] = {
    "platformName": "Android",
    "deviceName": "R3CX70ALSLB",  # 실제 기기
    "appPackage": "com.wjthinkbig.woongjinbooks",
    "appActivity": ".view.IntroActivity",
    "automationName": "UiAutomator2",
}
```

**수정 코드:**
```python
import os

class AppConfig:
    # 환경 변수로 기기 선택 (기본값: 실제 기기)
    DEVICE_NAME = os.getenv("DEVICE_NAME", "R3CX70ALSLB")

    WOONGJIN_APP: Dict[str, str] = {
        "platformName": "Android",
        "deviceName": DEVICE_NAME,  # 환경 변수에서 가져오기
        "appPackage": "com.wjthinkbig.woongjinbooks",
        "appActivity": ".view.IntroActivity",
        "automationName": "UiAutomator2",
    }
```

### 4.2 .env 파일 수정

**파일:** `.env`

**추가:**
```bash
# 기본: 실제 기기
DEVICE_NAME=R3CX70ALSLB

# 에뮬레이터 사용 시 주석 해제
# DEVICE_NAME=emulator-5554
```

---

## 🧪 5단계: 에뮬레이터로 테스트 실행

### 5.1 에뮬레이터 실행
1. Android Studio → Device Manager
2. 생성한 AVD **▶ 플레이 버튼** 클릭
3. 부팅 완료 대기 (2-3분)

### 5.2 ADB 연결 확인
```bash
adb devices
```
출력:
```
emulator-5554   device
```

### 5.3 웅진마켓 앱 설치

**방법 A: APK 파일로 설치 (권장)**
```bash
adb install -r C:\path\to\woongjin_market.apk
```

**방법 B: Google Play Store 사용**
1. 에뮬레이터에서 Play Store 앱 실행
2. Google 계정 로그인
3. "웅진마켓" 검색 → 설치

### 5.4 .env 파일 수정
```bash
# DEVICE_NAME=R3CX70ALSLB  ← 주석 처리
DEVICE_NAME=emulator-5554   # 에뮬레이터 사용
```

### 5.5 테스트 실행
```bash
pytest src/tests/test_login.py -v
```

**성공 시:**
- 에뮬레이터 화면에서 앱 실행됨
- 테스트 자동 진행
- 로그인 성공 확인

---

## 🔄 6단계: 실제 기기 ↔ 에뮬레이터 전환

### 실제 기기 사용
```bash
# .env
DEVICE_NAME=R3CX70ALSLB
```

### 에뮬레이터 사용
```bash
# .env
DEVICE_NAME=emulator-5554
```

### 동적 선택 (고급)
**conftest.py 수정:**
```python
import os

@pytest.fixture(scope="function")
def driver() -> Generator[WebDriver, None, None]:
    device_name = os.getenv("DEVICE_NAME", "R3CX70ALSLB")

    if device_name.startswith("emulator"):
        logger.info("🖥️ 에뮬레이터 사용")
    else:
        logger.info("📱 실제 기기 사용")

    caps = AppConfig.get_capabilities("woongjin")
    # ... (기존 코드)
```

---

## ⚡ 에뮬레이터 최적화 팁

### 성능 향상
1. **Android Studio → AVD 설정 → Edit**
2. **Emulated Performance**
   - Graphics: **Hardware - GLES 2.0** (빠름)
3. **RAM 조정**
   - 2048MB → 4096MB (PC 메모리 16GB 이상일 때)

### 빠른 부팅 (Cold Boot → Quick Boot)
1. AVD 설정 → **Boot option**
2. **Quick Boot** 선택
3. 부팅 시간: 10분 → 30초로 단축

### 애니메이션 비활성화
에뮬레이터에서:
1. **Settings → About emulated device**
2. **Build number 7번 탭** (개발자 옵션 활성화)
3. **Settings → System → Developer options**
4. **Window animation scale: 0.5x**
5. **Transition animation scale: 0.5x**
6. **Animator duration scale: 0.5x**

---

## 🐛 문제 해결 (Troubleshooting)

### 문제 1: 에뮬레이터가 느려요
**원인:** CPU 가상화(VT-x/AMD-V) 미활성화

**해결:**
1. BIOS 진입 (재부팅 시 F2/DEL 키)
2. **Intel VT-x** 또는 **AMD-V** 활성화
3. 저장 후 재부팅

**Windows 11 Hyper-V 충돌 해결:**
```powershell
# 관리자 권한 PowerShell
bcdedit /set hypervisorlaunchtype off
# 재부팅
```

### 문제 2: ADB가 에뮬레이터를 찾지 못해요
```bash
adb kill-server
adb start-server
adb devices
```

### 문제 3: 앱이 설치되지 않아요
**에러:** `INSTALL_FAILED_INSUFFICIENT_STORAGE`

**해결:**
1. AVD 설정 → Edit
2. **Internal Storage: 4096 MB**로 증가

### 문제 4: Appium이 에뮬레이터에 연결 안 됨
**에러:** `An unknown server-side error occurred while processing the command`

**해결:**
```bash
# Appium 서버 재시작
Ctrl+C  # 기존 서버 종료
appium  # 재시작
```

**app_config.py 확인:**
```python
"deviceName": "emulator-5554",  # 정확한 이름
```

---

## 📊 실제 기기 vs 에뮬레이터 비교

| 항목 | 실제 기기 | 에뮬레이터 |
|------|----------|-----------|
| **속도** | ⭐⭐⭐⭐⭐ 빠름 | ⭐⭐⭐ 보통 |
| **안정성** | ⭐⭐⭐⭐⭐ 높음 | ⭐⭐⭐ 중간 |
| **비용** | 기기 필요 | 무료 |
| **다양성** | 1개 기기만 | 무제한 생성 |
| **편의성** | USB 연결 필요 | PC만 있으면 됨 |
| **실제 환경** | ⭐⭐⭐⭐⭐ 동일 | ⭐⭐⭐⭐ 유사 |

---

## 🎯 권장 사용 전략

### 일상 개발/테스트
**→ 실제 기기 사용** (현재 방식 유지)
- 빠르고 안정적
- 실제 사용자 환경과 동일

### 특수 상황
**→ 에뮬레이터 사용**
- 다른 Android 버전 테스트 (API 29, 30, 31 등)
- 다양한 화면 크기 테스트 (폴더블, 태블릿 등)
- 실제 기기 미연결 시 백업

### CI/CD
**→ GitHub Actions 에뮬레이터** (자동)
- 로컬 설치 불필요
- 자동화된 테스트

---

## ✅ 최종 체크리스트

### GitHub Actions만 사용 (추천)
- [ ] `.github/workflows/appium-test.yml` 작성
- [ ] Git Push
- [ ] **로컬 설치 불필요!**

### 로컬 에뮬레이터 추가 (선택)
- [ ] Android Studio 설치
- [ ] AVD 생성
- [ ] 에뮬레이터 부팅 확인
- [ ] ADB 연결 확인
- [ ] 웅진마켓 앱 설치
- [ ] `.env` 파일 수정
- [ ] 테스트 실행 성공

---

## 🔗 추가 자료

- [Android Studio 공식 가이드](https://developer.android.com/studio/intro)
- [AVD Manager 사용법](https://developer.android.com/studio/run/managing-avds)
- [Appium Android 설정](http://appium.io/docs/en/drivers/android-uiautomator2/)

---

**작성일:** 2025-12-24
**대상:** 로컬 에뮬레이터 테스트가 필요한 경우 (선택사항)
**참고:** 실제 기기가 있다면 이 가이드는 선택사항입니다!
