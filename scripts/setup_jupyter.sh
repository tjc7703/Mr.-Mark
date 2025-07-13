#!/bin/bash
set -e

# 1. Jupyter Lab, ipykernel 설치 (venv 환경 가정)
pip install jupyterlab ipykernel
python -m ipykernel install --user --name=mrmark

# 2. notebooks 폴더 및 예시 노트북 생성
mkdir -p notebooks
cp templates/example_notebook.ipynb notebooks/ 2>/dev/null || touch notebooks/example_notebook.ipynb

# 3. Jupyter Lab 환경설정
cp templates/jupyter_lab_config.py . 2>/dev/null || touch jupyter_lab_config.py

echo "[3단계] Jupyter Lab, ipykernel, notebook 자동화 완료" 