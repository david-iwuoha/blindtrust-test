# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from backend.db.connection import init_db_from_schema
from backend.db.seed import seed_demo
from .ai.pipeline import process_audio
import base64  # needed for encoding audio

# routers
from backend.routes import auth as auth_router
from backend.routes import user as user_router
from backend.routes import accounts as accounts_router
from backend.routes import beneficiaries as beneficiaries_router
from backend.routes import ai as ai_router

app = FastAPI(title="BlindTrust Demo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize db and seed
init_db_from_schema()
seed_demo()

# include routers
app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(accounts_router.router)
app.include_router(beneficiaries_router.router)
app.include_router(ai_router.router)

@app.get("/")
def health():
    return {"status": "ok"}

# --- Temporary test endpoint for AI pipeline ---
@app.post("/test-pipeline")
async def test_pipeline(input_text: str):
    """
    Test the full AI pipeline with text input.
    Returns structured output and a dummy audio file.
    """
    # Await the async pipeline
    result = await process_audio(input_text)

    # convert audio bytes to base64 if file exists
    audio_b64 = ""
    if result.get("audio_file"):
        try:
            with open(result["audio_file"], "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode("utf-8")
        except FileNotFoundError:
            audio_b64 = ""  # fallback for placeholder

    return {
        "input_text": result.get("text"),
        "intent": result.get("intent"),
        "reply_text": result.get("response_text"),
        "audio_base64": audio_b64
    }
