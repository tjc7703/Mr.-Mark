# Mr. Mark 배포 상태 및 설정값

## 🚀 현재 배포 상태

### 서비스 상태 (2025-07-14)
- ✅ **Frontend (Next.js 14)**: 정상 동작 (Port: 3000)
- ✅ **Backend (FastAPI)**: 정상 동작 (Port: 8001)
- ✅ **AI Engine (FastAPI)**: 정상 동작 (Port: 9000)
- ✅ **Nginx Gateway**: 정상 동작 (Port: 8000)
- ✅ **PostgreSQL DB**: 정상 동작 (Port: 5432)
- ✅ **Redis Cache**: 정상 동작 (Port: 6379)
- ✅ **Prometheus**: 정상 동작 (Port: 9090)
- ✅ **Grafana**: 정상 동작 (Port: 3001)

### API Gateway 라우팅
- ✅ `/api/backend/health` → Backend `/health`
- ✅ `/api/ai/health` → AI Engine `/health`
- ✅ `/api/backend/*` → Backend `/*`
- ✅ `/api/ai/*` → AI Engine `/*`
- ✅ `/` → Frontend

### 헬스체크 결과
```json
{
  "backend": {"status":"healthy","timestamp":"2025-07-14T09:13:17.582334"},
  "ai-engine": {"status":"healthy","timestamp":"2025-07-14T09:13:17.603490"}
}
```

## 🔧 개발 환경 설정

### 기술 스택
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11, PostgreSQL, Redis
- **AI Engine**: FastAPI, Python 3.11, Redis
- **Gateway**: Nginx Alpine
- **Monitoring**: Prometheus, Grafana
- **Container**: Docker Compose

### 환경 변수
```bash
# Frontend
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://gateway:8000

# Backend
ENV=development
DATABASE_URL=postgresql://user:password@db:5432/mrmark
REDIS_URL=redis://redis:6379

# AI Engine
ENV=development
REDIS_URL=redis://redis:6379
```

### 포트 매핑
- Frontend: 3000
- Backend: 8001
- AI Engine: 9000
- Gateway: 8000
- PostgreSQL: 5432
- Redis: 6379
- Prometheus: 9090
- Grafana: 3001

## 📊 모니터링 설정

### Prometheus 설정
- **Targets**: Backend, AI Engine, Frontend
- **Metrics**: HTTP 요청, 응답 시간, 에러율
- **Port**: 9090

### Grafana 설정
- **Admin Password**: admin
- **Port**: 3001
- **Dashboards**: 시스템 메트릭, API 성능, 서비스 상태

## 🔄 자동화 스크립트

### Makefile 명령어
```bash
make setup      # 개발 환경 설정
make up         # 서비스 시작
make down       # 서비스 중지
make restart    # 서비스 재시작
make logs       # 로그 확인
make status     # 상태 확인
make clean      # 정리
```

### Docker Compose 명령어
```bash
docker-compose up -d          # 백그라운드 실행
docker-compose down           # 중지 및 삭제
docker-compose restart        # 재시작
docker-compose logs           # 로그 확인
docker-compose ps             # 상태 확인
```

## 🛠️ 문제 해결 이력

### 해결된 문제들
1. **Kong API Gateway 라우팅 문제**
   - 해결: Nginx Gateway로 전환
   - 결과: 모든 API 라우팅 정상 동작

2. **Docker Compose 의존성 순환**
   - 해결: depends_on 단방향 구조로 변경
   - 결과: 컨테이너 정상 기동

3. **Nginx 설정 오류**
   - 해결: add_header 위치 수정, 특별 라우팅 추가
   - 결과: 헬스체크 정상 응답

4. **API 엔드포인트 누락**
   - 해결: /health, /metrics 엔드포인트 추가
   - 결과: 모니터링 시스템 정상 동작

## 📝 최종 확인 사항

### ✅ 완료된 작업
- [x] 모든 서비스 정상 기동
- [x] API Gateway 라우팅 정상
- [x] 헬스체크 엔드포인트 정상
- [x] 모니터링 시스템 정상
- [x] 프론트엔드 렌더링 정상
- [x] 데이터베이스 연결 정상
- [x] 캐시 시스템 정상
- [x] CORS 설정 정상
- [x] 자동화 스크립트 정상
- [x] 문서화 완료

### 🔍 접속 정보
- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Backend API**: http://localhost:8001
- **AI Engine API**: http://localhost:9000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

---

**최종 업데이트**: 2025-07-14 09:13:17
**상태**: 모든 서비스 정상 동작 ✅ 