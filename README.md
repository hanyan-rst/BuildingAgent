# 建筑规范查询助手

这是一个基于百炼API的建筑规范查询助手，通过Streamlit提供交互式界面，帮助用户查询建筑规范相关信息。

## 功能特点

- 交互式聊天界面
- 连续对话能力（保持会话上下文）
- 建筑规范专业知识查询
- 简洁易用的用户界面

## 安装说明

1. 确保已安装Python 3.8或更高版本
2. 安装必要的依赖包：

```bash
pip install streamlit dashscope
```

## 使用方法

1. 启动应用：

```bash
streamlit run streamlit_app_simple.py
```

2. 在浏览器中打开显示的本地URL（通常是http://localhost:8501）
3. 在输入框中输入您的建筑规范相关问题
4. 查看AI助手的回答
5. 可以通过侧边栏的"清除对话历史"按钮重新开始对话

## 文件说明

- `agent.py`: 百炼API调用的基础实现
- `streamlit_app_simple.py`: Streamlit交互式应用实现
- `requirements.txt`: 项目依赖列表

## 注意事项

- 应用使用了百炼API，请确保网络连接正常
- 首次运行可能需要等待依赖安装完成