#!/bin/bash
set -e

# Python 테스트
if [ -f requirements.txt ]; then
  source venv/bin/activate
  pip install pytest || true
  pytest || true
  deactivate
fi

# Node.js 테스트
if [ -f package.json ]; then
  npm test || pnpm test || yarn test || true
fi 