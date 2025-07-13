#!/bin/bash
set -e

# 1. 이슈/PR 템플릿 복사
mkdir -p .github/ISSUE_TEMPLATE
cp -n docs/ISSUE_TEMPLATE.md .github/ISSUE_TEMPLATE/ 2>/dev/null || true
cp -n docs/PULL_REQUEST_TEMPLATE.md .github/ 2>/dev/null || true

# 2. 다국어 문서화/Notion/Wiki 연동 (예시)
echo "[협업] 다국어 문서화, Notion/Wiki 연동은 별도 API/스크립트로 관리하세요."

echo "[setup_collaboration.sh] 글로벌 협업/문서화 자동화 완료!" 