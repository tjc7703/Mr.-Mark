# secrets 관리 & 환경별 config 분리

## secrets 예시
- .env, .env.dev, .env.prod 등 환경별 분리
- k8s secrets, HashiCorp Vault, AWS Secrets Manager 등 활용

## 민감정보 암호화
- 환경변수, secrets manager, configmap 등으로 코드에 직접 노출 금지

## 예시
```
DB_PASSWORD=xxxxxxx
API_KEY=yyyyyyy
```

## 참고
- secrets 템플릿은 git에 커밋하지 않고, README에 예시만 제공 