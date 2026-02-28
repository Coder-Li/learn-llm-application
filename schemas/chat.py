from pydantic import BaseModel

class ChatRequestBody(BaseModel):
    prompt: str
