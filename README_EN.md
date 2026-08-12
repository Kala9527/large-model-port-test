# Large Model Port Test Tool

[中文说明](./README.md)

A server-rendered web tool for testing LLM API connectivity. Enter a model service URL, API key, model ID, and call mode, then the app sends a real test message `Hi` and displays the response, HTTP status code, successful protocol, model output, raw failure details, and possible troubleshooting hints.

It is built for the very common "why can't my model endpoint connect?" moment. If it saves you a few rounds of endpoint guessing, stars, forks, issues, and provider preset PRs are all welcome.

## Highlights

- Browser-based testing form for real model requests.
- Supports OpenAI Chat Completions, OpenAI Responses, Anthropic Messages, Gemini Native, Azure OpenAI, Ollama, and more.
- `auto` mode tries common protocols in order and stops after the first success.
- Fully custom JSON request mode with method, path, headers, and body templates.
- Built-in presets for OpenAI, DeepSeek, DashScope, SiliconFlow, Zhipu, Volcengine Ark, Moonshot, OpenRouter, Groq, LM Studio, vLLM, Ollama, and others.
- Failure analysis with status code, raw response, and common troubleshooting directions.
- API key masking in the UI to reduce accidental leakage in screenshots.
- `/health` endpoint for quick service checks.

## Tech Stack

- Python 3.11+
- FastAPI
- Uvicorn
- Jinja2
- httpx
- HTML / CSS

## Quick Start

### 1. Install dependencies

Windows users can run:

```powershell
.\start.bat
```

The script checks dependencies and starts the service.

Or install manually:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Start the app

```powershell
python -m uvicorn main:app --host 0.0.0.0 --port 5181
```

Open:

```text
http://127.0.0.1:5181
```

Health check:

```text
http://127.0.0.1:5181/health
```

## Usage

1. Choose a provider preset or select Custom.
2. Enter the model service URL, such as `https://api.openai.com/v1` or `http://127.0.0.1:8000/v1`.
3. Enter an API key. Leave it empty for local services without authentication.
4. Enter the model ID. For Azure OpenAI, use the deployment name.
5. Choose a call mode. Use `auto` for first-time troubleshooting.
6. Run the test and inspect the status code, request protocol, model answer, and failure analysis.

## Supported Call Modes

- `openai_chat_completions`
- `openai_responses`
- `anthropic_messages`
- `azure_openai_chat_completions`
- `gemini_generate_content`
- `message_chat`
- `generate`
- `ollama_chat`
- `ollama_generate`
- `custom_request`
- `auto`

## Custom JSON Requests

In `custom_request` mode, you can configure:

- HTTP method: `POST`, `GET`, `PUT`, `PATCH`, `DELETE`
- Endpoint path: relative path like `/chat/completions` or a full URL
- Header JSON
- Body JSON

Supported placeholders:

```text
{api_key}
{model}
{model_id}
{deployment}
{message}
{temperature}
{api_version}
```

## GitHub Topics

`python`, `fastapi`, `llm`, `openai-compatible`, `api-testing`, `model-endpoint`, `ollama`, `anthropic`, `gemini`, `azure-openai`

## License

MIT License is recommended if you plan to publish this project as open source.
