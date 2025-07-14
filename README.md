# Mr. Mark - AI 기반 마케팅 마스터리 플랫폼

[![Mr. Mark](https://img.shields.io/badge/Mr.%20Mark-AI%20Marketing%20Platform-blue?style=for-the-badge&logo=robot)](https://github.com/tjc7703/Mr.-Mark)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)](https://docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.0.0-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![Status](https://img.shields.io/badge/Status-All%20Services%20Healthy-green?style=flat-square)](https://github.com/tjc7703/Mr.-Mark)

> 🌟 **세계 최고 수준의 AI 기반 마케팅 마스터리 플랫폼**  
> 실시간 트렌드 분석, 30개 SNS 자동화, AI 기반 콘텐츠 생성, 실시간 모니터링

## 🚀 빠른 시작

### 1. 자동 설정 (권장)
```bash
# 프로젝트 클론
git clone https://github.com/tjc7703/Mr.-Mark.git
cd Mr.-Mark

# 자동 설정 실행
./scripts/auto_setup.sh
```

### 2. 수동 설정
```bash
# 개발 환경 설정
make setup

# 서비스 시작
make up

# 상태 확인
make status
```

## 📊 현재 상태

### ✅ 모든 서비스 정상 동작
- **Frontend**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Backend API**: http://localhost:8001
- **AI Engine API**: http://localhost:9000
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3001 (admin/admin)

### 🔧 기술 스택
- **Frontend**: Next.js 14, React 18, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python 3.11, PostgreSQL, Redis
- **AI Engine**: FastAPI, Python 3.11, Redis
- **Gateway**: Nginx Alpine
- **Monitoring**: Prometheus, Grafana
- **Container**: Docker Compose

## 🏗️ 아키텍처

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   AI Engine     │
│   (Next.js 14)  │    │   (FastAPI)     │    │   (FastAPI)     │
│   Port: 3000    │    │   Port: 8001    │    │   Port: 9000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Nginx Gateway  │
                    │   Port: 8000    │
                    └─────────────────┘
                                 │
         ┌───────────────────────┼───────────────────────┐
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Redis       │    │   Prometheus    │
│   Port: 5432    │    │   Port: 6379    │    │   Port: 9090    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                              ┌─────────────────┐
                                              │    Grafana       │
                                              │   Port: 3001    │
                                              └─────────────────┘
```

## 🔄 API 라우팅

### Gateway를 통한 API 접근
```bash
# 헬스체크
curl http://localhost:8000/api/backend/health
curl http://localhost:8000/api/ai/health

# 백엔드 API
curl http://localhost:8000/api/backend/feed/today
curl http://localhost:8000/api/backend/trend

# AI 엔진 API
curl http://localhost:8000/api/ai/predict
curl http://localhost:8000/api/ai/analyze
```

## 🛠️ 개발 명령어

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

## 📊 모니터링

### Prometheus
- **URL**: http://localhost:9090
- **Targets**: Backend, AI Engine, Frontend
- **Metrics**: HTTP 요청, 응답 시간, 에러율

### Grafana
- **URL**: http://localhost:3001
- **Username**: admin
- **Password**: admin
- **Dashboards**: 시스템 메트릭, API 성능, 서비스 상태

## 🔧 환경 변수

### Frontend
```bash
NODE_ENV=development
NEXT_PUBLIC_API_URL=http://gateway:8000
```

### Backend
```bash
ENV=development
DATABASE_URL=postgresql://user:password@db:5432/mrmark
REDIS_URL=redis://redis:6379
```

### AI Engine
```bash
ENV=development
REDIS_URL=redis://redis:6379
```

## 🚀 배포 상태

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

## 📝 문제 해결 이력

### 해결된 문제들
1. **Kong API Gateway 라우팅 문제** → Nginx Gateway로 전환
2. **Docker Compose 의존성 순환** → depends_on 단방향 구조로 변경
3. **Nginx 설정 오류** → add_header 위치 수정, 특별 라우팅 추가
4. **API 엔드포인트 누락** → /health, /metrics 엔드포인트 추가

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 연락처

프로젝트 링크: [https://github.com/tjc7703/Mr.-Mark](https://github.com/tjc7703/Mr.-Mark)

---

**최종 업데이트**: 2025-07-14 09:13:17  
**상태**: 모든 서비스 정상 동작 ✅ 