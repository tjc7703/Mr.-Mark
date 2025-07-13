# Mr. Mark 온보딩/실행 가이드

## 1. 개발환경 준비
- Docker, Python 3.11+, Node.js 18+, pyenv, pnpm 권장
- git clone 후 make setup

## 2. 서비스 실행
- 전체 실행: make up && make run_all
- 개별 실행: make backend, make frontend, make ai, make pipeline

## 3. 테스트/품질관리
- make lint, make test

## 4. 환경변수
- .env.example 참고, .env 직접 생성/수정

## 5. 문제해결
- python 명령어 인식 안됨: pyenv, PATH, venv 확인
- 패키지 설치 오류: requirements.txt, package.json 버전 확인
- 컨테이너 실행 오류: docker-compose logs, 포트 충돌 확인

## 6. FAQ
- Q: 신규 개발자 온보딩은?
  A: make setup, make up, make run_all만 실행하면 됨
- Q: 데이터 파이프라인만 실행하려면?
  A: make pipeline 