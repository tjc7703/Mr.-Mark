# Mr. Mark 프로젝트

## 개요
마케팅/AI 대시보드 통합 플랫폼. 프론트엔드(Next.js), 백엔드(FastAPI), 데이터 파이프라인, AI, 품질관리 등 멀티서비스 구조.

## 폴더 구조
- apps/: 멀티서비스(Docker 지원)
- scripts/: 자동화 스크립트
- data/: 데이터 파이프라인/레이크/마트/웨어하우스
- ai-engine/: AI 파이프라인
- frontend/: 프론트엔드(Next.js)
- backend/: 백엔드(FastAPI)
- infra/: 인프라/IaC
- docs/: 문서화

## 빠른 시작
```bash
make setup
make up
make run_all
```

## 주요 명령어
- make setup: 환경 세팅
- make up/down: 전체 서비스 실행/중지
- make backend/frontend/ai: 개별 서비스 실행
- make pipeline: 데이터/AI 파이프라인 실행
- make lint/test: 품질관리

## 자동화/운영
- Docker, Makefile, scripts, .env, CI/CD, devcontainer, pre-commit 등 완비

## 문서
- docs/architecture.md: 아키텍처/구조
- docs/onboarding.md: 온보딩/실행가이드
- docs/pipeline.md: 데이터/AI 파이프라인

## 문의/기여
- 깃허브 이슈/PR 또는 Notion/Wiki 참고 