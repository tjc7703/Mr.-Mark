#!/bin/bash
# Blue/Green 롤백: 서비스 selector를 이전 버전으로 전환
kubectl patch service ai-engine-service -p '{"spec":{"selector":{"app":"ai-engine","version":"blue"}}}'
echo "롤백 완료: 트래픽이 blue로 전환되었습니다." 