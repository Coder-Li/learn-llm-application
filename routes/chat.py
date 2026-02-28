from fastapi import APIRouter
from clients.llm_client import client
from schemas.chat import ChatRequestBody

router = APIRouter()

@router.post("/chat")
def chat(request_body: ChatRequestBody):
    resp = client.chat.completions.create(
        model = "qwen3.5-flash",
        messages = [
            {
                "role": "user",
                "content": request_body.prompt
            }
        ],
        temperature = 0.7,
        max_tokens = 1024
    )
    return resp.choices[0].message.content
