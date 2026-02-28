import asyncio
import time
import uuid
from fastapi import APIRouter, HTTPException
from openai import APIError, APITimeoutError, AuthenticationError, RateLimitError
from clients.llm_client import async_client
from schemas.chat import ChatRequestBody
from store import history_store

router = APIRouter()

def get_session_id(session_id: str | None) -> str:
    return session_id or str(uuid.uuid4())

def append_message(session_id: str, role: str, content: str):
    history_store.setdefault(session_id, [])
    history_store[session_id].append({
        "role": role,
        "content": content,
        "ts": int(time.time())
    })

@router.post("/chat")
async def chat(request_body: ChatRequestBody):
    prompt = request_body.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt 不能为空")
    
    session_id = get_session_id(request_body.session_id)

    history = history_store.get(session_id, [])
    messages = history + [
        {
            "role": "user",
            "content": prompt
        }
    ]

    try:
        resp = await asyncio.wait_for(
            async_client.chat.completions.create(
                model = "qwen3.5-flash",
                messages = messages,
                temperature = 0.7,
                max_tokens = 1024
            ),
            timeout=60,
        )
        reply = resp.choices[0].message.content

        append_message(session_id, "user", prompt)
        append_message(session_id, "assistant", reply)
        
        return {
            "session_id": session_id,
            "reply": reply
        }
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="上游服务调用超时")
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="API key 无效或权限不足")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="API 调用频率超过限制")
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="上游服务调用超时")
    except APIError:
        raise HTTPException(status_code=502, detail="上游服务异常")
    except Exception:
        raise HTTPException(status_code=500, detail="服务内部异常")
