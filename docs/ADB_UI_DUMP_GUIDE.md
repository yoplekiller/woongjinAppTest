# ADB UI Dump 가이드

앱 UI 소스를 추출하는 방법을 정리한 문서입니다.

## 기본 명령어

### 1. UI 덤프 (Git Bash)

```bash
# 1. 앱 실행 (패키지명/액티비티명 확인 필요)
adb shell am start -n com.woongjin.market/.MainActivity

# 2. UI 덤프
adb shell uiautomator dump /sdcard/window_dump.xml

# 3. 파일 가져오기 (Git Bash 경로 변환 방지)
MSYS_NO_PATHCONV=1 adb pull /sdcard/window_dump.xml
```

### 2. UI 덤프 (PowerShell / CMD)

```powershell
# PowerShell에서는 ; 사용
adb shell uiautomator dump /sdcard/window_dump.xml; adb pull /sdcard/window_dump.xml

# CMD에서는 && 사용
adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml
```

### 3. 한 줄로 실행 (Git Bash)

```bash
MSYS_NO_PATHCONV=1 adb shell "uiautomator dump /sdcard/window_dump.xml" && MSYS_NO_PATHCONV=1 adb pull /sdcard/window_dump.xml
```

## Python (Appium) 에서 사용

### page_source_helper 유틸리티 사용

```python
from utils.page_source_helper import save_page_source

# 현재 화면 XML로 저장
save_page_source(driver, "home_screen.xml")
```

### 직접 사용

```python
# driver.page_source로 바로 가져오기
source = driver.page_source

# 파일로 저장
with open("screen_dump.xml", "w", encoding="utf-8") as f:
    f.write(source)
```

## 테스트 실행으로 덤프

```bash
# 소스 추출 테스트 실행
pytest src/extract_source_test/test_woongjin_extract_source.py -v -s
```

## 자주 쓰는 ADB 명령어

```bash
# 연결된 디바이스 확인
adb devices

# 현재 포그라운드 앱 패키지/액티비티 확인
adb shell dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'

# 스크린샷
adb shell screencap /sdcard/screenshot.png
MSYS_NO_PATHCONV=1 adb pull /sdcard/screenshot.png

# 앱 강제 종료
adb shell am force-stop com.woongjin.market

# 앱 재시작
adb shell am start -n com.woongjin.market/.MainActivity
```

## 트러블슈팅

### Git Bash 경로 변환 문제

Git Bash가 `/sdcard/`를 `C:/Program Files/Git/sdcard/`로 변환하는 경우:

```bash
# 방법 1: MSYS_NO_PATHCONV 환경변수 사용
MSYS_NO_PATHCONV=1 adb pull /sdcard/window_dump.xml

# 방법 2: 영구 설정 (~/.bashrc에 추가)
export MSYS_NO_PATHCONV=1
```

### PowerShell && 에러

PowerShell에서 `&&`는 지원되지 않습니다. `;`로 대체:

```powershell
# 에러
adb shell uiautomator dump /sdcard/window_dump.xml && adb pull /sdcard/window_dump.xml

# 정상
adb shell uiautomator dump /sdcard/window_dump.xml; adb pull /sdcard/window_dump.xml
```

### 잠금 화면이 덤프되는 경우

앱이 아닌 시스템 UI가 덤프되면:
1. 화면 잠금 해제
2. 대상 앱을 포그라운드로 이동
3. 다시 덤프 실행
