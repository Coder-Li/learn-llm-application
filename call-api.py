import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key = os.environ.get("LLM_API_KEY"),
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
)

resp = client.chat.completions.create(
    model = "qwen3.5-flash",
    messages = [
        {
            "role": "user",
            "content": "你好,介绍一下你自己"
        }
    ],
    temperature = 0.7,
    max_tokens = 1024
)

print(resp.choices[0].message.content)
