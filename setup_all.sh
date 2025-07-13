#!/bin/bash
set -e

bash ./setup_env.sh
bash ./setup_data_pipeline.sh
bash ./setup_ai_ml.sh
bash ./setup_backend_dashboard.sh
bash ./setup_quality_monitoring.sh
bash ./setup_deployment.sh
bash ./setup_security.sh
bash ./setup_collaboration.sh
bash ./setup_optimization.sh
bash ./setup_experimentation.sh

echo "[setup_all.sh] 엔터프라이즈 AI/ML 통합 자동화 완료!" 