#!/bin/bash
# KPI 자동 리포트 생성 예시
python scripts/generate_kpi_report.py > reports/kpi_report_$(date +%Y%m%d).txt 