import asyncio
import sys
from local_doc_agent.agent import creat_agent, close_checkpointer
from local_doc_agent.config import MODEL_CONFIGS


def choose_model() -> str:
    available = ", ".join(MODEL_CONFIGS.keys())
    while True:
        print(f"Choose a model [{available}]: ", end="", flush=True)
        model_name = sys.stdin.readline().strip()
        if model_name in MODEL_CONFIGS:
            return model_name
        print(f"Unknown model. Available: {available}")


def choose_user() -> str:
    print("Enter your user id (default: default_user): ", end="", flush=True)
    user_id = sys.stdin.readline().strip()
    return user_id or "default_user"


async def async_input(prompt: str) -> str:
    """在异步环境里安全读取一行输入，兼容 Windows 中文输入法。"""
    print(prompt, end="", flush=True)
    line = await asyncio.to_thread(sys.stdin.readline)
    return line.rstrip("\n")


async def main():
    model_name = choose_model()
    agent = await creat_agent(model_name)
    if isinstance(agent, str):
        print(f"[FATAL] {agent}")
        return

    user_id = choose_user()
    config = {"configurable": {"thread_id": user_id}}

    print(f"\nUsing model: {model_name}")
    print(f"Memory space: {user_id}")
    print("Type 'quit' to exit.\n")

    try:
        while True:
            try:
                user_input = await async_input("You: ")
            except (KeyboardInterrupt, EOFError):
                print("\nBye.")
                break

            if not user_input:
                continue

            if user_input.lower() == "quit":
                break

            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config,
            )
            print(f"Assistant: {result['messages'][-1].content}\n")
    finally:
        await close_checkpointer()


if __name__ == "__main__":
    asyncio.run(main())