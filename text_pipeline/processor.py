import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def build_system_prompt() -> str:
    return """Eres un asistente multimodal inteligente.
Puedes analizar texto, imágenes y audio.
Responde siempre en el mismo idioma que el usuario.
Sé claro, conciso y útil."""

async def stream_response(messages: list, on_chunk, client_id: str):
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=int(os.environ.get("MAX_TOKENS", 2048)),
        system=build_system_prompt(),
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            await on_chunk(client_id, text)