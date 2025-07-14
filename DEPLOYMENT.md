# Mr. Mark 프로젝트 배포 가이드

## 🚀 빠른 시작

### 1. 환경 준비
```bash
# 필수 소프트웨어 설치
- Docker Desktop
- Git
- Node.js 20+
- Python 3.11+

# 프로젝트 클론
git clone https://github.com/your-username/mr-mark.git
cd mr-mark
```

### 2. 개발 환경 시작
```bash
# 전체 서비스 시작
docker-compose up -d

# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f
```

### 3. 접속 확인
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/backend
- **AI Engine**: http://localhost:8000/api/ai
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

## 🔧 환경 설정

### 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# 환경 변수 편집
nano .env
```

### 주요 환경 변수
```env
# 데이터베이스
DATABASE_URL=postgresql://user:password@db:5432/mrmark
REDIS_URL=redis://redis:6379

# API 설정
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here

# 외부 서비스
OPENAI_API_KEY=your_openai_key
GOOGLE_TRENDS_API_KEY=your_google_key
```

## 🐳 Docker 배포

### 개발 환경
```bash
# 개발용 빌드
docker-compose up --build

# 백그라운드 실행
docker-compose up -d

# 특정 서비스만 실행
docker-compose up -d frontend backend
```

### 프로덕션 환경
```bash
# 프로덕션 빌드
docker-compose -f docker-compose.prod.yml up -d

# 스케일링
docker-compose up -d --scale backend=3 --scale ai-engine=2
```

## 📊 모니터링 설정

### Prometheus 설정
```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'mr-mark'
    static_configs:
      - targets: ['backend:8001', 'ai-engine:9000', 'frontend:3000']
```

### Grafana 대시보드
1. Grafana 접속: http://localhost:3001
2. 로그인: admin/admin
3. Prometheus 데이터 소스 추가
4. 대시보드 임포트

## 🔒 보안 설정

### SSL/TLS 설정
```bash
# SSL 인증서 생성
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx.key -out nginx.crt

# Kong SSL 설정
curl -X POST http://localhost:8001/certificates \
  -d "cert=@nginx.crt" \
  -d "key=@nginx.key" \
  -d "snis=localhost"
```

### 방화벽 설정
```bash
# 필요한 포트만 열기
sudo ufw allow 3000  # Frontend
sudo ufw allow 8000  # API Gateway
sudo ufw allow 5432  # PostgreSQL
sudo ufw allow 6379  # Redis
```

## 🔄 CI/CD 파이프라인

### GitHub Actions 설정
```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and deploy
        run: |
          docker-compose -f docker-compose.prod.yml up -d
```

## 🚨 문제 해결

### 일반적인 문제들

#### 1. 포트 충돌
```bash
# 사용 중인 포트 확인
lsof -i :3000
lsof -i :8000

# 프로세스 종료
kill -9 [PID]
```

#### 2. Docker 이미지 빌드 실패
```bash
# 캐시 삭제 후 재빌드
docker-compose build --no-cache

# Docker 시스템 정리
docker system prune -a
```

#### 3. 데이터베이스 연결 실패
```bash
# PostgreSQL 컨테이너 상태 확인
docker-compose logs db

# 데이터베이스 재시작
docker-compose restart db
```

#### 4. 메모리 부족
```bash
# Docker 메모리 제한 설정
# Docker Desktop > Settings > Resources > Memory: 4GB+
```

### 로그 확인
```bash
# 전체 로그
docker-compose logs

# 특정 서비스 로그
docker-compose logs backend
docker-compose logs ai-engine

# 실시간 로그
docker-compose logs -f
```

## 📈 성능 최적화

### Docker 최적화
```dockerfile
# 멀티스테이지 빌드 사용
FROM python:3.11-slim AS base
FROM base AS deps
# 의존성 설치
FROM base AS runtime
# 런타임만 복사
```

### 데이터베이스 최적화
```sql
-- 인덱스 생성
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_campaigns_user_id ON campaigns(user_id);

-- 쿼리 최적화
EXPLAIN ANALYZE SELECT * FROM campaigns WHERE user_id = 1;
```

### 캐싱 전략
```python
# Redis 캐싱 구현
import redis
import json

redis_client = redis.Redis(host='redis', port=6379, db=0)

def get_cached_data(key):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)
    return None
```

## 🔄 백업 및 복구

### 데이터베이스 백업
```bash
# PostgreSQL 백업
docker-compose exec db pg_dump -U user mrmark > backup.sql

# Redis 백업
docker-compose exec redis redis-cli BGSAVE
```

### 자동 백업 스크립트
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose exec db pg_dump -U user mrmark > backup_$DATE.sql
aws s3 cp backup_$DATE.sql s3://mr-mark-backups/
```

## 🎯 프로덕션 체크리스트

### 배포 전 확인사항
- [ ] 모든 테스트 통과
- [ ] 환경 변수 설정 완료
- [ ] SSL 인증서 설치
- [ ] 모니터링 설정 완료
- [ ] 백업 시스템 구축
- [ ] 로그 수집 설정
- [ ] 알림 시스템 설정

### 배포 후 확인사항
- [ ] 모든 서비스 정상 동작
- [ ] API 응답 시간 확인
- [ ] 데이터베이스 연결 확인
- [ ] 모니터링 대시보드 확인
- [ ] 로그 정상 수집 확인
- [ ] 백업 정상 동작 확인 