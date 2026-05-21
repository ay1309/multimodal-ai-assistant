import base64

SUPPORTED_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}

def encode_image(image_bytes: bytes, media_type: str) -> dict:
    if media_type not in SUPPORTED_TYPES:
        raise ValueError(f"Tipo de imagen no soportado: {media_type}")
    b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": b64,
        }
    }

def build_vision_message(image_bytes: bytes, media_type: str, prompt: str) -> dict:
    return {
        "role": "user",
        "content": [
            encode_image(image_bytes, media_type),
            {"type": "text", "text": prompt}
        ]
    }