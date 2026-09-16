import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from local_doc_agent.logger import logger
from local_doc_agent.config import MODEL_CONFIGS
from local_doc_agent.tools.about_docx import docx_read
from local_doc_agent.tools.about_excel import excel_read


def creat_agent(model_name: str):
    if model_name not in MODEL_CONFIGS:
        logger.info(f"Can't find the {model_name} model")
        return "error : do not found model"

    cfg = MODEL_CONFIGS[model_name]

    model = init_chat_model(
        cfg["model"],
        model_provider="openai",
        base_url=cfg["base_url"],
        api_key=cfg["api_key_env"],
    )

    tools = [docx_read, excel_read]

    # 短期记忆：SQLite 持久化到硬盘
    conn = sqlite3.connect(
        "short_memory.db",
        check_same_thread=False,
        isolation_level=None,   # 关键：自动提交模式，避免事务冲突
    )
    checkpointer = SqliteSaver(conn)

    system_prompt = """你是一个本地文档助手，可以读取本地Excel和Word文件并回答问题。请用中文回答。
当用户提供个人信息（名字、喜好等）时，请在回复中自然地提及或确认，不要忽略。
请始终用与用户输入相同的语言进行回复。
"""

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
    )
    return agent