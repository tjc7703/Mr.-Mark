# 🚀 Mr. Mark - AI 기반 실용 마케팅 교육 플랫폼

> **최신 기술 스택으로 구축된 완전한 AI 기반 마케팅 교육 플랫폼**

## 📊 현재 상태

### ✅ 모든 서비스 정상 동작 중 (2025-07-14)

| 서비스 | 상태 | 포트 | 설명 |
|--------|------|------|------|
| **프론트엔드** | ✅ 정상 | 3000 | Next.js 14 + TypeScript |
| **백엔드 API** | ✅ 정상 | 8001 | FastAPI + Python 3.11 |
| **AI 엔진** | ✅ 정상 | 9000 | AI 마케팅 분석 엔진 |
| **API Gateway** | ✅ 정상 | 8000 | Nginx 프록시 |
| **데이터베이스** | ✅ 정상 | 5432 | PostgreSQL 15 |
| **캐시** | ✅ 정상 | 6379 | Redis 7 |
| **모니터링** | ✅ 정상 | 9090/3001 | Prometheus + Grafana |

## 🌐 접속 정보

### 웹 서비스
- **메인 홈페이지**: http://localhost:3000
- **API Gateway**: http://localhost:8000
- **Grafana 대시보드**: http://localhost:3001
- **Prometheus 메트릭**: http://localhost:9090

### API 엔드포인트
- **백엔드 API**: http://localhost:8001
- **AI 엔진**: http://localhost:9000
- **피드 API**: http://localhost:8000/feed/today
- **트렌드 API**: http://localhost:8000/trend
- **AI 피드백**: http://localhost:8000/ai/feedback

## 🎯 주요 기능

### ✅ 정상 동작 중인 기능들
1. **실시간 마케팅 트렌드 차트**
   - AI 마케팅 자동화, 틱톡 마케팅 등 실시간 트렌드
   - Recharts를 활용한 인터랙티브 차트

2. **오늘의 마케팅 소식 피드**
   - 최신 마케팅 뉴스 5개
   - 카테고리별 분류 (트렌드, 소셜미디어, 바이럴마케팅 등)

3. **AI 마케팅 코치 피드백**
   - 개인화된 마케팅 조언
   - 콘텐츠 최적화, 포스팅 시간, 콘텐츠 유형 제안

4. **플랫폼별 성과 파이 차트**
   - 인스타그램, 틱톡, 유튜브, 링크드인 성과 분석
   - 시각적 데이터 표현

5. **오늘의 미션 체크리스트**
   - 실용적인 마케팅 미션
   - 인스타그램 릴스 업로드, 해시태그 추가 등

6. **실시간 통계 카드**
   - 조회수, 팔로워, 좋아요, 댓글 실시간 통계

## 🛠️ 기술 스택

### Frontend
- **Next.js 14** - React 기반 풀스택 프레임워크
- **TypeScript** - 타입 안전성
- **Tailwind CSS** - 유틸리티 퍼스트 CSS 프레임워크
- **Recharts** - React 차트 라이브러리
- **SWR** - 데이터 페칭 라이브러리

### Backend
- **FastAPI** - 현대적 Python 웹 프레임워크
- **Python 3.11** - 최신 Python 버전
- **Uvicorn** - ASGI 서버
- **PostgreSQL 15** - 관계형 데이터베이스
- **Redis 7** - 인메모리 캐시

### Infrastructure
- **Docker** - 컨테이너화
- **Docker Compose** - 멀티 컨테이너 오케스트레이션
- **Nginx** - API Gateway 및 리버스 프록시
- **Prometheus** - 메트릭 수집
- **Grafana** - 모니터링 대시보드

## 🚀 빠른 시작

### 1. 저장소 클론
```bash
git clone https://github.com/tjc7703/Mr.-Mark.git
cd Mr.-Mark
```

### 2. 환경 설정
```bash
# Python 가상환경 설정
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 3. 서비스 실행
```bash
# 모든 서비스 시작
docker-compose up -d

# 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f
```

### 4. 접속 확인
- 홈페이지: http://localhost:3000
- API Gateway: http://localhost:8000
- Grafana: http://localhost:3001 (admin/admin)

## 📁 프로젝트 구조

```
Mr. Mark/
├── apps/
│   ├── frontend/          # Next.js 프론트엔드
│   ├── backend/           # FastAPI 백엔드
│   └── ai-engine/         # AI 분석 엔진
├── docker-compose.yml     # 서비스 오케스트레이션
├── nginx.conf            # API Gateway 설정
├── prometheus.yml        # 모니터링 설정
├── requirements.txt      # Python 의존성
├── Makefile             # 자동화 스크립트
└── docs/                # 문서
```

## 🔧 개발 명령어

### Docker Compose
```bash
# 서비스 시작
docker-compose up -d

# 서비스 중지
docker-compose down

# 서비스 재시작
docker-compose restart

# 로그 확인
docker-compose logs -f [service-name]

# 상태 확인
docker-compose ps
```

### Makefile
```bash
# 전체 설정
make setup

# 서비스 시작
make up

# 서비스 중지
make down

# 재시작
make restart

# 로그 확인
make logs

# 상태 확인
make status

# 정리
make clean
```

## 📈 성능 지표

### API 성능
- **피드 API**: ~50ms 응답 시간
- **트렌드 API**: ~45ms 응답 시간
- **AI 피드백**: ~60ms 응답 시간

### 서비스 가동률
- **전체 서비스**: 100% 정상 동작
- **헬스체크**: 모든 서비스 healthy 상태

## 🛠️ 문제 해결

### 일반적인 문제들

1. **포트 충돌**
   ```bash
   # 사용 중인 포트 확인
   lsof -i :3000
   
   # Docker 컨테이너 재시작
   docker-compose restart
   ```

2. **API 연결 문제**
   ```bash
   # API 헬스체크
   curl http://localhost:8001/health
   curl http://localhost:9000/health
   ```

3. **빌드 오류**
   ```bash
   # 캐시 삭제 후 재빌드
   docker-compose build --no-cache
   docker-compose up -d
   ```

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

**마지막 업데이트**: 2025-07-14  
**상태**: 🟢 모든 시스템 정상 동작 