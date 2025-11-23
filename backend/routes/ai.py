# backend/routes/ai.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.ai.pipeline import process_audio_sync
import base64

router = APIRouter()

class PipelineRequest(BaseModel):
    input_text: str

@router.post("/test-pipeline")
def test_pipeline(req: PipelineRequest):
    result = process_audio_sync(req.input_text)

    # Handle audio safely
    audio_b64 = ""
    audio_file_path = result.get("audio_file")
    if audio_file_path:
        try:
            with open(audio_file_path, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        except FileNotFoundError:
            audio_b64 = ""  # file doesn't exist, return empty string

    return {
        "input_text": result.get("text"),
        "intent": result.get("intent"),
        "reply_text": result.get("response_text"),
        "audio_base64": audio_b64
    }
