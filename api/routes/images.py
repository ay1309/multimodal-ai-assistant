import os
from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from image_pipeline.processor import build_vision_message
from text_pipeline.processor import client, build_system_prompt

router = APIRouter()

@router.post("/api/analyze-image")
async def analyze_image(
    file: UploadFile = File(...),
    prompt: str = Form(default="Describe esta imagen detalladamente.")
):
    image_bytes = await file.read()
    message = build_vision_message(image_bytes, file.content_type, prompt)

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=int(os.environ.get("MAX_TOKENS", 2048)),
        system=build_system_prompt(),
        messages=[message],
    )
    return JSONResponse({"result": response.content[0].text})