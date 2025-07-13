# Alertmanager 실시간 알림 연동

## Slack 연동
- alertmanager.yml에 slack_configs 추가
- SLACK_WEBHOOK_URL 환경변수/secrets로 관리

## 이메일 연동
- alertmanager.yml에 email_configs 추가
- SMTP 서버, 인증정보 환경변수/secrets로 관리

## 참고
- 장애/이상 감지 시 실시간 알림 자동 발송 