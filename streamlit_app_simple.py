import streamlit as st
import os
from http import HTTPStatus
from dashscope import Application

API_KEY = "sk-12345678901234567890"
APP_ID = "百炼唯一应用ID"

# 设置页面标题和配置
st.set_page_config(page_title="AI助手", layout="wide")
st.title("AI助手")

# 初始化会话状态
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = None

total_input_tokens = 0
total_output_tokens = 0

# 调用百炼API的函数
def call_api(prompt, session_id=None):
    try:
        global total_input_tokens, total_output_tokens
        responses = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=prompt,
            session_id=session_id,
            stream=True,
            incremental_output=True
        )

        full_response = ""
        new_session_id = None

        for response in responses:
            if response.status_code != HTTPStatus.OK:
                error_message = f'请求失败: code={response.status_code}, message={response.message}'
                yield error_message, session_id
                return

            if not new_session_id and hasattr(response.output, 'session_id'):
                new_session_id = response.output.session_id

            if hasattr(response, 'usage') and response.usage and response.usage.models:
                usage_info = response.usage.models[0]
                total_input_tokens = usage_info.input_tokens
                total_output_tokens = usage_info.output_tokens

            full_response += response.output.text
            yield full_response, new_session_id

    except Exception as e:
        yield f"发生错误: {str(e)}", session_id

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
user_input = st.chat_input("请输入您的问题...")

# 处理用户输入
if user_input:
    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(user_input)

    # 显示AI正在思考
    with st.chat_message("assistant"):
        # 创建占位符
        message_placeholder = st.empty()
        full_text = ""
        for chunk, new_session_id in call_api(user_input, st.session_state.session_id):
            full_text = chunk
            message_placeholder.markdown(full_text + "▌")  # 游标动画效果

# 最终显示内容
        message_placeholder.markdown(full_text)
        st.caption(f"🧮 Token 消耗：输入 {total_input_tokens} | 输出 {total_output_tokens} | 总共 {total_input_tokens + total_output_tokens}")

# 保存会话ID与对话
        if new_session_id:
            st.session_state.session_id = new_session_id
        st.session_state.messages.append({"role": "assistant", "content": full_text})

# 添加使用说明和控制按钮
with st.sidebar:
    st.title("使用说明")
    st.markdown("""
    对话是连续的，助手会记住您之前的问题。
    """)

    # 添加清除对话按钮
    if st.button("清除对话历史"):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()
