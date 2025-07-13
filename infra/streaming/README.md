# 실시간/배치 데이터 파이프라인

## Kafka + Spark Streaming
- kafka-docker-compose.yml: Kafka/ZooKeeper 실시간 메시지 브로커
- Spark, Airflow 등과 연동하여 실시간/배치 파이프라인 구축 가능

## 실행 예시
```bash
docker-compose -f kafka-docker-compose.yml up -d
```

## 확장
- Spark Streaming, Airflow DAG, 데이터 파이프라인 스크립트 추가 가능 