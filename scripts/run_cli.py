from local_doc_agent.agent import creat_agent
from local_doc_agent.config import MODEL_CONFIGS


def main():
    # 让用户选择模型
    available = ", ".join(MODEL_CONFIGS.keys())
    while True:
        model_name = input(f"Choose a model [{available}]: ").strip()
        if model_name in MODEL_CONFIGS:
            break
        print(f"Unknown model. Available: {available}")

    # 创建 Agent
    agent = creat_agent(model_name)

    # 检查是否初始化失败
    if isinstance(agent, str):
        print(f"[FATAL] {agent}")
        return

    print(f"Using model: {model_name}")
    print("Type 'quit' to exit.\n")

    # 交互循环
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        result = agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        print(f"Assistant: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()