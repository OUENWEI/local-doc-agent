import asyncio
import uuid
import streamlit as st
from local_doc_agent.agent import creat_agent
from local_doc_agent.config import MODEL_CONFIGS

st.set_page_config(page_title="本地文档助手",  layout="wide")
st.title("本地文档助手")

# ---------- 持久化事件循环 ----------
if "event_loop" not in st.session_state:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    st.session_state.event_loop = loop

def run_async(coro):
    return st.session_state.event_loop.run_until_complete(coro)

# ---------- 其他初始化 ----------
if "agent" not in st.session_state:
    st.session_state.agent = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# ---------- 侧边栏 ----------
with st.sidebar:
    st.header("设置")
    model_name = st.selectbox("选择模型", list(MODEL_CONFIGS.keys()))
    import_blender = st.checkbox("导入 Blender 工具", value=False)

    if st.button("启动 Agent", type="primary"):
        with st.spinner("正在加载 Agent..."):
            st.session_state.agent = run_async(
                creat_agent(model_name, import_blender=import_blender)
            )
        if isinstance(st.session_state.agent, str):
            st.error(st.session_state.agent)
            st.session_state.agent = None
        else:
            st.success(f"已启动，模型：{model_name}")

    if st.button("清除对话"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

# ---------- 展示历史 ----------
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------- 聊天输入 ----------
if prompt := st.chat_input("请输入问题..."):
    if st.session_state.agent is None:
        st.warning("请先在左侧启动 Agent。")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                result = run_async(
                    st.session_state.agent.ainvoke(
                        {"messages": [{"role": "user", "content": prompt}]},
                        config,
                    )
                )
                reply = result["messages"][-1].content
                st.write(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})