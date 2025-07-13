# 실전 운영/배포 자동화

## 운영 환경별 배포
- dev, staging, prod 등 환경별 config, 배포 스크립트 분리

## 롤링/무중단 배포
- rolling-update.sh: 롤링/무중단 배포 자동화
- blue/green, canary, 롤백 등 다양한 전략 적용 가능

## 자동 롤백
- k8s rollout undo, rollback.sh 등 장애 시 자동 복구

## 실시간 모니터링 연동
- prometheus, grafana, alertmanager, slack/webhook 등과 연동 