#!/bin/bash
set -e

# 1. pytest, black, flake8, mypy, pre-commit 설치
pip install pytest black flake8 mypy pre-commit

# 2. pre-commit hook 설치
pre-commit install

# 3. 테스트/품질 스크립트 및 샘플 테스트 생성
cp templates/test_sample.py tests/ 2>/dev/null || mkdir -p tests && touch tests/test_sample.py
cp templates/lint.sh scripts/ 2>/dev/null || touch scripts/lint.sh
cp templates/test.sh scripts/ 2>/dev/null || touch scripts/test.sh

# 4. CI/CD 워크플로우 템플릿 복사
cp templates/ci_template.yml .github/workflows/ci.yml 2>/dev/null || touch .github/workflows/ci.yml

echo "[4단계] 테스트/품질/CI/CD 자동화 완료" 