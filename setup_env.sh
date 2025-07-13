#!/bin/bash
set -e

# 1. pyenv 및 Python 설치
if ! command -v pyenv &> /dev/null; then
  echo "[pyenv] 설치 중..."
  curl https://pyenv.run | bash
  export PATH="$HOME/.pyenv/bin:$PATH"
  eval "$(pyenv init -)"
  eval "$(pyenv virtualenv-init -)"
fi
pyenv install -s 3.11.9
pyenv global 3.11.9

# 2. venv 및 requirements
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || true

# 3. pre-commit
pip install pre-commit
pre-commit install

# 4. Jupyter Lab, ipykernel
pip install jupyterlab ipykernel
python -m ipykernel install --user --name=mrmark

# 5. VSCode devcontainer
if [ -d ".devcontainer" ]; then
  echo "VSCode devcontainer 설정 적용됨."
fi

echo "[setup_env.sh] Python/AI/ML 환경 자동화 완료!" 