# Mr. Mark 프로젝트 최고 효율 Makefile

.PHONY: help setup up down build test lint clean deploy monitor logs backup restore

# 기본 명령어
help: ## 도움말 표시
	@echo "Mr. Mark 프로젝트 명령어:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# 개발 환경 설정
setup: ## 개발 환경 초기 설정
	@echo "🔧 개발 환경 설정 중..."
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up -d
	@echo "✅ 개발 환경 설정 완료!"

# 서비스 관리
up: ## 모든 서비스 시작
	@echo "🚀 서비스 시작 중..."
	docker-compose up -d
	@echo "✅ 서비스 시작 완료!"

down: ## 모든 서비스 중지
	@echo "🛑 서비스 중지 중..."
	docker-compose down
	@echo "✅ 서비스 중지 완료!"

restart: ## 모든 서비스 재시작
	@echo "🔄 서비스 재시작 중..."
	docker-compose restart
	@echo "✅ 서비스 재시작 완료!"

# 빌드 및 테스트
build: ## 모든 서비스 빌드
	@echo "🔨 서비스 빌드 중..."
	docker-compose build --no-cache
	@echo "✅ 빌드 완료!"

test: ## 테스트 실행
	@echo "🧪 테스트 실행 중..."
	docker-compose exec backend pytest
	docker-compose exec frontend npm test
	@echo "✅ 테스트 완료!"

lint: ## 코드 품질 검사
	@echo "🔍 코드 품질 검사 중..."
	docker-compose exec backend flake8 .
	docker-compose exec backend black --check .
	docker-compose exec frontend npm run lint
	@echo "✅ 코드 품질 검사 완료!"

format: ## 코드 포맷팅
	@echo "🎨 코드 포맷팅 중..."
	docker-compose exec backend black .
	docker-compose exec frontend npm run format
	@echo "✅ 코드 포맷팅 완료!"

# 모니터링 및 로그
monitor: ## 모니터링 대시보드 열기
	@echo "📊 모니터링 대시보드:"
	@echo "  - Grafana: http://localhost:3001 (admin/admin)"
	@echo "  - Prometheus: http://localhost:9090"
	@echo "  - Frontend: http://localhost:3000"
	@echo "  - Backend API: http://localhost:8000/api/backend"
	@echo "  - AI Engine: http://localhost:8000/api/ai"

logs: ## 실시간 로그 확인
	@echo "📋 실시간 로그 확인 중..."
	docker-compose logs -f

logs-backend: ## 백엔드 로그 확인
	docker-compose logs -f backend

logs-frontend: ## 프론트엔드 로그 확인
	docker-compose logs -f frontend

logs-ai: ## AI 엔진 로그 확인
	docker-compose logs -f ai-engine

# 데이터베이스 관리
db-backup: ## 데이터베이스 백업
	@echo "💾 데이터베이스 백업 중..."
	docker-compose exec db pg_dump -U user mrmark > backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ 백업 완료!"

db-restore: ## 데이터베이스 복구
	@echo "🔄 데이터베이스 복구 중..."
	docker-compose exec -T db psql -U user mrmark < backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "✅ 복구 완료!"

db-reset: ## 데이터베이스 초기화
	@echo "🔄 데이터베이스 초기화 중..."
	docker-compose exec db psql -U user -d mrmark -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
	docker-compose exec db psql -U user -d mrmark -f /docker-entrypoint-initdb.d/init.sql
	@echo "✅ 초기화 완료!"

# 배포
deploy: ## 프로덕션 배포
	@echo "🚀 프로덕션 배포 중..."
	docker-compose -f docker-compose.prod.yml up -d
	@echo "✅ 배포 완료!"

deploy-scale: ## 스케일링 배포
	@echo "📈 스케일링 배포 중..."
	docker-compose up -d --scale backend=3 --scale ai-engine=2
	@echo "✅ 스케일링 배포 완료!"

# 정리
clean: ## 모든 컨테이너 및 이미지 정리
	@echo "🧹 정리 중..."
	docker-compose down -v --remove-orphans
	docker system prune -af
	@echo "✅ 정리 완료!"

clean-logs: ## 로그 파일 정리
	@echo "🗑️ 로그 파일 정리 중..."
	rm -f *.log nohup.out
	@echo "✅ 로그 파일 정리 완료!"

# 개발 도구
dev: ## 개발 모드 시작
	@echo "👨‍💻 개발 모드 시작..."
	docker-compose up -d
	@echo "✅ 개발 모드 시작 완료!"

dev-frontend: ## 프론트엔드 개발 모드
	@echo "🎨 프론트엔드 개발 모드..."
	cd apps/frontend && npm run dev

dev-backend: ## 백엔드 개발 모드
	@echo "🔧 백엔드 개발 모드..."
	cd apps/backend && uvicorn main:app --reload --host 0.0.0.0 --port 8001

dev-ai: ## AI 엔진 개발 모드
	@echo "🤖 AI 엔진 개발 모드..."
	cd apps/ai-engine && uvicorn app:app --reload --host 0.0.0.0 --port 9000

# 상태 확인
status: ## 서비스 상태 확인
	@echo "📊 서비스 상태:"
	docker-compose ps
	@echo ""
	@echo "🔗 접속 정보:"
	@echo "  - Frontend: http://localhost:3000"
	@echo "  - Backend: http://localhost:8000/api/backend"
	@echo "  - AI Engine: http://localhost:8000/api/ai"
	@echo "  - Grafana: http://localhost:3001"
	@echo "  - Prometheus: http://localhost:9090"

health: ## 헬스체크
	@echo "🏥 헬스체크 중..."
	@curl -f http://localhost:8000/api/backend/health || echo "❌ Backend 서비스 오류"
	@curl -f http://localhost:8000/api/ai/health || echo "❌ AI Engine 서비스 오류"
	@curl -f http://localhost:3000 || echo "❌ Frontend 서비스 오류"
	@echo "✅ 헬스체크 완료!"

# 자동화 스크립트
auto-deploy: setup build test deploy ## 자동 배포 (설정 → 빌드 → 테스트 → 배포)
	@echo "🤖 자동 배포 완료!"

auto-test: build test lint ## 자동 테스트 (빌드 → 테스트 → 린트)
	@echo "🤖 자동 테스트 완료!"

# 도움말
.DEFAULT_GOAL := help 