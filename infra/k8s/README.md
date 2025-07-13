# Kubernetes 템플릿 & 인프라 확장/운영 고도화

## Blue/Green 무중단 배포
- bluegreen-deployment.yaml: blue/green 버전 동시 배포, 서비스 selector로 트래픽 전환
- rollback.sh: 롤백/자동 복구 스크립트

## CI/CD 파이프라인
- .github/workflows/cicd.yml: 테스트, 빌드, 배포, 슬랙 알림 자동화

## 실시간 장애 복구/운영 자동화
- health check, self-healing, autoscaling, 장애 감지/알림

## 데이터/모델 거버넌스
- 데이터/모델 버전 관리, lineage, audit log, 데이터 품질 자동화 