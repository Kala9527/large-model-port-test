from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProviderPreset:
    id: str
    name: str
    base_url: str
    call_mode: str
    category: str
    description: str = ""
    api_version: str = ""
    custom_http_method: str = "POST"
    custom_endpoint_path: str = ""
    custom_headers_json: str = ""
    custom_body_json: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


PROVIDER_PRESETS: tuple[ProviderPreset, ...] = (
    ProviderPreset(
        id="custom",
        name="自定义",
        base_url="",
        call_mode="auto",
        category="Custom",
        description="完全自定义 URL、模型和请求方式。",
    ),
    ProviderPreset(
        id="openai_chat",
        name="OpenAI Chat Completions",
        base_url="https://api.openai.com/v1",
        call_mode="openai_chat_completions",
        category="Global",
        description="OpenAI 兼容 Chat Completions：POST /chat/completions。",
    ),
    ProviderPreset(
        id="openai_responses",
        name="OpenAI Responses",
        base_url="https://api.openai.com/v1",
        call_mode="openai_responses",
        category="Global",
        description="OpenAI Responses API：POST /responses。",
    ),
    ProviderPreset(
        id="anthropic_claude",
        name="Anthropic Claude",
        base_url="https://api.anthropic.com",
        call_mode="anthropic_messages",
        category="Global",
        description="Claude Messages API：POST /v1/messages，使用 x-api-key 和 anthropic-version。",
        api_version="2023-06-01",
    ),
    ProviderPreset(
        id="google_gemini_openai",
        name="Google Gemini OpenAI 兼容",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        call_mode="openai_chat_completions",
        category="Global",
        description="Gemini 的 OpenAI 兼容入口，API Key 仍填写在 api_key。",
    ),
    ProviderPreset(
        id="google_gemini_native",
        name="Google Gemini Native",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        call_mode="gemini_generate_content",
        category="Global",
        description="Gemini 原生 generateContent：POST /models/{model}:generateContent?key={api_key}。",
    ),
    ProviderPreset(
        id="azure_openai",
        name="Azure OpenAI",
        base_url="https://{resource-name}.openai.azure.com",
        call_mode="azure_openai_chat_completions",
        category="Cloud",
        description="Azure OpenAI Chat Completions，模型_id 填 Azure deployment name。",
        api_version="2024-10-21",
    ),
    ProviderPreset(
        id="aliyun_dashscope_cn",
        name="阿里云百炼 DashScope 中国站",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        call_mode="openai_chat_completions",
        category="China",
        description="阿里云百炼 OpenAI 兼容接口。",
    ),
    ProviderPreset(
        id="aliyun_dashscope_us",
        name="阿里云百炼 美国弗吉尼亚",
        base_url="https://dashscope-us.aliyuncs.com/compatible-mode/v1",
        call_mode="openai_chat_completions",
        category="China",
        description="阿里云百炼美国区域 OpenAI 兼容接口。",
    ),
    ProviderPreset(
        id="aliyun_maas_beijing",
        name="阿里云百炼 Workspace 北京",
        base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        call_mode="openai_chat_completions",
        category="China",
        description="将 {WorkspaceId} 替换为实际工作空间 ID。",
    ),
    ProviderPreset(
        id="aliyun_maas_singapore",
        name="阿里云百炼 Workspace 新加坡",
        base_url="https://{WorkspaceId}.ap-southeast-1.maas.aliyuncs.com/compatible-mode/v1",
        call_mode="openai_chat_completions",
        category="China",
        description="将 {WorkspaceId} 替换为实际工作空间 ID。",
    ),
    ProviderPreset(
        id="aliyun_maas_tokyo",
        name="阿里云百炼 Workspace 日本东京",
        base_url="https://{WorkspaceId}.ap-northeast-1.maas.aliyuncs.com/compatible-mode/v1",
        call_mode="openai_chat_completions",
        category="China",
        description="将 {WorkspaceId} 替换为实际工作空间 ID。",
    ),
    ProviderPreset(
        id="aliyun_anthropic_cn",
        name="阿里云百炼 Anthropic 协议",
        base_url="https://dashscope.aliyuncs.com/apps/anthropic",
        call_mode="anthropic_messages",
        category="China",
        description="阿里云百炼 Anthropic 兼容入口。",
        api_version="2023-06-01",
    ),
    ProviderPreset(
        id="siliconflow_openai",
        name="硅基流动 OpenAI 兼容",
        base_url="https://api.siliconflow.cn/v1",
        call_mode="openai_chat_completions",
        category="China",
        description="硅基流动 OpenAI 兼容 Chat Completions，模型_id 由用户填写。",
    ),
    ProviderPreset(
        id="deepseek",
        name="DeepSeek 官方",
        base_url="https://api.deepseek.com",
        call_mode="openai_chat_completions",
        category="China",
        description="DeepSeek OpenAI 格式 Chat Completions。",
    ),
    ProviderPreset(
        id="zhipu_general",
        name="智谱普通 API",
        base_url="https://open.bigmodel.cn/api/paas/v4",
        call_mode="openai_chat_completions",
        category="China",
        description="智谱 OpenAI 兼容普通 API。",
    ),
    ProviderPreset(
        id="zhipu_coding",
        name="智谱 Coding Plan",
        base_url="https://open.bigmodel.cn/api/coding/paas/v4",
        call_mode="openai_chat_completions",
        category="China",
        description="智谱 Coding Plan OpenAI 兼容入口。",
    ),
    ProviderPreset(
        id="volcengine_ark",
        name="火山方舟",
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        call_mode="openai_chat_completions",
        category="China",
        description="火山方舟 OpenAI 兼容 Chat Completions。",
    ),
    ProviderPreset(
        id="moonshot",
        name="Moonshot Kimi",
        base_url="https://api.moonshot.cn/v1",
        call_mode="openai_chat_completions",
        category="China",
        description="Moonshot/Kimi OpenAI 兼容接口。",
    ),
    ProviderPreset(
        id="baichuan",
        name="百川智能",
        base_url="https://api.baichuan-ai.com/v1",
        call_mode="openai_chat_completions",
        category="China",
        description="百川 OpenAI 兼容接口。",
    ),
    ProviderPreset(
        id="minimax",
        name="MiniMax",
        base_url="https://api.minimax.chat/v1",
        call_mode="openai_chat_completions",
        category="China",
        description="MiniMax OpenAI 兼容接口。",
    ),
    ProviderPreset(
        id="openrouter",
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        call_mode="openai_chat_completions",
        category="Global",
        description="OpenRouter OpenAI 兼容聚合接口。",
    ),
    ProviderPreset(
        id="mistral",
        name="Mistral AI",
        base_url="https://api.mistral.ai/v1",
        call_mode="openai_chat_completions",
        category="Global",
        description="Mistral OpenAI 兼容 Chat Completions。",
    ),
    ProviderPreset(
        id="groq",
        name="Groq",
        base_url="https://api.groq.com/openai/v1",
        call_mode="openai_chat_completions",
        category="Global",
        description="Groq OpenAI 兼容入口。",
    ),
    ProviderPreset(
        id="xai",
        name="xAI Grok",
        base_url="https://api.x.ai/v1",
        call_mode="openai_chat_completions",
        category="Global",
        description="xAI OpenAI 兼容入口。",
    ),
    ProviderPreset(
        id="together",
        name="Together AI",
        base_url="https://api.together.xyz/v1",
        call_mode="openai_chat_completions",
        category="Global",
        description="Together AI OpenAI 兼容入口。",
    ),
    ProviderPreset(
        id="deepinfra",
        name="DeepInfra",
        base_url="https://api.deepinfra.com/v1/openai",
        call_mode="openai_chat_completions",
        category="Global",
        description="DeepInfra OpenAI 兼容入口。",
    ),
    ProviderPreset(
        id="lmstudio",
        name="LM Studio 本地",
        base_url="http://127.0.0.1:1234/v1",
        call_mode="openai_chat_completions",
        category="Local",
        description="LM Studio 本地 OpenAI 兼容服务。",
    ),
    ProviderPreset(
        id="vllm",
        name="vLLM OpenAI Server",
        base_url="http://127.0.0.1:8000/v1",
        call_mode="openai_chat_completions",
        category="Local",
        description="vLLM OpenAI 兼容服务。",
    ),
    ProviderPreset(
        id="ollama_chat",
        name="Ollama Chat",
        base_url="http://127.0.0.1:11434",
        call_mode="ollama_chat",
        category="Local",
        description="Ollama 原生 /api/chat。",
    ),
    ProviderPreset(
        id="ollama_generate",
        name="Ollama Generate",
        base_url="http://127.0.0.1:11434",
        call_mode="ollama_generate",
        category="Local",
        description="Ollama 原生 /api/generate。",
    ),
    ProviderPreset(
        id="austpic_custom",
        name="Austpic / 其他 OpenAI 兼容",
        base_url="",
        call_mode="openai_chat_completions",
        category="Custom",
        description="未内置固定 endpoint，请填写官方 Base URL；默认按 OpenAI 兼容 Chat Completions 测试。",
    ),
    ProviderPreset(
        id="custom_json_request",
        name="完全自定义 JSON 请求",
        base_url="",
        call_mode="custom_request",
        category="Custom",
        description="自定义 HTTP 方法、路径、Header JSON 和 Body JSON，支持 {api_key}/{model}/{message} 等占位符。",
        custom_headers_json='{"Authorization": "Bearer {api_key}", "Content-Type": "application/json"}',
        custom_body_json='{"model": "{model}", "messages": [{"role": "user", "content": "{message}"}]}',
    ),
)


def provider_presets_as_dicts() -> list[dict[str, str]]:
    return [preset.to_dict() for preset in PROVIDER_PRESETS]
