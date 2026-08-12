# 大模型端口测试工具

[English](./README_EN.md)

一个纯后端渲染的模型接口连通性测试工具。打开网页后填写模型服务 URL、API Key、模型 ID 和调用方式，工具会向目标接口发送固定测试消息 `Hi`，并展示真实响应、HTTP 状态码、成功调用方式、模型回答、失败原始错误和可能原因分析。

它适合用来快速判断“模型服务到底能不能调通”“Base URL 写没写对”“是不是协议选错了”。如果这个工具帮你少排了几次接口坑，欢迎 Star 一下，也欢迎把你常用的供应商预设提 PR。

## 功能亮点

- Web 表单测试：浏览器填写参数，一键发起真实请求。
- 多协议支持：覆盖 OpenAI Chat Completions、OpenAI Responses、Anthropic Messages、Gemini Native、Azure OpenAI、Ollama 等。
- 自动探测模式：`auto` 会按多个常见协议依次尝试，成功即停止。
- 自定义 JSON 请求：可自定义 HTTP 方法、路径、Header JSON 和 Body JSON。
- 供应商预设：内置 OpenAI、DeepSeek、阿里云百炼、硅基流动、智谱、火山方舟、Moonshot、OpenRouter、Groq、LM Studio、vLLM、Ollama 等。
- 错误分析：失败时给出状态码、原始响应和常见排查方向。
- 密钥脱敏：页面展示会隐藏完整 API Key，降低误截图泄露风险。
- 健康检查：提供 `/health` 接口，便于确认服务是否启动。

## 技术栈

- Python 3.11+
- FastAPI
- Uvicorn
- Jinja2
- httpx
- HTML / CSS

## 快速开始

### 1. 安装依赖

Windows 用户可以使用项目脚本：

```powershell
.\start.bat
```

脚本会检查依赖并启动服务。

也可以手动安装：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. 启动服务

```powershell
python -m uvicorn main:app --host 0.0.0.0 --port 5181
```

浏览器访问：

```text
http://127.0.0.1:5181
```

健康检查：

```text
http://127.0.0.1:5181/health
```

## 使用方法

1. 选择供应商预设，或选择“自定义”。
2. 填写模型服务 URL，例如 `https://api.openai.com/v1` 或 `http://127.0.0.1:8000/v1`。
3. 填写 API Key。无鉴权的本地服务可留空。
4. 填写模型 ID。Azure OpenAI 场景下这里填写 deployment name。
5. 选择调用方式，第一次排查建议使用 `auto`。
6. 点击测试，查看状态码、请求方式、模型回答和错误分析。

## 支持的调用方式

- `openai_chat_completions`：OpenAI 兼容 `/chat/completions`
- `openai_responses`：OpenAI `/responses`
- `anthropic_messages`：Anthropic Claude `/v1/messages`
- `azure_openai_chat_completions`：Azure OpenAI deployment 调用方式
- `gemini_generate_content`：Google Gemini 原生 `generateContent`
- `message_chat`：通用 `/chat`
- `generate`：通用 `/generate`
- `ollama_chat`：Ollama `/api/chat`
- `ollama_generate`：Ollama `/api/generate`
- `custom_request`：完全自定义 HTTP 请求
- `auto`：按常见协议顺序自动尝试

## 自定义 JSON 请求

选择 `custom_request` 后，可填写：

- HTTP 方法：`POST`、`GET`、`PUT`、`PATCH`、`DELETE`
- 请求路径：相对路径如 `/chat/completions`，或完整 URL
- Header JSON：例如 `{"Authorization": "Bearer {api_key}", "Content-Type": "application/json"}`
- Body JSON：例如 `{"model": "{model}", "messages": [{"role": "user", "content": "{message}"}]}`

支持占位符：

```text
{api_key}
{model}
{model_id}
{deployment}
{message}
{temperature}
{api_version}
```

## 项目结构

```text
LargeModelPortTest/
├─ app/
│  ├─ error_analysis.py
│  ├─ providers.py
│  └─ tester.py
├─ static/
│  └─ styles.css
├─ templates/
│  └─ index.html
├─ main.py
├─ requirements.txt
├─ start.bat
└─ README.md
```

## 上传 GitHub 前建议

本项目已经提供 `.gitignore`，会排除：

- `__pycache__/`
- `.tmp/`
- `.venv/`
- 日志文件
- 本地环境变量文件

请不要把真实 API Key、内网服务地址截图或私有供应商配置写进仓库。

## GitHub Topics 建议

`python`, `fastapi`, `llm`, `openai-compatible`, `api-testing`, `model-endpoint`, `ollama`, `anthropic`, `gemini`, `azure-openai`

## License

如果你准备开源，建议选择 MIT License，方便社区复用和贡献供应商适配。
