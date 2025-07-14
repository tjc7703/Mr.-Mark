# 🛠️ Mr. Mark 개발 환경 설정 가이드

## 📋 필수 요구사항

### 시스템 요구사항
- **OS**: macOS 10.15+, Ubuntu 20.04+, Windows 10+
- **RAM**: 최소 8GB (권장 16GB)
- **Storage**: 최소 10GB 여유 공간
- **Docker**: Docker Desktop 4.0+
- **Git**: Git 2.30+

### 소프트웨어 요구사항
- **Python**: 3.11+
- **Node.js**: 18+
- **Docker**: 24.0+
- **Docker Compose**: 2.0+

## 🚀 초기 설정

### 1. 저장소 클론
```bash
git clone https://github.com/tjc7703/Mr.-Mark.git
cd Mr.-Mark
```

### 2. Python 가상환경 설정
```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. Node.js 의존성 설치
```bash
# 프론트엔드 의존성
cd apps/frontend
npm install
cd ../..

# 또는 yarn 사용
cd apps/frontend
yarn install
cd ../..
```

## 🔧 개발 환경 구성

### 환경 변수 설정

#### 1. Frontend 환경 변수
```bash
# apps/frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_ENVIRONMENT=development
```

#### 2. Backend 환경 변수
```bash
# apps/backend/.env
ENVIRONMENT=development
DATABASE_URL=postgresql://user:password@localhost:5432/mrmark
REDIS_URL=redis://localhost:6379
API_KEY=your_api_key_here
```

#### 3. AI Engine 환경 변수
```bash
# apps/ai-engine/.env
ENVIRONMENT=development
REDIS_URL=redis://localhost:6379
MODEL_PATH=/app/models
```

### Docker 설정

#### 1. Docker Compose 환경 변수
```bash
# .env
POSTGRES_USER=mrmark
POSTGRES_PASSWORD=password123
POSTGRES_DB=mrmark
REDIS_PASSWORD=redis123
GRAFANA_ADMIN_PASSWORD=admin
```

#### 2. Docker 네트워크 설정
```bash
# Docker 네트워크 생성
docker network create mrmark-network
```

## 🏃‍♂️ 개발 서버 실행

### 1. 전체 서비스 실행 (권장)
```bash
# 모든 서비스 시작
docker-compose up -d

# 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f
```

### 2. 개별 서비스 개발 모드
```bash
# 프론트엔드 개발 서버
cd apps/frontend
npm run dev

# 백엔드 개발 서버
cd apps/backend
uvicorn main:app --reload --host 0.0.0.0 --port 8001

# AI 엔진 개발 서버
cd apps/ai-engine
uvicorn app:app --reload --host 0.0.0.0 --port 9000
```

## 🔍 디버깅 및 로그

### 1. 서비스별 로그 확인
```bash
# 프론트엔드 로그
docker-compose logs frontend

# 백엔드 로그
docker-compose logs backend

# AI 엔진 로그
docker-compose logs ai-engine

# Gateway 로그
docker-compose logs gateway
```

### 2. 실시간 로그 모니터링
```bash
# 모든 서비스 로그
docker-compose logs -f

# 특정 서비스 로그
docker-compose logs -f [service-name]
```

### 3. 디버깅 도구
```bash
# 컨테이너 내부 접속
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec ai-engine bash

# 포트 확인
docker-compose port backend 8001
docker-compose port frontend 3000
```

## 🧪 테스트 실행

### 1. API 테스트
```bash
# 헬스체크
curl http://localhost:8001/health
curl http://localhost:9000/health

# API 엔드포인트 테스트
curl http://localhost:8000/feed/today
curl http://localhost:8000/trend
curl http://localhost:8000/ai/feedback
```

### 2. 프론트엔드 테스트
```bash
cd apps/frontend
npm run test
npm run test:watch
```

### 3. 백엔드 테스트
```bash
cd apps/backend
pytest
pytest -v
pytest --cov
```

## 📊 모니터링 설정

### 1. Prometheus 설정
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8001']
  - job_name: 'ai-engine'
    static_configs:
      - targets: ['ai-engine:9000']
```

### 2. Grafana 대시보드
- **URL**: http://localhost:3001
- **Username**: admin
- **Password**: admin
- **데이터소스**: Prometheus (http://prometheus:9090)

## 🔧 개발 도구

### 1. VS Code 설정
```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/node_modules": true,
    "**/.next": true
  }
}
```

### 2. Pre-commit 훅
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

## 🚨 문제 해결

### 1. 포트 충돌
```bash
# 사용 중인 포트 확인
lsof -i :3000
lsof -i :8001
lsof -i :9000

# 포트 해제
kill -9 [PID]
```

### 2. Docker 문제
```bash
# Docker 캐시 정리
docker system prune -a

# 컨테이너 재시작
docker-compose down
docker-compose up -d
```

### 3. 의존성 문제
```bash
# Python 의존성 재설치
pip install -r requirements.txt --force-reinstall

# Node.js 의존성 재설치
cd apps/frontend
rm -rf node_modules package-lock.json
npm install
```

### 4. 데이터베이스 문제
```bash
# 데이터베이스 재시작
docker-compose restart db

# 데이터베이스 초기화
docker-compose exec db psql -U mrmark -d mrmark -f /docker-entrypoint-initdb.d/init.sql
```

## 📝 개발 체크리스트

### ✅ 초기 설정
- [ ] Git 저장소 클론
- [ ] Python 가상환경 설정
- [ ] Node.js 의존성 설치
- [ ] 환경 변수 설정
- [ ] Docker 설치 및 설정

### ✅ 서비스 실행
- [ ] 모든 서비스 정상 기동
- [ ] API 엔드포인트 응답 확인
- [ ] 프론트엔드 렌더링 확인
- [ ] 데이터베이스 연결 확인
- [ ] 모니터링 시스템 확인

### ✅ 개발 환경
- [ ] VS Code 설정 완료
- [ ] Pre-commit 훅 설정
- [ ] 테스트 환경 구성
- [ ] 디버깅 도구 설정
- [ ] 로그 모니터링 설정

---

**마지막 업데이트**: 2025-07-14  
**상태**: 🟢 개발 환경 완전 구성 