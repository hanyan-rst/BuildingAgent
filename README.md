# 百炼webui

这是一个基于百炼API的网页接入demo，通过Streamlit提供交互式界面。

## 功能特点

- 交互式聊天界面
- 连续对话能力（保持会话上下文）
- 流式输出内容
- 显示对话token数
- 简洁易用的用户界面
- 支持并发

## 安装说明

1. Python 3.8或更高版本
2. 安装依赖：
```bash
pip install streamlit dashscope fastapi uvicorn requests
```

## 使用方法

1. 启动应用：
```bash
uvicorn backend:app --host 0.0.0.0 --port 8000
streamlit run app.py
```

2. 在浏览器中打开URL
   http://127.0.0.1:8501
