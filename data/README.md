# 데이터/모델 거버넌스 & 품질 자동화

## 데이터/모델 버전 관리
- 데이터: lake/warehouse/marts 폴더별 버전 관리, 변경 이력 기록
- 모델: ai-engine/models/에 버전별 저장, MLflow 등 활용

## 데이터 라인리지(lineage)
- 데이터 흐름/변환/사용 이력 추적 (예: pipeline 로그, audit log)

## Audit Log 예시
- 수집/변환/분석/예측 등 주요 단계별 로그 자동 기록

## 품질 자동화
- data/pipelines/quality_checks.py: 품질 검증, 리포트 자동화
- 품질 기준(정합성, 완전성, 최신성 등) 자동 체크 