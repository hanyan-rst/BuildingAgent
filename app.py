import streamlit as st
import requests
import json

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI助手", layout="wide")
st.title("AI助手")

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = None

if 'input_tokens' not in st.session_state:
    st.session_state.input_tokens = 0
if 'output_tokens' not in st.session_state:
    st.session_state.output_tokens = 0

user_input = st.chat_input("请输入您的问题...")

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        with requests.post(BACKEND_URL, json={"prompt": user_input, "session_id": st.session_state.session_id}, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    if data["type"] == "chunk":
                        full_response = data["text"]
                        message_placeholder.markdown(full_response + "▌")
                    elif data["type"] == "done":
                        st.session_state.session_id = data.get("session_id")
                        st.session_state.input_tokens = data.get("input_tokens", 0)
                        st.session_state.output_tokens = data.get("output_tokens", 0)
                    elif data["type"] == "error":
                        full_response = data["message"]
                        message_placeholder.markdown(full_response)
                        break

        message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        st.caption(f"🧮 Token 消耗：输入 {st.session_state.input_tokens} | 输出 {st.session_state.output_tokens} | 总共 {st.session_state.input_tokens + st.session_state.output_tokens}")
