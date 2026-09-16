from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from local_doc_agent.logger import logger
from local_doc_agent.config import MODEL_CONFIGS
from local_doc_agent.tools.about_docx import docx_read
from local_doc_agent.tools.about_excel import excel_read


# 全局持有 checkpointer 的上下文管理器和实例，防止连接被提前关闭
_checkpointer_context = None
_checkpointer = None


async def _get_checkpointer():
    """获取（或创建）异步 checkpointer，保持连接存活。"""
    global _checkpointer_context, _checkpointer
    if _checkpointer is not None:
        return _checkpointer

    _checkpointer_context = AsyncSqliteSaver.from_conn_string("short_memory.db")
    _checkpointer = await _checkpointer_context.__aenter__()
    await _checkpointer.setup()
    return _checkpointer


async def close_checkpointer():
    """程序退出时关闭 checkpointer 连接。"""
    global _checkpointer_context, _checkpointer
    if _checkpointer_context is not None:
        await _checkpointer_context.__aexit__(None, None, None)
        _checkpointer_context = None
        _checkpointer = None


async def creat_agent(model_name: str):
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

    # 连接 BlenderMCP
    client = MultiServerMCPClient({
        "blender": {
            "command": "uvx",
            "args": ["blender-mcp"],
            "transport": "stdio",
        }
    })
    blender_tools = await client.get_tools()
    logger.info(f"成功加载 {len(blender_tools)} 个 Blender 工具")

    all_tools = [docx_read, excel_read] + blender_tools

    checkpointer = await _get_checkpointer()

    system_prompt = """你是一个本地文档与3D建模助手。
你可以读取本地Excel和Word文件并回答问题。
你还可以通过 Blender 工具进行 3D 建模操作。
当用户提供个人信息时，请自然地提及或确认。
请始终用与用户输入相同的语言进行回复。
"""

    agent = create_agent(
        model=model,
        tools=all_tools,
        system_prompt=system_prompt,
        checkpointer=checkpointer,
    )
    return agent