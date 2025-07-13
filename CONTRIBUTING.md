# Mr. Mark 프로젝트 기여 가이드

## 1. 브랜치 전략
- main: 배포/운영용, 항상 안정 상태 유지
- dev: 개발 통합, 기능/버그 브랜치 병합 전용
- feature/xxx, bugfix/xxx: 기능 개발/버그 수정용 개별 브랜치

## 2. 커밋 메시지 규칙
- [타입] 요약 (예: [feat] 사용자 로그인 기능 추가)
- 타입: feat, fix, docs, style, refactor, test, chore 등
- 본문/이슈번호는 선택

## 3. PR(Pull Request) 규칙
- dev 브랜치로 PR 생성, 리뷰어 지정
- 주요 변경점/테스트 방법/이슈번호 명시
- CI 통과, 코드리뷰 승인 후 병합

## 4. 코드 스타일
- Python: black, flake8, mypy, isort 적용
- JS/TS: prettier, eslint 적용
- pre-commit hook 필수 적용

## 5. 테스트
- pytest 등 자동화 테스트 필수
- 주요 기능/버그는 테스트 코드 동반

## 6. 문서화
- docs/README.md, 코드 내 docstring, 주석 적극 활용
- 신규 기능/구조 변경 시 문서 갱신

## 7. 이슈/토론
- 깃허브 이슈/PR, Discussions, Notion/Wiki 적극 활용
- 질문/제안/버그는 이슈 등록

---

> 글로벌 오픈소스 협업 문화를 지향합니다. 모든 기여는 환영합니다! 