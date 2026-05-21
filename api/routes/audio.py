import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from audio_pipeline.processor import build_audio_message
from text_pipeline.processor import client, build_system_prompt

router = APIRouter()

@router.post("/api/transcribe")
async def transcribe_and_respond(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    message = build_audio_message(audio_bytes, file.content_type)

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=int(os.environ.get("MAX_TOKENS", 2048)),
        system=build_system_prompt(),
        messages=[message],
    )

    return JSONResponse({
        "response": response.content[0].text
    })