import asyncio
from fastapi import APIRouter, HTTPException
from openai import APIError, APITimeoutError, AuthenticationError, RateLimitError
from clients.llm_client import async_client
from schemas.chat import ChatRequestBody

router = APIRouter()

@router.post("/chat")
async def chat(request_body: ChatRequestBody):
    prompt = request_body.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt 不能为空")
    try:
        resp = await asyncio.wait_for(
            async_client.chat.completions.create(
                model = "qwen3.5-flash",
                messages = [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature = 0.7,
                max_tokens = 1024
            ),
            timeout=60,
        )
        return resp.choices[0].message.content
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
