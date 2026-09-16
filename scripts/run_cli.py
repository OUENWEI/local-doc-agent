from local_doc_agent.agent import creat_agent
from local_doc_agent.config import MODEL_CONFIGS


def choose_model() -> str:
    available = ", ".join(MODEL_CONFIGS.keys())
    while True:
        model_name = input(f"Choose a model [{available}]: ").strip()
        if model_name in MODEL_CONFIGS:
            return model_name
        print(f"Unknown model. Available: {available}")


def choose_user() -> str:
    user_id = input("Enter your user id (default: default_user): ").strip()
    return user_id or "default_user"


def main():
    model_name = choose_model()
    agent = creat_agent(model_name)
    if isinstance(agent, str):
        print(f"[FATAL] {agent}")
        return

    user_id = choose_user()
    config = {"configurable": {"thread_id": user_id}}

    print(f"\nUsing model: {model_name}")
    print(f"Memory space: {user_id}")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

        if user_input.lower() == "quit":
            break

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config,
        )
        print(f"Assistant: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    main()