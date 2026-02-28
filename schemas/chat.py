from pydantic import BaseModel

class ChatRequestBody(BaseModel):
    session_id: str | None = None
    prompt: str
