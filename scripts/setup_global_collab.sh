#!/bin/bash
set -e

# 1. 다국어/다지역 협업 템플릿 복사
cp templates/globalization.md docs/ 2>/dev/null || mkdir -p docs && touch docs/globalization.md
cp templates/auto_translate.py scripts/ 2>/dev/null || touch scripts/auto_translate.py

# 2. KPI/피드백/실험/개선 자동화 스크립트 복사
cp templates/auto_kpi_report.sh scripts/ 2>/dev/null || touch scripts/auto_kpi_report.sh
cp templates/generate_kpi_report.py scripts/ 2>/dev/null || touch scripts/generate_kpi_report.py
cp templates/auto_improvement_report.py scripts/ 2>/dev/null || touch scripts/auto_improvement_report.py

# 3. 글로벌 협업/지속적 개선 문서화
cp templates/README_global_collab.md docs/ 2>/dev/null || touch docs/README_global_collab.md

echo "[6단계] 글로벌 협업/지속적 개선 자동화 완료" 