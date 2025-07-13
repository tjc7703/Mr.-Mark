# Mr. Mark 프로젝트

## 의존성/버전 관리 정책
- 모든 패키지의 버전은 package.json에 명확히 고정합니다. (^, ~ 등 범위 지정자 사용 금지)
- pnpm-lock.yaml(lock 파일)은 반드시 커밋합니다.
- 의존성 추가/업데이트 시 반드시 버전을 명시하고, lock 파일을 갱신 후 커밋하세요.
- 여러 워크스페이스(예: frontend, apps/frontend 등) 모두 동일하게 적용합니다.
- CI/CD에서 install/build 자동 테스트를 통해 버전 충돌을 사전에 방지합니다.

## 프로젝트 목표
- AI 기반 마케팅 마스터리 플랫폼
- 실무 중심, 실시간 트렌드, 30개 SNS 연동, 게임화 UX, 개인화 로드맵 등 세계 최고 수준의 기능 구현

## 주요 기술 스택
- **프론트엔드**: Next.js(React), TypeScript, Tailwind CSS
- **백엔드**: FastAPI(Python), Node.js(Express), GraphQL, WebSocket
- **AI/ML**: OpenAI API, HuggingFace, Google Trends API, BeautifulSoup, Prophet, Scikit-learn
- **DB/캐시**: PostgreSQL, Redis, MongoDB
- **인프라**: Docker, Kubernetes, AWS/GCP, GitHub Actions

## 폴더 구조
```
Mr. Mark/
├── frontend/        # 프론트엔드(Next.js)
├── backend/         # 백엔드(FastAPI, Node.js)
├── ai-engine/       # AI/ML, 크롤러, 트렌드 분석
├── data/            # 데이터, DB, 마이그레이션
├── infra/           # 인프라, 배포, Docker, CI/CD
├── docs/            # 문서, 설계, 회의록
└── 개발과정.md      # 전체 개발 과정 문서
```

## 시작 방법
1. 각 폴더별 README 및 예시 코드 참고
2. `frontend/`에서 Next.js 개발 서버 실행
3. `backend/`에서 FastAPI/Node.js 서버 실행

---

> 본 프로젝트는 AI, 자동화, 실시간성, 확장성, 게임화 UX를 모두 결합한 차세대 마케팅 교육 플랫폼입니다. 