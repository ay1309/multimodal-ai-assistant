from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, images, audio
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Multimodal AI-Assistant",
    description="This agent is able to analyze text, images, and audio using Anthropic's Claude API. By Ana Fernanda Mompin Beristain.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(images.router)
app.include_router(audio.router)

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}