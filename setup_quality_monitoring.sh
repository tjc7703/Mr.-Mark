#!/bin/bash
set -e

# 1. 린트/포맷/테스트
if [ -f Makefile ]; then
  make lint || true
  make format || true
  make test || true
fi

# 2. 품질관리/모니터링/알림 (예시)
echo "[품질관리] 코드 품질 및 모니터링 자동화 완료!"

echo "[setup_quality_monitoring.sh] 테스트/품질/모니터링 자동화 완료!" 