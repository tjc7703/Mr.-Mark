#!/bin/bash

############################################################
# [파이썬 버전 호환 문제 해결]
#
# 이 스크립트는 pyenv를 이용해 원하는 Python 버전을 설치하고,
# 프로젝트에 로컬 버전으로 지정하며,
# 가상환경(.venv) 생성 및 필수 패키지 설치까지 자동화합니다.
#
# - pyenv가 없으면 자동 설치
# - 환경변수 자동 설정
# - requirements.txt가 있으면 패키지 자동 설치
# - 모든 과정에서 에러 발생 시 중단
#
# 원하는 Python 버전/패키지로 수정해서 재사용 가능!
############################################################

set -e

PYTHON_VERSION="3.11.9"  # <--- 필요시 원하는 버전으로 변경

# pyenv 설치
if ! command -v pyenv &> /dev/null; then
  echo "[INFO] pyenv가 설치되어 있지 않습니다. Homebrew로 설치합니다."
  if ! command -v brew &> /dev/null; then
    echo "[ERROR] Homebrew가 필요합니다. 먼저 설치해주세요."
    exit 1
  fi
  brew install pyenv
else
  echo "[INFO] pyenv가 이미 설치되어 있습니다."
fi

# pyenv 환경변수 설정 (zsh 기준)
if ! grep -q "pyenv init" ~/.zshrc; then
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
  echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
  echo 'eval "$(pyenv init -)"' >> ~/.zshrc
fi
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"

# Python 버전 설치
if ! pyenv versions | grep -q "$PYTHON_VERSION"; then
  echo "[INFO] Python $PYTHON_VERSION 설치 중..."
  pyenv install $PYTHON_VERSION
else
  echo "[INFO] Python $PYTHON_VERSION가 이미 설치되어 있습니다."
fi

# 프로젝트 폴더에 로컬 버전 지정
pyenv local $PYTHON_VERSION

echo "[INFO] python --version: $(python --version)"

# 가상환경 생성 및 활성화
if [[ ! -d ".venv" ]]; then
  python -m venv .venv
  echo "[INFO] 가상환경(.venv) 생성 완료"
fi
source .venv/bin/activate

echo "[INFO] 가상환경 활성화: $(which python)"

# pip 업그레이드 및 패키지 설치
pip install --upgrade pip setuptools wheel
if [[ -f "requirements.txt" ]]; then
  pip install -r requirements.txt
  echo "[INFO] requirements.txt로 패키지 설치 완료"
else
  echo "[INFO] requirements.txt가 없어 패키지 설치는 건너뜁니다."
fi

echo "[SUCCESS] 파이썬 버전 호환 환경 구축이 완료되었습니다!" 