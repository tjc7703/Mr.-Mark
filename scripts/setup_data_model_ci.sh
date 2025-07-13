#!/bin/bash
set -e

# 1. data 폴더 구조 및 ETL/수집/전처리 템플릿
mkdir -p data/pipelines data/lake data/warehouse data/marts
cp templates/data_pipeline.py data/pipelines/ 2>/dev/null || touch data/pipelines/data_pipeline.py
cp templates/README_data.md data/README.md 2>/dev/null || touch data/README.md

# 2. src/models 기본 템플릿, 학습/추론/평가, 샘플 데이터/문서화
mkdir -p src/models
cp templates/model_base.py src/models/ 2>/dev/null || touch src/models/base_model.py
cp templates/README_models.md src/models/README.md 2>/dev/null || touch src/models/README.md

# 3. CI 템플릿 복사
mkdir -p .github/workflows
cp templates/ci_template.yml .github/workflows/ci.yml 2>/dev/null || touch .github/workflows/ci.yml

# 4. 샘플 데이터/스크립트/문서화
cp templates/sample_data.csv data/lake/ 2>/dev/null || touch data/lake/sample_data.csv

# 5. requirements.txt, 환경설정
cp templates/requirements.txt . 2>/dev/null || touch requirements.txt

# 6. 문서화
cp templates/README_data.md data/README.md 2>/dev/null || touch data/README.md

echo "[2단계] 데이터/모델/CI 템플릿 및 문서화 완료" 