# lang_test

说明：本示例演示如何安全地提供 OpenAI/Deepseek/Tavily API Key，避免将密钥硬编码到源码中。

准备工作

1. 安装依赖：

```bash
pip3 install openai python-dotenv
```

2. 在 shell 中设置环境变量（示例）：

```bash
export OPENAI_API_KEY="sk-..."
# 如果你使用 Tavily API：
export TAVILY_API_KEY="tavily-..."
```

快速运行

- 初始化客户端（不会发起网络请求）：

```bash
# 在项目根目录下运行：
OPENAI_API_KEY=test python3 api_test.py
# 你应该看到："API client initialized..." 的信息
```

- 运行实际的示例请求（会发起网络请求并消耗配额）：

```bash
# 只有当你确认要发起真实请求时才执行：
OPENAI_API_KEY="sk-..." RUN_DEMO=1 python3 api_test.py
```

安全提示

- 永远不要把真实的 API key 提交到 Git 仓库。使用环境变量或 CI secret 管理密钥。
- 推荐在本地使用 `.env` 文件并配合 gitignore 把它排除在版本控制之外。