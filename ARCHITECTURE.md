# Mr. Mark 프로젝트 아키텍처 설계

## 🏗️ 전체 아키텍처 개요

```
Mr. Mark Platform Architecture
├── API Gateway (Kong)
│   ├── Frontend Service (Next.js 14)
│   ├── Backend Service (FastAPI)
│   └── AI Engine Service (Python)
├── Database Layer
│   ├── PostgreSQL (Primary DB)
│   └── Redis (Cache)
└── Monitoring Layer
    ├── Prometheus (Metrics)
    └── Grafana (Visualization)
```

## 🔧 기술 스택

### Frontend
- **Framework**: Next.js 14.0.0
- **Language**: TypeScript 5.8.3
- **Styling**: Tailwind CSS 4.1.11
- **State Management**: SWR 2.2.0
- **Charts**: Recharts 2.8.0

### Backend
- **Framework**: FastAPI 0.115.6
- **Language**: Python 3.11
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **ORM**: SQLAlchemy 2.0.30

### AI Engine
- **Framework**: FastAPI 0.115.6
- **ML Libraries**: 
  - Transformers 4.40.0
  - Scikit-learn 1.4.0
  - PyTorch 2.1.0+cpu
- **NLP**: NLTK 3.8.1, TextBlob 0.18.0

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **API Gateway**: Kong 3.4
- **Monitoring**: Prometheus + Grafana
- **CI/CD**: GitHub Actions

## 🚀 핵심 기능

### 1. 소셜미디어 자동화 (MultiPost 패턴)
- 30개 SNS 플랫폼 연동
- 자동 포스팅 스케줄링
- 크로스 플랫폼 콘텐츠 최적화

### 2. 실시간 분석 대시보드 (Grafana 패턴)
- 실시간 KPI 추적
- 자동 리포트 생성
- 성과 측정 및 시각화

### 3. AI 기반 콘텐츠 생성 (Fiction 패턴)
- 트렌드 기반 콘텐츠 생성
- 자동 최적화 및 개선
- 감정 분석 및 참여도 예측

### 4. 마케팅 자동화 워크플로우 (Mautic 패턴)
- 이메일 마케팅 자동화
- A/B 테스트 자동화
- 고객 생애주기 관리

## 📊 데이터 흐름

```
1. 데이터 수집
   SNS APIs → Data Collection Service → PostgreSQL

2. AI 분석
   Raw Data → AI Engine → Analysis Results → PostgreSQL

3. 실시간 처리
   Events → Redis → Real-time Processing → Frontend

4. 모니터링
   All Services → Prometheus → Grafana Dashboard
```

## 🔒 보안 및 성능

### 보안
- API Gateway를 통한 중앙화된 인증
- CORS 설정으로 크로스 오리진 보호
- 환경 변수를 통한 민감 정보 관리

### 성능
- Redis 캐싱으로 응답 시간 단축
- 멀티스테이지 Docker 빌드로 이미지 크기 최적화
- 헬스체크를 통한 서비스 안정성 확보

## 🛠️ 개발 환경

### 로컬 개발
```bash
# 전체 서비스 시작
docker-compose up -d

# 특정 서비스만 시작
docker-compose up frontend backend ai-engine

# 로그 확인
docker-compose logs -f [service-name]
```

### 프로덕션 배포
```bash
# 프로덕션 빌드
docker-compose -f docker-compose.prod.yml up -d

# 스케일링
docker-compose up -d --scale backend=3
```

## 📈 모니터링 및 로깅

### 메트릭 수집
- Prometheus: 시스템 메트릭, 애플리케이션 메트릭
- Grafana: 대시보드 시각화
- 커스텀 메트릭: 비즈니스 KPI

### 로깅
- 구조화된 로깅 (JSON 형식)
- 로그 레벨: DEBUG, INFO, WARNING, ERROR
- 중앙화된 로그 수집

## 🔄 CI/CD 파이프라인

### GitHub Actions 워크플로우
1. **코드 품질 검사**
   - Linting (ESLint, Flake8)
   - Type checking (TypeScript, MyPy)
   - Security scanning

2. **테스트 실행**
   - Unit tests
   - Integration tests
   - E2E tests

3. **빌드 및 배포**
   - Docker 이미지 빌드
   - 컨테이너 레지스트리 푸시
   - 자동 배포

## 🎯 성능 목표

### 응답 시간
- API 응답: < 200ms
- 페이지 로드: < 2초
- 실시간 업데이트: < 1초

### 가용성
- 시스템 업타임: 99.9%
- 데이터 백업: 매일 자동
- 장애 복구: < 5분

### 확장성
- 동시 사용자: 10,000+
- 데이터 처리량: 1M+ records/day
- AI 모델 추론: 100+ requests/second

## 🔮 향후 계획

### Phase 1 (현재)
- 기본 아키텍처 구축
- 핵심 기능 구현
- 모니터링 시스템 구축

### Phase 2 (다음 3개월)
- 마이크로서비스 분리
- Kubernetes 마이그레이션
- 고급 AI 기능 추가

### Phase 3 (6개월 후)
- 클라우드 네이티브 아키텍처
- 서버리스 함수 도입
- 글로벌 확장 준비 