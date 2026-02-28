import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

async_client = AsyncOpenAI(
    api_key = os.environ.get("LLM_API_KEY"),
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    timeout = 120
)
