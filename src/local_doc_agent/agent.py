from langchain.chat_models import init_chat_model
from local_doc_agent.logger import logger
from langchain.agents import create_agent
from local_doc_agent.config import MODEL_CONFIGS
from local_doc_agent.tools.about_docx import docx_read
from local_doc_agent.tools.about_excel import excel_read




def creat_agent(model_name : str) :
    if model_name not in MODEL_CONFIGS:
        logger.info(f"Can't find the {model_name} model")
        return "error : do not found model"
    # Return a string instead of raising, so the caller can decide
    # whether to terminate the process (agreed error-handling convention).
    else:
        cfg = MODEL_CONFIGS[model_name]
        model = init_chat_model(
            cfg["model"],
            model_provider="openai",
            base_url = cfg["base_url"],
            api_key = cfg["api_key_env"],

        )

        tools = [docx_read,excel_read]

        system_prompt =  """You are a local document assistant. You have access to two tools:
- docx_read: reads Word documents (.docx)
- excel_read: reads Excel spreadsheets (.xlsx)

Important rules when handling tool results:
1. If a tool returns a string starting with 'error:', it means the tool failed.
   You must:
   a) Try another tool that might be suitable.
   b) If no tool can handle the task, explain the situation to the user clearly.
2. If a tool returns a string starting with 'warning:', the content is truncated.
   You must inform the user about the limitation.

Always respond in the user's language.
"""
        agent = create_agent(
            model = model,
            tools = tools,
            system_prompt = system_prompt,
        )

        return agent










