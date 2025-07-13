# 🐍 Mr. Mark Python 환경 설정 가이드

## 🚀 빠른 시작

### 1. 자동화 스크립트 실행
```bash
./setup_python_env.sh
```

이 스크립트가 다음을 자동으로 처리합니다:
- ✅ pyenv 설치 및 설정
- ✅ Python 3.11.9 설치
- ✅ 가상환경 생성 및 활성화
- ✅ 모든 필수 패키지 설치
- ✅ 환경 검증

### 2. 수동 설정 (스크립트 실행이 안 될 경우)

#### pyenv 설치
```bash
brew install pyenv
```

#### 환경변수 설정
```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
source ~/.zshrc
```

#### Python 3.11.9 설치
```bash
pyenv install 3.11.9
cd /Users/richardlee/Desktop/My\ Agent\ AI/Mr.\ Mark
pyenv local 3.11.9
```

#### 가상환경 설정
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## 🔧 문제 해결

### Python 버전 확인
```bash
python --version  # 3.11.9가 나와야 함
```

### 가상환경 활성화 확인
```bash
which python  # .venv/bin/python이 나와야 함
```

### 패키지 설치 확인
```bash
pip list | grep torch  # torch가 설치되어 있어야 함
```

### 일반적인 문제들

#### 1. pyenv 명령어를 찾을 수 없음
```bash
source ~/.zshrc
# 또는 터미널을 새로 열기
```

#### 2. Python 설치 중 에러
```bash
# Xcode Command Line Tools 설치
xcode-select --install

# 또는 Homebrew 업데이트
brew update
```

#### 3. torch 설치 실패
```bash
# CPU 버전으로 설치
pip install torch==2.1.2+cpu -f https://download.pytorch.org/whl/torch_stable.html
```

## 📦 주요 패키지들

### Data Science & AI
- **torch**: PyTorch 딥러닝 프레임워크
- **scikit-learn**: 머신러닝 라이브러리
- **pandas**: 데이터 분석 라이브러리
- **transformers**: HuggingFace 트랜스포머 모델

### Web & API
- **fastapi**: 현대적인 웹 API 프레임워크
- **uvicorn**: ASGI 서버
- **aiohttp**: 비동기 HTTP 클라이언트

### Data Collection
- **beautifulsoup4**: 웹 스크래핑
- **feedparser**: RSS 피드 파싱
- **requests**: HTTP 요청

### Visualization
- **matplotlib**: 기본 플롯 라이브러리
- **seaborn**: 통계 시각화
- **plotly**: 인터랙티브 시각화
- **dash**: 웹 대시보드

## 🎯 다음 단계

환경 설정이 완료되면:

1. **데이터 파이프라인 실행**
   ```bash
   python scripts/run_pipeline.py
   ```

2. **백엔드 서버 실행**
   ```bash
   python backend/main.py
   ```

3. **프론트엔드 실행**
   ```bash
   cd frontend && npm run dev
   ```

## 📝 참고사항

- Python 3.11.9는 torch와 다른 AI 라이브러리들과 최적의 호환성을 제공합니다
- 모든 패키지 버전은 호환성을 위해 고정되어 있습니다
- 가상환경(.venv)을 사용하여 프로젝트별 의존성을 격리합니다

---

**문제가 발생하면 언제든 말씀해 주세요!** 🚀 