#!/bin/bash
set -e

# 1. 프로젝트 구조/환경/코드 스타일/문서 표준화
bash scripts/setup_project_env.sh

# 2. 데이터 파이프라인/모델 템플릿/문서화
bash scripts/setup_data_model_ci.sh

# 3. Jupyter Lab, ipykernel, notebook 자동화
bash scripts/setup_jupyter.sh

# 4. 테스트/품질/CI/CD 자동화
bash scripts/setup_quality_ci.sh

# 5. 실행/배포/운영/모니터링 자동화
bash scripts/setup_ops_monitoring.sh

# 6. 글로벌 협업/지속적 개선 자동화
bash scripts/setup_global_collab.sh

echo "[완료] Mr. Mark 프로젝트 전체 자동화 세팅이 끝났습니다!" 