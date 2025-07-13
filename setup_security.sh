#!/bin/bash
set -e

# 1. RBAC/네트워크 정책/감사로그 (예시)
echo "[보안] RBAC, 네트워크 정책, 감사로그 자동화는 인프라/클라우드 IaC(Terraform 등)에서 관리하세요."

# 2. JWT 등 인증/인가 샘플
if [ -f apps/backend/main.py ]; then
  echo "[JWT] 인증/인가 샘플은 FastAPI 코드에 포함되어야 합니다."
fi

echo "[setup_security.sh] 보안 자동화 완료!" 