#!/bin/bash
set -e

# Python 환경 세팅
if [ -f .python-version ]; then
  pyenv install -s $(cat .python-version)
  pyenv local $(cat .python-version)
fi

if [ ! -d venv ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || true

deactivate

# Node.js 패키지 설치
if [ -f package.json ]; then
  npm install || pnpm install || yarn install
fi

# .env 파일 복사
if [ ! -f .env ] && [ -f .env.example ]; then
  cp .env.example .env
fi

chmod +x scripts/*.sh

echo "[SETUP] 환경 세팅 완료!" 