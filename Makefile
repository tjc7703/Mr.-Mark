# Mr. Mark 프로젝트 통합 Makefile

.PHONY: setup up down backend frontend ai pipeline lint test clean

setup:
	bash scripts/setup.sh

up:
	docker-compose up -d --build

down:
	docker-compose down

backend:
	cd apps/backend && bash ../../scripts/start_backend.sh

frontend:
	cd apps/frontend && bash ../../scripts/start_frontend.sh

ai:
	cd apps/ai-engine && bash ../../scripts/start_ai.sh

pipeline:
	bash scripts/run_pipeline.sh

lint:
	bash scripts/lint.sh

test:
	bash scripts/test.sh

clean:
	docker system prune -af
	rm -rf **/__pycache__ **/.pytest_cache **/.mypy_cache **/.next **/node_modules 