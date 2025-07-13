# Kubernetes 템플릿 & 인프라 확장

## 구성 예시
- ai-engine, backend, frontend, db, redis 등 서비스별 배포 yaml
- secrets/configmap, ingress, service, deployment, hpa 등 포함

## 배포 예시
```bash
kubectl apply -f ai-engine-deployment.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
```

## 운영 자동화
- prometheus, grafana, alertmanager, slack/webhook 연동
- rolling update, autoscaling, zero-downtime 배포 