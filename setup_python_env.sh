#!/bin/bash

# Mr. Mark Python Environment Setup Script
# 이 스크립트는 Python 3.11.9 환경을 자동으로 설정합니다

set -e  # 에러 발생 시 스크립트 중단

echo "🚀 Mr. Mark Python 환경 설정을 시작합니다..."

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로그 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. pyenv 설치 확인 및 설치
check_and_install_pyenv() {
    log_info "pyenv 설치 상태를 확인합니다..."
    
    if ! command -v pyenv &> /dev/null; then
        log_info "pyenv가 설치되어 있지 않습니다. 설치를 시작합니다..."
        
        if ! command -v brew &> /dev/null; then
            log_error "Homebrew가 설치되어 있지 않습니다. 먼저 Homebrew를 설치해주세요."
            exit 1
        fi
        
        brew install pyenv
        log_success "pyenv 설치 완료"
    else
        log_success "pyenv가 이미 설치되어 있습니다."
    fi
}

# 2. pyenv 환경변수 설정
setup_pyenv_env() {
    log_info "pyenv 환경변수를 설정합니다..."
    
    # zshrc 파일에 환경변수 추가 (중복 방지)
    if ! grep -q "pyenv init" ~/.zshrc; then
        echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
        echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
        echo 'eval "$(pyenv init --path)"' >> ~/.zshrc
        echo 'eval "$(pyenv init -)"' >> ~/.zshrc
        log_success "pyenv 환경변수가 ~/.zshrc에 추가되었습니다."
    else
        log_info "pyenv 환경변수가 이미 설정되어 있습니다."
    fi
    
    # 현재 세션에 환경변수 적용
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
}

# 3. Python 3.11.9 설치
install_python() {
    log_info "Python 3.11.9 설치 상태를 확인합니다..."
    
    if ! pyenv versions | grep -q "3.11.9"; then
        log_info "Python 3.11.9를 설치합니다 (시간이 걸릴 수 있습니다)..."
        pyenv install 3.11.9
        log_success "Python 3.11.9 설치 완료"
    else
        log_success "Python 3.11.9가 이미 설치되어 있습니다."
    fi
}

# 4. 프로젝트 디렉토리 설정
setup_project_env() {
    log_info "프로젝트 디렉토리를 설정합니다..."
    
    # 현재 디렉토리가 Mr. Mark 프로젝트인지 확인
    if [[ ! -f "package.json" ]] && [[ ! -f "requirements.txt" ]] && [[ ! -f "README.md" ]]; then
        log_warning "Mr. Mark 프로젝트 디렉토리가 아닌 것 같습니다."
        log_info "올바른 프로젝트 디렉토리로 이동해주세요."
        exit 1
    fi
    
    # 로컬 Python 버전 설정
    pyenv local 3.11.9
    log_success "프로젝트에 Python 3.11.9가 설정되었습니다."
}

# 5. 가상환경 생성 및 활성화
setup_venv() {
    log_info "가상환경을 설정합니다..."
    
    if [[ ! -d ".venv" ]]; then
        log_info "가상환경을 생성합니다..."
        python -m venv .venv
        log_success "가상환경 생성 완료"
    else
        log_info "가상환경이 이미 존재합니다."
    fi
    
    # 가상환경 활성화
    source .venv/bin/activate
    log_success "가상환경이 활성화되었습니다."
}

# 6. pip 업그레이드 및 기본 패키지 설치
install_packages() {
    log_info "pip를 최신 버전으로 업그레이드합니다..."
    pip install --upgrade pip setuptools wheel
    
    log_info "기본 패키지들을 설치합니다..."
    
    # requirements.txt가 있으면 설치
    if [[ -f "requirements.txt" ]]; then
        log_info "requirements.txt에서 패키지를 설치합니다..."
        pip install -r requirements.txt
    else
        log_info "기본 필수 패키지들을 설치합니다..."
        pip install torch==2.1.2
        pip install aiohttp==3.8.6
        pip install scikit-learn==1.3.2
        pip install pandas==2.1.4
        pip install numpy==1.24.3
        pip install matplotlib==3.7.2
        pip install seaborn==0.12.2
        pip install jupyter==1.0.0
        pip install fastapi==0.104.1
        pip install uvicorn==0.24.0
        pip install python-multipart==0.0.6
        pip install python-dotenv==1.0.0
        pip install requests==2.31.0
        pip install beautifulsoup4==4.12.2
        pip install lxml==4.9.3
        pip install feedparser==6.0.10
        pip install textblob==0.17.1
        pip install nltk==3.8.1
        pip install transformers==4.35.2
        pip install torchvision==0.16.2
        pip install torchaudio==2.1.2
        pip install prophet==1.1.4
        pip install plotly==5.17.0
        pip install dash==2.14.2
        pip install dash-bootstrap-components==1.5.0
        pip install sqlalchemy==2.0.23
        pip install alembic==1.12.1
        pip install psycopg2-binary==2.9.9
        pip install redis==5.0.1
        pip install celery==5.3.4
        pip install flower==2.0.1
        pip install prometheus-client==0.19.0
        pip install pytest==7.4.3
        pip install black==23.11.0
        pip install flake8==6.1.0
        pip install mypy==1.7.1
        pip install pre-commit==3.5.0
    fi
    
    log_success "패키지 설치 완료"
}

# 7. 환경 확인
verify_environment() {
    log_info "환경 설정을 확인합니다..."
    
    echo ""
    echo "=== 환경 확인 결과 ==="
    echo "Python 버전: $(python --version)"
    echo "pip 버전: $(pip --version)"
    echo "가상환경: $(which python)"
    echo "설치된 패키지 수: $(pip list | wc -l)"
    echo "====================="
    echo ""
    
    # Python 버전 확인
    if [[ $(python --version) == *"3.11.9"* ]]; then
        log_success "Python 3.11.9가 정상적으로 설정되었습니다."
    else
        log_error "Python 버전이 3.11.9가 아닙니다."
        exit 1
    fi
    
    # 가상환경 확인
    if [[ $(which python) == *".venv"* ]]; then
        log_success "가상환경이 정상적으로 활성화되었습니다."
    else
        log_error "가상환경이 활성화되지 않았습니다."
        exit 1
    fi
}

# 8. 다음 단계 안내
show_next_steps() {
    echo ""
    log_success "🎉 Python 환경 설정이 완료되었습니다!"
    echo ""
    echo "다음 단계:"
    echo "1. 터미널을 새로 열거나 다음 명령어를 실행하세요:"
    echo "   source ~/.zshrc"
    echo ""
    echo "2. 프로젝트 디렉토리로 이동하세요:"
    echo "   cd /Users/richardlee/Desktop/My\ Agent\ AI/Mr.\ Mark"
    echo ""
    echo "3. 가상환경을 활성화하세요:"
    echo "   source .venv/bin/activate"
    echo ""
    echo "4. 데이터 파이프라인을 실행하세요:"
    echo "   python scripts/run_pipeline.py"
    echo ""
    echo "5. 백엔드 서버를 실행하세요:"
    echo "   python backend/main.py"
    echo ""
    echo "6. 프론트엔드를 실행하세요:"
    echo "   cd frontend && npm run dev"
    echo ""
}

# 메인 실행 함수
main() {
    echo "=========================================="
    echo "    Mr. Mark Python 환경 설정 스크립트"
    echo "=========================================="
    echo ""
    
    check_and_install_pyenv
    setup_pyenv_env
    install_python
    setup_project_env
    setup_venv
    install_packages
    verify_environment
    show_next_steps
    
    echo ""
    log_success "모든 설정이 완료되었습니다! 🚀"
}

# 스크립트 실행
main "$@" 