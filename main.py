import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.environ.get("LLM_API_KEY"),
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

class ChatRequestBody(BaseModel):
    prompt: str

app = FastAPI()

@app.get('/')
def read_root():
    return {
        "Hello": "World"
    }

@app.get('/items/{item_id}')
def read_item(item_id: int, q: str | None = None):
    return {
        "item_id": item_id,
        "q": q
    }

@app.post('/chat')
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