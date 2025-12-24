# Slack 알림 연동 가이드

## 🎯 목표

GitHub Actions에서 테스트가 완료되면 자동으로 Slack에 알림 전송

```
테스트 완료 → GitHub Actions → Slack 메시지 📬
```

---

## 📱 알림 예시

### 성공 시
```
✅ Appium 테스트 성공!

저장소: username/appium-project
브랜치: main
커밋: Add new test cases
실행 시간: 12분 34초
결과: 16개 테스트 모두 통과

상세보기: https://github.com/...
```

### 실패 시
```
❌ Appium 테스트 실패!

저장소: username/appium-project
브랜치: main
커밋: Fix login test
실패한 테스트: test_login_with_wrong_password
에러: AssertionError at line 45

상세보기: https://github.com/...
```

---

## 🔧 설정 방법 (10분)

### 1단계: Slack Webhook URL 생성

#### 1.1 Slack 워크스페이스 준비
- Slack 워크스페이스가 없다면: https://slack.com/get-started
- 무료 플랜으로 충분

#### 1.2 Incoming Webhook 앱 설치
1. **Slack 워크스페이스 열기**
2. 좌측 사이드바에서 **Apps** 클릭
3. **App Directory** 검색창에 `Incoming WebHooks` 입력
4. **Incoming WebHooks** 앱 선택
5. **Add to Slack** 버튼 클릭

#### 1.3 Webhook URL 생성
1. **Post to Channel** 선택
   - 예: `#github-notifications` (채널 새로 만들기 권장)
2. **Add Incoming WebHooks integration** 클릭
3. **Webhook URL 복사** (중요!)
   ```
   https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX
   ```
4. **Save Settings** 클릭

---

### 2단계: GitHub Secrets에 Webhook URL 저장

**GitHub 저장소 → Settings → Secrets and variables → Actions**

**New repository secret 클릭:**
```
Name: SLACK_WEBHOOK_URL
Secret: https://hooks.slack.com/services/T00000000/B00000000/XXXX...
```

**Save** 클릭

---

### 3단계: GitHub Actions Workflow 수정

#### 방법 A: 간단한 알림 (추천)

**파일:** `.github/workflows/appium-test.yml`

**기존 코드 끝에 추가:**
```yaml
    # 기존 테스트 단계들...

    # Slack 알림 (성공/실패 모두)
    - name: Slack Notification
      if: always()  # 성공/실패 관계없이 항상 실행
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: '테스트가 완료되었습니다'
        webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
        fields: repo,message,commit,author,action,eventName,ref,workflow
```

#### 방법 B: 커스텀 메시지 (고급)

```yaml
    - name: Slack Notification on Success
      if: success()
      uses: slackapi/slack-github-action@v1.24.0
      with:
        payload: |
          {
            "text": "✅ Appium 테스트 성공!",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*✅ Appium 테스트 성공!*\n저장소: ${{ github.repository }}\n브랜치: ${{ github.ref_name }}\n커밋: ${{ github.event.head_commit.message }}"
                }
              },
              {
                "type": "actions",
                "elements": [
                  {
                    "type": "button",
                    "text": {
                      "type": "plain_text",
                      "text": "상세보기"
                    },
                    "url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
                  }
                ]
              }
            ]
          }
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK

    - name: Slack Notification on Failure
      if: failure()
      uses: slackapi/slack-github-action@v1.24.0
      with:
        payload: |
          {
            "text": "❌ Appium 테스트 실패!",
            "blocks": [
              {
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "*❌ Appium 테스트 실패!*\n저장소: ${{ github.repository }}\n브랜치: ${{ github.ref_name }}\n커밋: ${{ github.event.head_commit.message }}\n\n실패한 워크플로우를 확인하세요."
                }
              },
              {
                "type": "actions",
                "elements": [
                  {
                    "type": "button",
                    "text": {
                      "type": "plain_text",
                      "text": "실패 로그 보기"
                    },
                    "url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}",
                    "style": "danger"
                  }
                ]
              }
            ]
          }
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
        SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK
```

---

## 📋 완전한 Workflow 예시

**파일:** `.github/workflows/appium-test.yml`

```yaml
name: Appium Test with Slack

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      # 1. 코드 체크아웃
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. Python 설정
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      # 3. 의존성 설치
      - name: Install dependencies
        run: pip install -r requirements.txt

      # 4. Node.js & Appium 설치
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install Appium
        run: |
          npm install -g appium@2.0
          appium driver install uiautomator2

      # 5. 에뮬레이터 + 테스트 실행
      - name: Run tests
        uses: reactivecircus/android-emulator-runner@v2
        with:
          api-level: 33
          target: google_apis
          arch: x86_64
          script: |
            appium &
            sleep 5
            pytest src/tests/ -v --tb=short

      # 6. 실패 시 스크린샷 업로드
      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: test-screenshots
          path: screenshots/

      # 7. Slack 알림 (성공)
      - name: Slack - Success
        if: success()
        uses: 8398a7/action-slack@v3
        with:
          status: custom
          custom_payload: |
            {
              text: '✅ Appium 테스트 성공!',
              attachments: [{
                color: 'good',
                fields: [
                  { title: '저장소', value: '${{ github.repository }}', short: true },
                  { title: '브랜치', value: '${{ github.ref_name }}', short: true },
                  { title: '커밋', value: '${{ github.event.head_commit.message }}', short: false },
                  { title: '작성자', value: '${{ github.actor }}', short: true },
                  { title: '링크', value: '<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|상세보기>', short: true }
                ]
              }]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

      # 8. Slack 알림 (실패)
      - name: Slack - Failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: custom
          custom_payload: |
            {
              text: '❌ Appium 테스트 실패!',
              attachments: [{
                color: 'danger',
                fields: [
                  { title: '저장소', value: '${{ github.repository }}', short: true },
                  { title: '브랜치', value: '${{ github.ref_name }}', short: true },
                  { title: '커밋', value: '${{ github.event.head_commit.message }}', short: false },
                  { title: '작성자', value: '${{ github.actor }}', short: true },
                  { title: '링크', value: '<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|실패 로그 보기>', short: true }
                ]
              }]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 🎨 커스터마이징

### 메시지 색상 변경
```yaml
color: 'good'      # 녹색 (성공)
color: 'warning'   # 노란색 (경고)
color: 'danger'    # 빨간색 (실패)
color: '#FF5733'   # 커스텀 색상
```

### 이모지 추가
```yaml
text: '🎉 테스트 통과!'
text: '🚨 테스트 실패!'
text: '⏰ 스케줄 테스트 시작'
```

### 멘션 추가
```yaml
text: '<!channel> 테스트 실패!'      # 채널 전체 알림
text: '<@U12345678> 확인 필요'       # 특정 사용자 멘션
text: '<!here> 긴급 확인 필요'       # 온라인 사용자만
```

---

## 🔔 알림 시나리오별 설정

### 시나리오 1: 실패할 때만 알림
```yaml
- name: Slack - Failure Only
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: '❌ 테스트 실패! 확인 필요'
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 시나리오 2: 성공/실패 모두 알림
```yaml
- name: Slack - Always
  if: always()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 시나리오 3: main 브랜치만 알림
```yaml
- name: Slack - Main Branch Only
  if: github.ref == 'refs/heads/main'
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 시나리오 4: 스케줄 테스트 결과만 알림
```yaml
- name: Slack - Scheduled Tests
  if: github.event_name == 'schedule'
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: '⏰ 일일 회귀 테스트 완료'
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 📊 테스트 결과 상세 알림

### Pytest 결과 포함
```yaml
- name: Run tests and capture results
  id: pytest
  run: |
    pytest src/tests/ -v --tb=short > test_results.txt
    echo "PYTEST_RESULT<<EOF" >> $GITHUB_ENV
    cat test_results.txt >> $GITHUB_ENV
    echo "EOF" >> $GITHUB_ENV

- name: Slack with Test Results
  uses: 8398a7/action-slack@v3
  with:
    status: custom
    custom_payload: |
      {
        text: '테스트 결과',
        attachments: [{
          color: '${{ job.status == 'success' && 'good' || 'danger' }}',
          text: '```${{ env.PYTEST_RESULT }}```'
        }]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 스크린샷 링크 포함
```yaml
- name: Upload screenshots
  if: failure()
  id: screenshots
  uses: actions/upload-artifact@v4
  with:
    name: screenshots
    path: screenshots/

- name: Slack with Screenshot Link
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: custom
    custom_payload: |
      {
        text: '❌ 테스트 실패 - 스크린샷 확인 필요',
        attachments: [{
          color: 'danger',
          fields: [
            { title: '스크린샷', value: '<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|다운로드>', short: false }
          ]
        }]
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## 🧪 테스트 방법

### 1. Webhook URL 테스트 (curl)
```bash
curl -X POST -H 'Content-type: application/json' \
--data '{"text":"테스트 메시지입니다!"}' \
https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**성공 시:**
- Slack 채널에 "테스트 메시지입니다!" 표시

### 2. GitHub Actions에서 테스트
```bash
# 간단한 수정 후 Push
git add .
git commit -m "Test Slack notification"
git push

# GitHub Actions 탭에서 확인
# Slack 채널에서 알림 확인
```

---

## 🔧 문제 해결

### 문제 1: Slack 알림이 오지 않아요
**확인사항:**
1. Webhook URL이 정확한가?
   ```bash
   # GitHub Secrets 확인
   # Settings → Secrets → SLACK_WEBHOOK_URL
   ```
2. Slack 채널이 존재하는가?
3. Workflow에서 `if:` 조건이 맞는가?
   ```yaml
   if: always()  # 항상 실행
   if: failure() # 실패 시만
   ```

### 문제 2: 메시지가 깨져요
**원인:** JSON 형식 오류

**해결:**
- 작은따옴표 사용: `text: '메시지'`
- 이스케이프: `text: "메시지 \"인용\""`

### 문제 3: Secrets가 없다고 나와요
**에러:** `Error: Secrets "SLACK_WEBHOOK_URL" is not defined`

**해결:**
```bash
# GitHub Settings 확인
저장소 → Settings → Secrets and variables → Actions
→ SLACK_WEBHOOK_URL 존재하는지 확인
→ 없으면 New repository secret으로 추가
```

---

## 💡 고급 기능

### 1. 멀티 채널 알림
```yaml
# 실패 시 긴급 채널, 성공 시 일반 채널
- name: Slack - Critical
  if: failure()
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_CRITICAL }}

- name: Slack - General
  if: success()
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_GENERAL }}
```

### 2. 조건부 멘션
```yaml
custom_payload: |
  {
    text: '${{ job.status == 'failure' && '<!channel> 긴급!' || '테스트 완료' }}'
  }
```

### 3. 테스트 통계 포함
```yaml
- name: Calculate Stats
  id: stats
  run: |
    PASSED=$(grep -c "PASSED" test_results.txt || echo "0")
    FAILED=$(grep -c "FAILED" test_results.txt || echo "0")
    echo "passed=$PASSED" >> $GITHUB_OUTPUT
    echo "failed=$FAILED" >> $GITHUB_OUTPUT

- name: Slack with Stats
  uses: 8398a7/action-slack@v3
  with:
    custom_payload: |
      {
        text: '테스트 완료',
        fields: [
          { title: '통과', value: '${{ steps.stats.outputs.passed }}', short: true },
          { title: '실패', value: '${{ steps.stats.outputs.failed }}', short: true }
        ]
      }
```

---

## ✅ 체크리스트

### 기본 설정
- [ ] Slack Webhook URL 생성
- [ ] GitHub Secrets에 URL 저장
- [ ] Workflow에 알림 step 추가
- [ ] Push 후 Slack 알림 확인

### 고급 설정 (선택)
- [ ] 성공/실패 메시지 분리
- [ ] 커스텀 색상 적용
- [ ] 이모지 추가
- [ ] 멘션 설정
- [ ] 테스트 결과 통계 포함

---

## 📚 참고 자료

### Slack Incoming Webhooks 문서
https://api.slack.com/messaging/webhooks

### GitHub Actions - Slack 연동
https://github.com/marketplace/actions/slack-notify

### Slack Block Kit Builder (메시지 디자인)
https://app.slack.com/block-kit-builder

---

## 🎯 요약

### 최소 설정 (5분)
1. Slack Webhook URL 생성
2. GitHub Secrets에 저장
3. Workflow에 3줄 추가:
```yaml
- uses: 8398a7/action-slack@v3
  with:
    webhook_url: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 권장 설정 (15분)
- 성공/실패 메시지 분리
- 커스텀 색상 & 이모지
- 상세 링크 포함

**효과:**
- 테스트 완료 즉시 알림
- 모바일에서도 확인 가능
- 팀 협업 효율 향상

---

**작성일:** 2025-12-24
**난이도:** ⭐⭐ (쉬움)
**소요 시간:** 5-15분
