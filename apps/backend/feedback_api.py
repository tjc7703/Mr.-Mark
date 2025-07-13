from fastapi import APIRouter, Request
from pydantic import BaseModel
from datetime import datetime
import json

router = APIRouter()

class Feedback(BaseModel):
    user_id: str
    feedback: str
    rating: int
    timestamp: str = datetime.now().isoformat()

@router.post("/feedback")
async def submit_feedback(feedback: Feedback):
    with open("feedbacks.json", "a") as f:
        f.write(json.dumps(feedback.dict(), ensure_ascii=False) + "\n")
    return {"status": "success", "msg": "피드백이 저장되었습니다."} 