#!/bin/bash
set -e

# 1. 모델 폴더 구조 생성
mkdir -p src/models

# 2. 샘플 모델/학습/추론/평가 스크립트 템플릿 생성
if [ ! -f src/models/sample_model.py ]; then
  cat <<EOF > src/models/sample_model.py
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def main():
    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"샘플 모델 정확도: {acc:.4f}")

if __name__ == "__main__":
    main()
EOF
fi

python src/models/sample_model.py

echo "[setup_ai_ml.sh] AI/ML 모델 템플릿/학습/추론/평가 자동화 완료!" 