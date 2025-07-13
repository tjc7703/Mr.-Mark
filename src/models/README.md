# src/models/ AI/ML 모델 템플릿

## 구조
- base_model.py: 공통 베이스 클래스
- classification.py: 분류 모델 예시 (scikit-learn)
- regression.py: 회귀 모델 예시 (scikit-learn)
- timeseries.py: 시계열 예측 예시 (Prophet)
- text_classification.py: 텍스트 분류 예시 (transformers)

## 사용 예시
```python
from src.models.classification import ClassificationModel
model = ClassificationModel()
model.train(X_train, y_train)
preds = model.predict(X_test)
acc = model.evaluate(X_test, y_test)
```

## 확장 방법
- 새로운 모델은 BaseModel을 상속받아 구현
- 학습/추론/평가 메서드 일관성 유지

## 참고
- scikit-learn, prophet, transformers 등 주요 라이브러리 활용
- 실제 데이터/실험 코드는 notebooks/ 또는 scripts/에 작성 권장 