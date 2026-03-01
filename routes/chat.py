import asyncio
import time
import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException
from openai import APIError, APITimeoutError, AuthenticationError, RateLimitError
from clients.llm_client import async_client
from db.engine import SessionLocal
from sqlalchemy.orm import Session
from db.models import Conversation, Message
from schemas.chat import ChatRequestBody
from store import history_store

# 配置 logger
logger = logging.getLogger(__name__)

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

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/chat")
async def chat(body: ChatRequestBody, db: Session = Depends(get_db)):
    prompt = body.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt 不能为空")
    
    conversation = None

    if not body.session_id:
        conversation = Conversation(title = "新对话", user_id = "default_user")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
    else:
        # query
        conversation = db.query(Conversation).filter(Conversation.id == body.session_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")

    # 构造历史消息列表，过滤掉无关字段
    history = [
        {"role": msg.role, "content": msg.content} 
        for msg in conversation.messages
    ]

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

        conversation.messages.append(Message(
            role = "user",
            content = prompt
        ))
        conversation.messages.append(Message(
            role = "assistant",
            content = reply
        ))
        db.commit()
        
        return {
            "session_id": conversation.id,
            "reply": reply
        }
    except asyncio.TimeoutError as e:
        logger.error(f"TimeoutError: {str(e)}")
        raise HTTPException(status_code=504, detail="上游服务调用超时")
    except AuthenticationError as e:
        logger.error(f"AuthenticationError: {str(e)}")
        raise HTTPException(status_code=401, detail="API key 无效或权限不足")
    except RateLimitError as e:
        logger.error(f"RateLimitError: {str(e)}")
        raise HTTPException(status_code=429, detail="API 调用频率超过限制")
    except APITimeoutError as e:
        logger.error(f"APITimeoutError: {str(e)}")
        raise HTTPException(status_code=504, detail="上游服务调用超时")
    except APIError as e:
        logger.error(f"APIError: {str(e)}")
        raise HTTPException(status_code=502, detail="上游服务异常")
    except Exception as e:
        logger.exception("Unexpected error occurred")
        raise HTTPException(status_code=500, detail="服务内部异常")

@router.get('/history/{id}')
async def get_history(id: str, db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="对话不存在")
    return [{"role": msg.role, "content": msg.content} for msg in conversation.messages]
