# Mr. Mark 시스템 아키텍처

## 전체 구조
- 프론트엔드(Next.js)
- 백엔드(FastAPI)
- 데이터 파이프라인(ETL, 품질, AI)
- AI 엔진
- 데이터 레이크/마트/웨어하우스
- 공통 패키지
- 멀티서비스(Docker, Makefile, scripts)
- CI/CD, devcontainer, pre-commit

## 서비스 연동
- docker-compose로 모든 서비스 컨테이너화
- Makefile/scripts로 일괄 실행/테스트/품질관리
- .env로 환경변수 일원화

## 데이터 흐름
1. 데이터 수집(collect_sns_data.py 등)
2. 데이터 정제/적재(ETL)
3. 품질 체크(quality_checks.py)
4. AI 학습/예측(train_ai.py)
5. 리포트 생성(report.py)

## 자동화 구조
- scripts/: setup, run_all, lint, test 등
- Makefile: 전체 명령어 통합
- CI/CD: .github/workflows/ci.yml
- devcontainer: 개발환경 자동화
- pre-commit: 커밋 전 린트/테스트

## 아키텍처 다이어그램
(mermaid 등으로 시각화 가능) 