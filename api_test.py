# Please install OpenAI SDK first: `pip3 install openai python-dotenv`
import os
from dotenv import load_dotenv
from openai import OpenAI

# 从 .env（如果存在）和环境变量加载配置
load_dotenv()

# 推荐使用环境变量名 OPENAI_API_KEY 来提供密钥
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY is not set. Set it in your environment (e.g. export OPENAI_API_KEY='sk-...') or pass api_key to the OpenAI client."
    )

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")

# 为了避免在没有明确同意的情况下发起网络请求，默认不自动运行示例。
# 要运行示例，请在命令前设置 RUN_DEMO=1
if os.environ.get("RUN_DEMO") == "1":
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=False,
    )

    print(response.choices[0].message.content)
else:
    print(
        "API client initialized. Set RUN_DEMO=1 and ensure OPENAI_API_KEY is set to run the example completion."
    )