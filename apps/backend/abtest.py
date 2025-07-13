from fastapi import APIRouter, Request
from random import choice
import json
from datetime import datetime

router = APIRouter()


@router.get("/abtest")
async def abtest(user_id: str):
    group = choice(["A", "B"])
    result = {
        "user_id": user_id,
        "group": group,
        "timestamp": datetime.now().isoformat(),
    }
    with open("abtest_results.json", "a") as f:
        f.write(json.dumps(result, ensure_ascii=False) + "\n")
    return result
