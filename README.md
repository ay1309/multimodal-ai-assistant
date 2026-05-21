# multimodal-ai-assistant

**MULTIMODAL AI-ASSISTANT**

Production-ready conversational AI assistant with real-time streaming, vision analysis, and audio transcription — built with FastAPI and Anthropic's Claude (Claude Haiku).


<img src="sample_images/mainView.jpeg" width="400"/>

This consists of a full-stack AI assistant that goes beyond only basic chat (just text). Users can send text, upload images for visual analysis, and submit audio files for a transcription and analysis of content — all processed by Claude (Haiku) in real time through a persistent WebSocket connection (full-duplex).

*Key technical decisions*:
    - WebSocket over REST for chat: This enables true token-by-token streaming
    - Single model for all modalities (Text, video, audio): Claude (claude-haiku-4-5-20251001) 
    - Stateless backend with in-memory history on the client: Alowys to scale horizontally without session storage 

## Features
    - *Live streaming*: Responses appear token-by-token via WebSocket, not all at once

    - *Vision analysis*: The user can upload any valid image file (JPG, PNG, WebP, GIF) and ask about it

    - *Audio transcription*: Valid audio files can be uploaded for transcription to obtain an intelligent response or analysis of the information contained on the recording

    - *Conversation memory*: Full chat history is sent with every request so Claude remembers context

    - *Auto-documentation*: FastAPI generates interactive API documentation (Can be visualized at \docs)

    - *Cloud deploy ready*: The assisant is ready to be deployed using Docker with the command *docker compose up*

Sample test chat that demonstrate the memory use and contextualized responses (Img below)
<img src="sample_images/imgMemory.jpeg" width="400"/>    

## Technology stack
| Layer | Technology | Justification |
|:-----------|:-----------:|-------------------------------------:|
| Backend    |   Uvicorn + FastAPI    |   Async-native, WebSocket support, auto OpenAPI docs   |
| AI Model   |   Anthropic Claude     |   Multimodal, context and streaming                    |
| Frontend   |   Vanilla JS + CSS     |   Fast load and easy to tailor to further requirments  |
| Container  |   Docker + Compose     |   Reproducible environments, ready to be cloud deployed|
| Testing    |   Pytest + asyncio     |   Used for Async test support for WebSocket endpoints  |

## Project folder structure 

```bash
multimodal-ai-assistant/
├── api/
│   └── routes/
│       ├── chat.py          # WebSocket endpoint for streaming the chat
│       ├── images.py        # REST endpoint for the image analysis
│       └── audio.py         # REST endpoint for the audio transcription
├── websocket_server/
│   └── manager.py           # The multi-user connection manager 
├── image_pipeline/
│   └── processor.py         # Base64 encoding and message builder for vision 
├── text_pipeline/
│   └── processor.py         # Anthropic client and streaming logic 
├── audio_pipeline/
│   └── processor.py         # Audio encoding for Claude (haiku) 
├── embeddings/
│   └── store.py             # Semantic search, yet to be extended 
├── frontend/
│   ├── index.html           # Chat UI, simple but easy to tailor to detailed specifications
│   ├── style.css            # Design the system and format
│   └── app.js               # WebSocket client, history management
├── tests/
│   └── test_chat.py         
├── docker/
│   └── Dockerfile           # Docker configuration to get the assistant ready for Cloud deployment 
├── docker-compose.yml
├── main.py                  # App entry point
└── requirements.txt
└── sample_images.txt        # Results obtained with test chat

