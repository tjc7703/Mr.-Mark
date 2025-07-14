# Mr. Mark - AI 기반 마케팅 마스터리 플랫폼

[![Mr. Mark](https://img.shields.io/badge/Mr.%20Mark-AI%20Marketing%20Platform-blue?style=for-the-badge&logo=robot)](https://github.com/tjc7703/Mr.-Mark)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=flat-square&logo=docker)](https://docker.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-14.0.0-black?style=flat-square&logo=next.js)](https://nextjs.org)

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

## 🏗️ 아키텍처

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

## 🎯 핵심 기능

### 1. 소셜미디어 자동화 (MultiPost 패턴)
- ✅ 30개 SNS 플랫폼 연동
- ✅ 자동 포스팅 스케줄링
- ✅ 크로스 플랫폼 콘텐츠 최적화
- ✅ 실시간 성과 분석

### 2. 실시간 분석 대시보드 (Grafana 패턴)
- ✅ 실시간 KPI 추적
- ✅ 자동 리포트 생성
- ✅ 성과 측정 및 시각화
- ✅ 예측 분석

### 3. AI 기반 콘텐츠 생성 (Fiction 패턴)
- ✅ 트렌드 기반 콘텐츠 생성
- ✅ 자동 최적화 및 개선
- ✅ 감정 분석 및 참여도 예측
- ✅ 개인화 추천

### 4. 마케팅 자동화 워크플로우 (Mautic 패턴)
- ✅ 이메일 마케팅 자동화
- ✅ A/B 테스트 자동화
- ✅ 고객 생애주기 관리
- ✅ 워크플로우 엔진

## 📊 접속 정보

| 서비스 | URL | 설명 |
|--------|-----|------|
| **Frontend** | http://localhost:3000 | 메인 대시보드 |
| **Backend API** | http://localhost:8000/api/backend | REST API |
| **AI Engine** | http://localhost:8000/api/ai | AI 서비스 |
| **Grafana** | http://localhost:3001 | 모니터링 대시보드 |
| **Prometheus** | http://localhost:9090 | 메트릭 수집 |

## 🛠️ 개발 명령어

### 기본 명령어
```bash
# 도움말
make help

# 서비스 관리
make up          # 서비스 시작
make down        # 서비스 중지
make restart     # 서비스 재시작

# 개발 도구
make build       # 빌드
make test        # 테스트
make lint        # 코드 품질 검사
make format      # 코드 포맷팅

# 모니터링
make monitor     # 모니터링 대시보드
make logs        # 실시간 로그
make health      # 헬스체크
make status      # 서비스 상태

# 데이터베이스
make db-backup   # 백업
make db-restore  # 복구
make db-reset    # 초기화

# 배포
make deploy      # 프로덕션 배포
make deploy-scale # 스케일링 배포

# 정리
make clean       # 전체 정리
make clean-logs  # 로그 정리
```

### 개발 모드
```bash
# 전체 개발 모드
make dev

# 개별 서비스 개발 모드
make dev-frontend  # 프론트엔드
make dev-backend   # 백엔드
make dev-ai        # AI 엔진
```

### 자동화 스크립트
```bash
# 자동 배포 (설정 → 빌드 → 테스트 → 배포)
make auto-deploy

# 자동 테스트 (빌드 → 테스트 → 린트)
make auto-test
```

## 📈 성능 지표

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

## 🔒 보안

- ✅ API Gateway를 통한 중앙화된 인증
- ✅ CORS 설정으로 크로스 오리진 보호
- ✅ 환경 변수를 통한 민감 정보 관리
- ✅ 헬스체크를 통한 서비스 안정성 확보
- ✅ Redis 캐싱으로 응답 시간 단축

## 📚 문서

- [📋 아키텍처 설계](./ARCHITECTURE.md)
- [🚀 배포 가이드](./DEPLOYMENT.md)
- [🔧 개발 과정](./개발과정.md)
- [📖 기능 설계](./FEATURE_DESIGN.md)

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 🙏 감사의 말

- [FastAPI](https://fastapi.tiangolo.com/) - 현대적이고 빠른 웹 프레임워크
- [Next.js](https://nextjs.org/) - React 프레임워크
- [Docker](https://docker.com/) - 컨테이너 플랫폼
- [Kong](https://konghq.com/) - API Gateway
- [Grafana](https://grafana.com/) - 모니터링 및 시각화

---

<div align="center">

**Mr. Mark** - AI 기반 마케팅 마스터리 플랫폼

[![GitHub stars](https://img.shields.io/github/stars/tjc7703/Mr.-Mark?style=social)](https://github.com/tjc7703/Mr.-Mark/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/tjc7703/Mr.-Mark?style=social)](https://github.com/tjc7703/Mr.-Mark/network)
[![GitHub issues](https://img.shields.io/github/issues/tjc7703/Mr.-Mark)](https://github.com/tjc7703/Mr.-Mark/issues)

</div> 