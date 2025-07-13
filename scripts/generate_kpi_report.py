import json
from datetime import datetime

# 예시 KPI 데이터 (실제 운영 데이터 연동 가능)
kpi = {
    "date": datetime.now().isoformat(),
    "user_count": 1234,
    "active_users": 876,
    "api_error_rate": 0.002,
    "avg_response_time": 0.21,
    "cost_usd": 42.5,
    "feedback_score": 4.7
}

print(json.dumps(kpi, ensure_ascii=False, indent=2)) 