import base64

SUPPORTED_AUDIO_TYPES = {
    "audio/mpeg", "audio/mp4", "audio/wav",
    "audio/webm", "audio/ogg", "audio/flac"
}

def encode_audio(audio_bytes: bytes, media_type: str) -> dict:
    if media_type not in SUPPORTED_AUDIO_TYPES:
        raise ValueError(f"Tipo de audio no soportado: {media_type}")
    b64 = base64.standard_b64encode(audio_bytes).decode("utf-8")
    return {
        "type": "document",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": b64,
        }
    }

def build_audio_message(audio_bytes: bytes, media_type: str, prompt: str = "Transcribe este audio y responde al contenido.") -> dict:
    return {
        "role": "user",
        "content": [
            encode_audio(audio_bytes, media_type),
            {"type": "text", "text": prompt}
        ]
    }