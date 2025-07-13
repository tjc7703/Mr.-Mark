# 운영 자동화/모니터링 고도화

## Prometheus + Grafana
- prometheus.yml: 메트릭 수집 설정
- grafana: 대시보드 시각화, 알림 연동

## Alertmanager
- alertmanager.yml: 슬랙/이메일 알림 템플릿

## 연동 예시
- ai-engine/monitoring.py, backend/health, k8s 서비스 메트릭 수집
- 슬랙/이메일로 장애/이상 감지 알림

## 실행 예시
```bash
# prometheus 실행
prometheus --config.file=prometheus.yml
# grafana 실행 (3000포트)
grafana-server
# alertmanager 실행
alertmanager --config.file=alertmanager.yml
``` 