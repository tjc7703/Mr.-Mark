#!/bin/bash
set -e

# Python 린트
if [ -f requirements.txt ]; then
  source venv/bin/activate
  pip install flake8 || true
  flake8 .
  deactivate
fi

# Node.js 린트
if [ -f package.json ]; then
  npm run lint || pnpm lint || yarn lint || true
fi 