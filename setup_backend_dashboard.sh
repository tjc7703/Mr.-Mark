#!/bin/bash
set -e

# 1. FastAPI 백엔드 실행 (예시)
if [ -f apps/backend/main.py ]; then
  echo "[FastAPI] 서버 실행 중..."
  nohup python apps/backend/main.py &
fi

# 2. Dash/Streamlit 대시보드 실행 (예시)
if [ -f apps/ai-engine/app.py ]; then
  echo "[Dash/Streamlit] 대시보드 실행 중..."
  nohup python apps/ai-engine/app.py &
fi

echo "[setup_backend_dashboard.sh] 백엔드/대시보드/문서화 자동화 완료!" 