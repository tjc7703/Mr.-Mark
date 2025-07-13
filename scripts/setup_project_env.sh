#!/bin/bash
set -e

# 1. 폴더/파일 구조 생성
mkdir -p src data notebooks tests docs infra scripts .devcontainer

# 2. README, CONTRIBUTING, 코드 스타일 가이드 템플릿 복사/생성
cp templates/README.md ./README.md 2>/dev/null || touch README.md
touch CONTRIBUTING.md
cp templates/.editorconfig . 2>/dev/null || touch .editorconfig

# 3. VS Code devcontainer, settings, 추천 확장
mkdir -p .devcontainer
cp templates/devcontainer.json .devcontainer/ 2>/dev/null || touch .devcontainer/devcontainer.json
cp templates/settings.json .vscode/ 2>/dev/null || mkdir -p .vscode && touch .vscode/settings.json

# 4. pre-commit, Makefile, .gitignore 등 복사/생성
cp templates/.pre-commit-config.yaml . 2>/dev/null || touch .pre-commit-config.yaml
touch Makefile .gitignore

# 5. 기본 환경설정/패키지 설치(예시)
# pip install -r requirements.txt
# npm install

# 6. 기본 문서화
cp templates/CONTRIBUTING.md . 2>/dev/null || echo "# 기여 가이드" > CONTRIBUTING.md

echo "[1단계] 프로젝트 구조/환경/코드 스타일/문서 표준화 완료" 