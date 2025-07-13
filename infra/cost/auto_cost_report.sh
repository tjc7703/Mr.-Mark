#!/bin/bash
# AWS 비용 리포트 자동화 예시
aws ce get-cost-and-usage --time-period Start=$(date +%Y-%m-01),End=$(date +%Y-%m-%d) --granularity MONTHLY --metrics "UnblendedCost" > cost_report_$(date +%Y%m%d).json 