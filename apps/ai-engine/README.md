# AI 엔진 대시보드 & 모니터링

## Dash 대시보드
- dashboard.py: 실시간 트렌드, 품질지표, AI 예측 등 시각화 예시
- 실행: `python dashboard.py`

## 모니터링/품질관리
- monitoring.py: 로깅, Prometheus 메트릭, 알림 시스템 템플릿
- 실행: `python monitoring.py` (Prometheus 8001 포트)

## 확장 방법
- 대시보드: plotly, dash, pandas 등으로 다양한 시각화 추가
- 모니터링: prometheus_client, logging, alerting 연동 