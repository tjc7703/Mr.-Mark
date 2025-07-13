#!/bin/bash
set -e

echo "=== [1] 네트워크/패키지 서버 상태 체크 ==="
curl -I https://registry.npmjs.org || (echo "NPM 서버 장애" && exit 1)

echo "=== [2] 병렬 빌드 시작 ==="
start_time=$(date +%s)

(time docker build -t mrmark-backend:latest ./apps/backend) 2>&1 | tee build_backend.log &
(time docker build -t mrmark-frontend:latest ./apps/frontend) 2>&1 | tee build_frontend.log &
(time docker build -t mrmark-ai-engine:latest ./apps/ai-engine) 2>&1 | tee build_ai_engine.log &
wait

echo "=== [3] 빌드 병목 자동 분석 ==="
python3 scripts/analyze_build_logs.py build_backend.log build_frontend.log build_ai_engine.log || true

echo "=== [4] CI/CD별 빌드 속도 비교 ==="
python3 scripts/compare_ci_build_times.py || true

end_time=$(date +%s)
echo "총 빌드 소요 시간: $((end_time - start_time))초"

echo "=== [5] 품질/테스트/배포/모니터링 등 후속 자동화 ==="
bash ./setup_quality_monitoring.sh || true
bash ./setup_deployment.sh || true
bash ./setup_security.sh || true
bash ./setup_collaboration.sh || true
bash ./setup_optimization.sh || true
bash ./setup_experimentation.sh || true

echo "=== [완료] 최적화된 통합 자동화 및 빌드 병목 리포트 ===" 