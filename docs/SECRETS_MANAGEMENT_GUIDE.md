# 민감 정보 관리 가이드

## 🔐 핵심 원칙

**절대로 GitHub에 올리면 안 되는 것:**
- ❌ 비밀번호, API 키
- ❌ 인증서, 토큰
- ❌ 개인 계정 정보

**GitHub에 올려도 되는 것:**
- ✅ 설정 파일 (app_config.py)
- ✅ 코드 구조
- ✅ 의존성 목록

---

## 📁 파일별 가이드

### ❌ .env (절대 커밋 금지)
```bash
# .env - .gitignore에 등록 필수!
TEST_USER_ID=myemail@gmail.com        # 민감!
TEST_USER_PASSWORD=mySecretPass123    # 민감!
```

**이유:** 계정 탈취 위험

### ✅ .env.example (커밋 OK)
```bash
# .env.example - GitHub에 올려도 됨
TEST_USER_ID=your_email@example.com   # 예시만
TEST_USER_PASSWORD=your_password_here # 예시만
```

**이유:** 실제 값 없음, 구조만 공유

### ✅ app_config.py (커밋 OK)
```python
# app_config.py - GitHub에 올려도 됨
WOONGJIN_APP = {
    "deviceName": "R3CX70ALSLB",      # 공개 정보
    "appPackage": "com.wjthinkbig.woongjinbooks",  # 공개 앱
}
```

**이유:** 민감 정보 없음

---

## 🎯 현재 프로젝트 분석

### 파일 구조
```
Project/
├── .env                    ❌ .gitignore 등록됨 (올바름!)
├── .env.example            ✅ 커밋 가능
├── src/
│   ├── config/
│   │   └── app_config.py   ✅ 커밋 가능 (민감 정보 없음)
│   └── conftest.py         ✅ 커밋 가능
└── .gitignore              ✅ .env 포함됨
```

### 현재 상태: ✅ 안전함!

---

## 🛡️ .gitignore 완전판

**파일:** `.gitignore` (이미 업데이트됨)

```gitignore
# 민감 정보
.env

# Python
__pycache__/
*.pyc
venv/

# 테스트 결과물
screenshots/
page_sources/
*.log

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## 🔄 GitHub Secrets 설정 (CI/CD용)

### 문제 상황
```yaml
# ❌ 잘못된 예 - YAML에 직접 작성
env:
  PASSWORD: mypassword123  # GitHub에 공개됨!
```

### 해결 방법: GitHub Secrets 사용

#### 1단계: Secrets 등록
**GitHub 저장소 → Settings → Secrets and variables → Actions**

**New repository secret 클릭:**
```
Name: TEST_USER_ID
Secret: your_email@example.com
```

```
Name: TEST_USER_PASSWORD
Secret: your_actual_password
```

#### 2단계: Workflow에서 사용
```yaml
# .github/workflows/appium-test.yml
jobs:
  test:
    env:
      TEST_USER_ID: ${{ secrets.TEST_USER_ID }}          # ✅ 안전
      TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}  # ✅ 안전
```

#### 3단계: conftest.py에서 읽기
```python
# conftest.py
import os
from dotenv import load_dotenv

# 로컬 환경에서만 .env 로드
if not os.getenv("CI"):
    load_dotenv()

@pytest.fixture
def test_user_credentials():
    return {
        "user_id": os.getenv("TEST_USER_ID"),      # 로컬: .env / CI: Secrets
        "password": os.getenv("TEST_USER_PASSWORD")
    }
```

---

## 🚨 실수했을 때 대처법

### Case 1: .env를 커밋했다!

**즉시 조치:**
```bash
# 1. 커밋 취소 (아직 Push 안 했을 때)
git reset HEAD~1

# 2. .gitignore에 .env 추가
echo ".env" >> .gitignore

# 3. 다시 커밋
git add .gitignore
git commit -m "Add .env to gitignore"
```

### Case 2: 이미 Push했다!

**심각한 상황 - 즉시 조치 필요:**

#### 옵션 A: 비밀번호 변경 (가장 안전)
1. 테스트 계정 비밀번호 즉시 변경
2. .env 파일 Git 히스토리에서 완전 삭제

```bash
# Git 히스토리에서 완전 삭제
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```

#### 옵션 B: BFG Repo-Cleaner (더 쉬움)
```bash
# BFG 다운로드
# https://rtyley.github.io/bfg-repo-cleaner/

# .env 파일 완전 삭제
bfg --delete-files .env

git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
```

**⚠️ 주의:** Force push는 위험! 팀 프로젝트면 조율 필요

---

## 📊 민감 정보 체크리스트

### 커밋 전 확인사항
- [ ] .env 파일이 .gitignore에 등록되어 있는가?
- [ ] git status에서 .env가 보이지 않는가?
- [ ] 코드에 하드코딩된 비밀번호가 없는가?
- [ ] API 키가 코드에 직접 들어가지 않았는가?

### GitHub Secrets 확인사항
- [ ] 모든 민감 정보가 Secrets에 등록되었는가?
- [ ] Workflow에서 ${{ secrets.NAME }} 형식으로 사용하는가?
- [ ] 로그에 민감 정보가 출력되지 않는가?

---

## 🔍 민감 정보 찾기

### 자동 검색
```bash
# 현재 커밋된 파일에서 비밀번호 검색
git grep -i "password"
git grep -i "api_key"
git grep -i "secret"

# .env 파일이 커밋되었는지 확인
git log --all --full-history -- .env
```

### 수동 확인
**검색어:**
- `password`
- `api_key`
- `secret`
- `token`
- `credentials`

---

## 💡 베스트 프랙티스

### 1. 환경 변수 사용
```python
# ❌ 나쁜 예
PASSWORD = "mypassword123"

# ✅ 좋은 예
PASSWORD = os.getenv("TEST_USER_PASSWORD")
```

### 2. .env.example 제공
```bash
# 팀원이 프로젝트 시작 시
cp .env.example .env
# .env 파일 편집하여 실제 값 입력
```

### 3. README에 안내
```markdown
## 설정 방법

1. `.env.example`을 복사하여 `.env` 생성
2. `.env` 파일에 실제 계정 정보 입력
3. **절대로 .env 파일을 커밋하지 마세요!**
```

### 4. Pre-commit Hook (고급)
```bash
# .git/hooks/pre-commit
#!/bin/sh

if git diff --cached --name-only | grep -q "^.env$"; then
    echo "❌ .env 파일은 커밋할 수 없습니다!"
    exit 1
fi
```

---

## 🎓 요약

### AppConfig.py
**답변:** ✅ .gitignore에 넣지 않아도 됩니다!

**이유:**
- `deviceName`, `appPackage` 등은 공개 정보
- 비밀번호나 API 키 없음
- GitHub에 올려도 안전

### .env 파일
**답변:** ❌ 절대로 커밋하면 안 됩니다!

**이유:**
- 실제 계정 정보 포함
- .gitignore에 반드시 등록
- GitHub Secrets 사용 권장

---

## 📚 참고 자료

### GitHub Secrets 공식 문서
https://docs.github.com/en/actions/security-guides/encrypted-secrets

### .gitignore 생성기
https://www.toptal.com/developers/gitignore

### Git 히스토리 정리 (BFG)
https://rtyley.github.io/bfg-repo-cleaner/

---

**작성일:** 2025-12-24
**핵심:** .env는 .gitignore, app_config.py는 커밋 OK!
