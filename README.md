# LLM Web Demo

一个最小可运行的 LLM API 调用示例，使用 OpenAI SDK 兼容模式进行调用。

## 环境准备

- Python 3.8+
- 安装依赖

```bash
python -m pip install -r requirements.txt
```

如果没有 requirements.txt，可以直接安装：

```bash
python -m pip install openai python-dotenv
```

## 配置环境变量

创建 `.env` 文件：

```bash
LLM_API_KEY=你的API_KEY
```

## 运行

```bash
python call-api.py
```

## 说明

- `.env` 已在 .gitignore 中忽略，不会提交
- `.env.example` 用作示例模板
