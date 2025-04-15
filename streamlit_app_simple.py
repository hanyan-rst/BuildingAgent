import streamlit as st
import os
from http import HTTPStatus
from dashscope import Application

# 设置页面标题和配置
st.set_page_config(page_title="建筑规范查询助手", layout="wide")
st.title("建筑规范查询助手")

# 初始化会话状态
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = None

# API配置
with st.sidebar:
    st.title("API配置")
    API_KEY = st.text_input("请输入您的API_KEY", type="password")
APP_ID = "182cc4571fa84c4f89b008339600bd0b"

# 调用百炼API的函数
def call_api(prompt, session_id=None):
    try:
        response = Application.call(
            api_key=API_KEY,
            app_id=APP_ID,
            prompt=prompt,
            session_id=session_id
        )
        
        if response.status_code != HTTPStatus.OK:
            error_message = f'请求失败: code={response.status_code}, message={response.message}'
            return error_message, session_id
        
        return response.output.text, response.output.session_id
    except Exception as e:
        return f"发生错误: {str(e)}", session_id

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
        message_placeholder = st.empty()
        message_placeholder.markdown("思考中...")
        
        # 调用API获取回复
        ai_response, new_session_id = call_api(user_input, st.session_state.session_id)
        
        # 更新会话ID
        if new_session_id:
            st.session_state.session_id = new_session_id
        
        # 显示AI回复
        message_placeholder.markdown(ai_response)
        
        # 添加AI回复到历史
        st.session_state.messages.append({"role": "assistant", "content": ai_response})

# 添加使用说明和控制按钮
with st.sidebar:
    st.title("使用说明")
    st.markdown("""
    这是一个建筑规范查询助手，您可以：
    - 询问关于建筑规范的问题
    - 查询特定建筑标准的内容
    - 获取建筑设计相关的专业建议
    
    对话是连续的，助手会记住您之前的问题。
    """)
    
    # 添加清除对话按钮
    if st.button("清除对话历史"):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()

