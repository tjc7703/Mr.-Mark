# Airflow 데이터/AI 파이프라인

## 개요
- 데이터 수집, ETL, 품질, AI 학습/예측, 리포트 등 전체 워크플로우를 Airflow로 스케줄링/모니터링/자동화

## 주요 DAG 예시
- collect_sns_data_dag
- etl_dag
- quality_check_dag
- train_ai_dag
- report_dag

## 실행 방법
```bash
docker-compose -f docker-compose.airflow.yml up -d
```
- Airflow UI: http://localhost:8080

## 커스텀 DAG 작성법
- airflow/dags/ 폴더에 Python 파일로 DAG 추가

## 참고
- https://airflow.apache.org/ 