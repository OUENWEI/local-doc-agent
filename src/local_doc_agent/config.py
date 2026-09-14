import os
from dotenv import load_dotenv

load_dotenv()

# ---------- API Keys ----------
DS_API_KEY = os.getenv("DS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")


MODEL_CONFIGS = {
    "deepseekV4.1flash": {
        "model": "deepseek-flash",
        "base_url": "https://api.deepseek.com",
        "api_key_env": DS_API_KEY,
    },
    "deepseekV4pro": {
        "model": "deepseek-v4-pro",
        "base_url": "https://api.deepseek.com",
        "api_key_env": DS_API_KEY,
    },
    "chatgpt6astra": {
        "model": "gpt-6-astra",
        "base_url": "https://api.openai.com/v1",
        "api_key_env": OPENAI_API_KEY,
    },
    "qwen3.8max": {
        "model": "qwen3.8-max",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key_env": DASHSCOPE_API_KEY,
    },
    "qwen3.7plus": {
        "model": "qwen3.7-plus",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key_env": DASHSCOPE_API_KEY,
    },
    "qwen3.8flash": {
        "model": "qwen3.8-flash",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "api_key_env": DASHSCOPE_API_KEY,
    },
}

# 默认模型别名（取字典的第一个键）
DEFAULT_MODEL_ALIAS = "deepseekV4.1flash"
