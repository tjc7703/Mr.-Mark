#!/bin/bash
# ai-engine 서비스 헬스체크 및 장애 자동 복구
STATUS=$(kubectl get pods -l app=ai-engine -o jsonpath='{.items[*].status.phase}')
if [[ $STATUS != *"Running"* ]]; then
  echo "장애 감지: ai-engine 재시작 시도"
  kubectl rollout restart deployment ai-engine-blue
fi 