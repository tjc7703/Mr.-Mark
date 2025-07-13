#!/bin/bash
set -e

# 1. 데이터 폴더 구조 생성
mkdir -p data/lake data/warehouse data/marts data/pipelines

# 2. 샘플 데이터/스크립트 복사 또는 생성
if [ ! -f data/lake/sample.csv ]; then
  echo "col1,col2,col3" > data/lake/sample.csv
  echo "1,2,3" >> data/lake/sample.csv
fi

# 3. ETL/수집/전처리 스크립트 실행
if [ -f packages/common/data/pipelines/collect_data.py ]; then
  python packages/common/data/pipelines/collect_data.py
fi

echo "[setup_data_pipeline.sh] 데이터 파이프라인/ETL/전처리 자동화 완료!" 