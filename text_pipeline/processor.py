import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def build_system_prompt() -> str:           # here is whre the system promt is defined. General but in my proyect works as an example
    return """You are a smart multimodal assistant.
You can analyze text, images, and audio.
Always respond in the same language as the user.
Be clear, concise, and helpful."""

async def stream_response(messages: list, on_chunk, client_id: str):
    with client.messages.stream(
        model="claude-3-5-sonnet-20241022",
        max_tokens=int(os.environ.get("MAX_TOKENS", 2048)),
        system=build_system_prompt(),
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            await on_chunk(client_id, text)