#!/bin/bash

# Mr. Mark 프로젝트 자동 설정 스크립트

set -e  # 오류 발생 시 스크립트 중단

echo "🚀 Mr. Mark 프로젝트 자동 설정 시작..."

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

# 필수 도구 확인
check_requirements() {
    log_info "필수 도구 확인 중..."
    
    # Docker 확인
    if ! command -v docker &> /dev/null; then
        log_error "Docker가 설치되지 않았습니다. https://docker.com 에서 설치하세요."
        exit 1
    fi
    
    # Docker Compose 확인
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose가 설치되지 않았습니다."
        exit 1
    fi
    
    # Git 확인
    if ! command -v git &> /dev/null; then
        log_error "Git이 설치되지 않았습니다."
        exit 1
    fi
    
    log_success "필수 도구 확인 완료"
}

# 환경 정리
cleanup_environment() {
    log_info "기존 환경 정리 중..."
    
    # 기존 컨테이너 중지 및 제거
    docker-compose down -v --remove-orphans 2>/dev/null || true
    
    # Docker 시스템 정리
    docker system prune -f
    
    # 로그 파일 정리
    rm -f *.log nohup.out 2>/dev/null || true
    
    log_success "환경 정리 완료"
}

# 의존성 설치
install_dependencies() {
    log_info "의존성 설치 중..."
    
    # Python 가상환경 생성
    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
        log_info "Python 가상환경 생성 완료"
    fi
    
    # 가상환경 활성화
    source .venv/bin/activate
    
    # Python 의존성 설치
    pip install --upgrade pip
    pip install -r requirements.txt
    
    log_success "의존성 설치 완료"
}

# Docker 이미지 빌드
build_images() {
    log_info "Docker 이미지 빌드 중..."
    
    # 캐시 없이 빌드
    docker-compose build --no-cache
    
    log_success "Docker 이미지 빌드 완료"
}

# 서비스 시작
start_services() {
    log_info "서비스 시작 중..."
    
    # 백그라운드에서 서비스 시작
    docker-compose up -d
    
    # 서비스 상태 확인
    sleep 10
    
    # 헬스체크
    check_health
    
    log_success "서비스 시작 완료"
}

# 헬스체크
check_health() {
    log_info "서비스 헬스체크 중..."
    
    # Backend 헬스체크
    if curl -f http://localhost:8000/api/backend/health >/dev/null 2>&1; then
        log_success "Backend 서비스 정상"
    else
        log_warning "Backend 서비스 응답 없음"
    fi
    
    # AI Engine 헬스체크
    if curl -f http://localhost:8000/api/ai/health >/dev/null 2>&1; then
        log_success "AI Engine 서비스 정상"
    else
        log_warning "AI Engine 서비스 응답 없음"
    fi
    
    # Frontend 헬스체크
    if curl -f http://localhost:3000 >/dev/null 2>&1; then
        log_success "Frontend 서비스 정상"
    else
        log_warning "Frontend 서비스 응답 없음"
    fi
}

# 데이터베이스 초기화
init_database() {
    log_info "데이터베이스 초기화 중..."
    
    # PostgreSQL 컨테이너가 준비될 때까지 대기
    until docker-compose exec db pg_isready -U user -d mrmark; do
        log_info "데이터베이스 준비 대기 중..."
        sleep 2
    done
    
    # 초기화 스크립트 실행
    docker-compose exec -T db psql -U user -d mrmark -f /docker-entrypoint-initdb.d/init.sql
    
    log_success "데이터베이스 초기화 완료"
}

# 모니터링 설정
setup_monitoring() {
    log_info "모니터링 설정 중..."
    
    # Prometheus 설정 확인
    if [ -f "prometheus.yml" ]; then
        log_success "Prometheus 설정 확인"
    else
        log_warning "Prometheus 설정 파일 없음"
    fi
    
    # Grafana 대시보드 정보
    log_info "모니터링 대시보드:"
    echo "  - Grafana: http://localhost:3001 (admin/admin)"
    echo "  - Prometheus: http://localhost:9090"
}

# 접속 정보 표시
show_access_info() {
    log_success "설정 완료!"
    echo ""
    echo "🔗 접속 정보:"
    echo "  - Frontend: http://localhost:3000"
    echo "  - Backend API: http://localhost:8000/api/backend"
    echo "  - AI Engine: http://localhost:8000/api/ai"
    echo "  - Grafana: http://localhost:3001 (admin/admin)"
    echo "  - Prometheus: http://localhost:9090"
    echo ""
    echo "📋 유용한 명령어:"
    echo "  - 서비스 상태 확인: make status"
    echo "  - 로그 확인: make logs"
    echo "  - 헬스체크: make health"
    echo "  - 서비스 중지: make down"
    echo "  - 서비스 재시작: make restart"
    echo ""
    echo "🎉 Mr. Mark 프로젝트가 성공적으로 설정되었습니다!"
}

# 메인 실행
main() {
    echo "=========================================="
    echo "    Mr. Mark 프로젝트 자동 설정"
    echo "=========================================="
    echo ""
    
    check_requirements
    cleanup_environment
    install_dependencies
    build_images
    start_services
    init_database
    setup_monitoring
    show_access_info
}

# 스크립트 실행
main "$@" 