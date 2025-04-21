import json
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Request
from dashscope import Application
from http import HTTPStatus
import asyncio
import os

API_KEY = "sk-REPLACE_YOUR_SK"
APP_ID = "REPLACE_YOUR_APP_ID"

app = FastAPI()

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    prompt = data.get("prompt")
    session_id = data.get("session_id")

    async def stream_response():
        try:
            responses = Application.call(
                api_key=API_KEY,
                app_id=APP_ID,
                prompt=prompt,
                session_id=session_id,
                stream=True,
                incremental_output=True
            )

            full_text = ""
            new_session_id = None
            input_tokens = 0
            output_tokens = 0

            for response in responses:
                if response.status_code != HTTPStatus.OK:
                    yield json.dumps({
                        "type": "error",
                        "message": f"请求失败: code={response.status_code}, message={response.message}"
                    }) + "\n"
                    return

                # 收集 session_id
                if not new_session_id and hasattr(response.output, 'session_id'):
                    new_session_id = response.output.session_id

                # 收集 usage
                if hasattr(response, 'usage') and response.usage and response.usage.models:
                    usage_info = response.usage.models[0]
                    input_tokens = usage_info.input_tokens
                    output_tokens = usage_info.output_tokens

                # 每次输出部分文本
                full_text += response.output.text
                yield json.dumps({
                    "type": "chunk",
                    "text": full_text
                }) + "\n"

            # 最终发送统计信息
            yield json.dumps({
                "type": "done",
                "session_id": new_session_id,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            }) + "\n"

        except Exception as e:
            yield json.dumps({
                "type": "error",
                "message": f"发生错误: {str(e)}"
            }) + "\n"

    return StreamingResponse(stream_response(), media_type="text/plain")
