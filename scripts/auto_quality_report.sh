#!/bin/bash
# 품질 리포트 자동 생성
python data/pipelines/quality_checks.py > reports/quality_report_$(date +%Y%m%d).txt 