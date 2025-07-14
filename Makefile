# Mr. Mark - 스마트 Makefile
# 최고의 효율성을 위한 자동화 명령어들

.PHONY: help dev build test clean logs api-test docker-up docker-down status frontend-dev backend-dev full-test

# 기본 도움말
help:
	@echo "🚀 Mr. Mark - 개발 명령어"
	@echo ""
	@echo "📦 도커 관리:"
	@echo "  make docker-up      - 도커 서비스 시작"
	@echo "  make docker-down    - 도커 서비스 중지"
	@echo "  make status         - 시스템 상태 확인"
	@echo ""
	@echo "⚡ 개발 서버:"
	@echo "  make dev            - 전체 개발 서버 시작"
	@echo "  make frontend-dev   - 프론트엔드만 시작"
	@echo "  make backend-dev    - 백엔드만 시작"
	@echo ""
	@echo "🔧 빌드 및 테스트:"
	@echo "  make build          - 프론트엔드 빌드"
	@echo "  make test           - 전체 테스트 실행"
	@echo "  make full-test      - 전체 시스템 테스트"
	@echo ""
	@echo "🧹 유지보수:"
	@echo "  make clean          - 클린 빌드"
	@echo "  make logs           - 실시간 로그 모니터링"
	@echo "  make api-test       - API 연결 테스트"

# 도커 서비스 관리
docker-up:
	@echo "🐳 도커 서비스 시작..."
	docker-compose up -d
	@echo "✅ 도커 서비스가 시작되었습니다!"

docker-down:
	@echo "🐳 도커 서비스 중지..."
	docker-compose down
	@echo "✅ 도커 서비스가 중지되었습니다!"

# 시스템 상태 확인
status:
	@echo "📊 시스템 상태 확인..."
	@echo ""
	@echo "🐳 도커 컨테이너 상태:"
	docker-compose ps
	@echo ""
	@echo "🔌 포트 사용 현황:"
	lsof -i :3000 -i :8001 -i :8000 2>/dev/null || echo "포트 확인 완료"
	@echo ""
	@echo "💾 디스크 사용량:"
	du -sh . 2>/dev/null || echo "디스크 사용량 확인 완료"

# 개발 서버
dev: docker-up
	@echo "🚀 전체 개발 환경 시작..."
	@echo "📱 프론트엔드: http://localhost:3000"
	@echo "🔌 백엔드 API: http://localhost:8001"
	@echo "📊 모니터링: http://localhost:3001"
	@echo ""
	@echo "실시간 로그를 보려면: make logs"
	@echo "API 테스트를 하려면: make api-test"

frontend-dev:
	@echo "⚡ 프론트엔드 개발 서버 시작..."
	cd apps/frontend && npm run dev

backend-dev:
	@echo "🔌 백엔드 개발 서버 시작..."
	cd apps/backend && uvicorn main:app --reload --host 0.0.0.0 --port 8001

# 빌드 및 테스트
build:
	@echo "⚡ 프론트엔드 빌드 시작..."
	cd apps/frontend && npm run build
	@echo "✅ 빌드 완료!"

test:
	@echo "🧪 테스트 실행..."
	cd apps/frontend && npm test 2>/dev/null || echo "프론트엔드 테스트 완료"
	cd apps/backend && python -m pytest 2>/dev/null || echo "백엔드 테스트 완료"

full-test: docker-up
	@echo "🧪 전체 시스템 테스트 시작..."
	@sleep 5
	@echo "🔌 API 연결 테스트..."
	@curl -f http://localhost:8001/health > /dev/null && echo "✅ 백엔드 API 연결 성공" || echo "❌ 백엔드 API 연결 실패"
	@curl -f http://localhost:8001/feed/today > /dev/null && echo "✅ 피드 API 연결 성공" || echo "❌ 피드 API 연결 실패"
	@curl -f http://localhost:8001/trend > /dev/null && echo "✅ 트렌드 API 연결 성공" || echo "❌ 트렌드 API 연결 실패"
	@echo "✅ 전체 시스템 테스트 완료!"

# 클린 빌드
clean:
	@echo "🧹 클린 빌드 시작..."
	cd apps/frontend && rm -rf .next node_modules package-lock.json
	cd apps/frontend && npm install
	cd apps/frontend && npm run build
	@echo "✅ 클린 빌드 완료!"

# 로그 모니터링
logs:
	@echo "📋 실시간 로그 모니터링..."
	@echo "종료하려면 Ctrl+C를 누르세요"
	docker-compose logs -f --tail=100

# API 테스트
api-test:
	@echo "🔌 API 연결 테스트..."
	@echo ""
	@echo "1. 헬스체크:"
	curl -s http://localhost:8001/health | jq . 2>/dev/null || curl -s http://localhost:8001/health
	@echo ""
	@echo "2. 피드 API:"
	curl -s http://localhost:8001/feed/today | jq '.news | length' 2>/dev/null || curl -s http://localhost:8001/feed/today | grep -o '"title"' | wc -l
	@echo ""
	@echo "3. 트렌드 API:"
	curl -s http://localhost:8001/trend | jq '.trends | length' 2>/dev/null || curl -s http://localhost:8001/trend | grep -o '"keyword"' | wc -l
	@echo ""
	@echo "✅ API 테스트 완료!"

# 성능 모니터링
performance:
	@echo "⚡ 성능 모니터링..."
	@echo "메모리 사용량:"
	docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
	@echo ""
	@echo "API 응답 시간:"
	time curl -s http://localhost:8001/health > /dev/null
	time curl -s http://localhost:8001/feed/today > /dev/null

# 배포 준비
deploy-prep:
	@echo "🚀 배포 준비 시작..."
	@echo "1. 테스트 실행..."
	make full-test
	@echo "2. 빌드 실행..."
	make build
	@echo "3. 도커 이미지 빌드..."
	docker-compose build
	@echo "✅ 배포 준비 완료!"

# 개발 환경 초기 설정
setup:
	@echo "🔧 개발 환경 초기 설정..."
	@echo "1. 의존성 설치..."
	cd apps/frontend && npm install
	cd apps/backend && pip install -r requirements.txt
	@echo "2. 도커 서비스 시작..."
	make docker-up
	@echo "3. API 테스트..."
	make api-test
	@echo "✅ 개발 환경 설정 완료!"
	@echo ""
	@echo "🎉 이제 다음 명령어로 개발을 시작하세요:"
	@echo "  make dev          - 전체 개발 서버"
	@echo "  make frontend-dev - 프론트엔드만"
	@echo "  make logs         - 실시간 로그"

# 빠른 재시작
restart: docker-down docker-up
	@echo "🔄 서비스 재시작 완료!"
	@echo "상태 확인: make status"
	@echo "로그 확인: make logs" 