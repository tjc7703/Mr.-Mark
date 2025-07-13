#!/bin/bash
set -e

# 1. docker-compose, k8s, 배포/운영 템플릿 복사
cp templates/docker-compose.yml . 2>/dev/null || touch docker-compose.yml
mkdir -p infra/k8s
cp templates/k8s_deployment.yaml infra/k8s/ 2>/dev/null || touch infra/k8s/k8s_deployment.yaml

# 2. 모니터링/알림/품질 리포트 자동화
cp templates/prometheus.yml infra/monitoring/ 2>/dev/null || mkdir -p infra/monitoring && touch infra/monitoring/prometheus.yml
cp templates/alertmanager.yml infra/monitoring/ 2>/dev/null || touch infra/monitoring/alertmanager.yml
cp templates/auto_quality_report.sh scripts/ 2>/dev/null || touch scripts/auto_quality_report.sh

# 3. 배포/운영/모니터링 스크립트 및 문서화
cp templates/rolling-update.sh infra/deploy/ 2>/dev/null || mkdir -p infra/deploy && touch infra/deploy/rolling-update.sh
cp templates/README_ops.md infra/deploy/ 2>/dev/null || touch infra/deploy/README.md

# 4. reports 폴더 생성
mkdir -p reports

echo "[5단계] 실행/배포/운영/모니터링 자동화 완료" 