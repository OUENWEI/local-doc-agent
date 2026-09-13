import logging
from langchain.chat_models import init_chat_model
from local_doc_agent.logger import logger
from langchain.agents import create_agent
from local_doc_agent.config import MODEL_CONFIGS, DEFAULT_MODEL_ALIAS
from local_doc_agent.tools.about_dock import docx_read

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
            api_key = cfg["api_key"],

        )

        tools = [docx_read]

        system_prompt = " " #暂时没写，等待书写，已做高亮标记
        agent = create_agent(
            model = model,
            tools = tools,
            system_prompt = system_prompt,
        )

        return agent










