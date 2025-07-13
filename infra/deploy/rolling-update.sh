#!/bin/bash
# 롤링/무중단 배포 자동화
kubectl rollout restart deployment ai-engine-blue
kubectl rollout status deployment ai-engine-blue 