from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote, urljoin

import httpx

from .error_analysis import analyze_failure, mask_api_key


TEST_MESSAGE = "Hi"
DEFAULT_ANTHROPIC_VERSION = "2023-06-01"
DEFAULT_AZURE_API_VERSION = "2024-10-21"


@dataclass(frozen=True)
class CallMethod:
    name: str
    label: str
    path: str
    payload_type: str
    auth_type: str
    description: str


CALL_METHODS: tuple[CallMethod, ...] = (
    CallMethod(
        "openai_chat_completions",
        "OpenAI 兼容 Chat Completions",
        "/chat/completions",
        "openai_chat",
        "bearer",
        "POST {base_url}/chat/completions",
    ),
    CallMethod(
        "openai_responses",
        "OpenAI Responses",
        "/responses",
        "openai_responses",
        "bearer",
        "POST {base_url}/responses",
    ),
    CallMethod(
        "anthropic_messages",
        "Anthropic Claude Messages",
        "/v1/messages",
        "anthropic_messages",
        "anthropic",
        "POST {base_url}/v1/messages",
    ),
    CallMethod(
        "azure_openai_chat_completions",
        "Azure OpenAI Chat Completions",
        "",
        "azure_openai_chat",
        "azure_api_key",
        "POST {base_url}/openai/deployments/{deployment}/chat/completions?api-version=...",
    ),
    CallMethod(
        "gemini_generate_content",
        "Google Gemini Native generateContent",
        "",
        "gemini_generate_content",
        "gemini_key_query",
        "POST {base_url}/models/{model}:generateContent?key=...",
    ),
    CallMethod(
        "message_chat",
        "通用 message chat",
        "/chat",
        "message_chat",
        "bearer_optional",
        "POST {base_url}/chat",
    ),
    CallMethod(
        "generate",
        "通用 generate",
        "/generate",
        "generate",
        "bearer_optional",
        "POST {base_url}/generate",
    ),
    CallMethod(
        "ollama_chat",
        "Ollama /api/chat",
        "/api/chat",
        "ollama_chat",
        "bearer_optional",
        "POST {base_url}/api/chat",
    ),
    CallMethod(
        "ollama_generate",
        "Ollama /api/generate",
        "/api/generate",
        "ollama_generate",
        "bearer_optional",
        "POST {base_url}/api/generate",
    ),
    CallMethod(
        "custom_request",
        "完全自定义 JSON 请求",
        "",
        "custom_request",
        "custom",
        "使用自定义 HTTP 方法、路径、Header JSON 和 Body JSON",
    ),
)

CALL_METHOD_MAP = {method.name: method for method in CALL_METHODS}
AUTO_METHOD_NAMES = (
    "openai_chat_completions",
    "openai_responses",
    "message_chat",
    "generate",
    "ollama_chat",
    "ollama_generate",
)


def normalize_base_url(base_url: str) -> str:
    stripped = base_url.strip()
    if not stripped:
        raise ValueError("URL 不能为空")
    if "{" in stripped or "}" in stripped:
        raise ValueError("URL 中仍包含占位符，请先替换 {WorkspaceId}、{resource-name} 等内容")
    if not stripped.startswith(("http://", "https://")):
        raise ValueError("URL 必须以 http:// 或 https:// 开头")
    return stripped.rstrip("/")


def validate_common_inputs(model_id: str, timeout_seconds: float, temperature: float) -> None:
    if not model_id.strip():
        raise ValueError("模型_id 不能为空")
    if "{" in model_id or "}" in model_id:
        raise ValueError("模型_id 中仍包含占位符，请填写真实模型名或部署名")
    if timeout_seconds <= 0:
        raise ValueError("超时时间必须大于 0")
    if not 0 <= temperature <= 2:
        raise ValueError("temperature 必须在 0 到 2 之间")


def append_path(base_url: str, path: str) -> str:
    normalized = normalize_base_url(base_url)
    clean_path = path.lstrip("/")
    if not clean_path:
        return normalized
    if normalized.endswith(f"/{clean_path}") or normalized.endswith(clean_path):
        return normalized
    return urljoin(f"{normalized}/", clean_path)


def render_placeholders(
    value: str,
    *,
    base_url: str,
    api_key: str,
    model_id: str,
    temperature: float,
    api_version: str,
) -> str:
    replacements = {
        "{base_url}": base_url.strip(),
        "{api_key}": api_key.strip(),
        "{model}": model_id.strip(),
        "{model_id}": model_id.strip(),
        "{deployment}": model_id.strip(),
        "{deployment_name}": model_id.strip(),
        "{message}": TEST_MESSAGE,
        "{temperature}": str(temperature),
        "{api_version}": api_version.strip(),
    }
    rendered = value
    for key, replacement in replacements.items():
        rendered = rendered.replace(key, replacement)
    return rendered


def build_request_url(
    base_url: str,
    method: CallMethod,
    model_id: str,
    api_key: str,
    api_version: str,
    temperature: float,
    custom_endpoint_path: str,
) -> str:
    normalized = normalize_base_url(base_url)

    if method.payload_type == "azure_openai_chat":
        version = api_version.strip() or DEFAULT_AZURE_API_VERSION
        deployment = quote(model_id.strip(), safe="")
        return (
            f"{normalized}/openai/deployments/{deployment}/chat/completions"
            f"?api-version={quote(version, safe='')}"
        )

    if method.name == "azure_openai_chat_completions":
        version = api_version.strip() or DEFAULT_AZURE_API_VERSION
        deployment = quote(model_id.strip(), safe="")
        return (
            f"{normalized}/openai/deployments/{deployment}/chat/completions"
            f"?api-version={quote(version, safe='')}"
        )

    if method.name == "gemini_generate_content":
        model = quote(model_id.strip(), safe="")
        key = quote(api_key.strip(), safe="")
        return f"{normalized}/models/{model}:generateContent?key={key}"

    if method.name == "custom_request":
        path = render_placeholders(
            custom_endpoint_path.strip(),
            base_url=base_url,
            api_key=api_key,
            model_id=model_id,
            temperature=temperature,
            api_version=api_version,
        )
        if not path:
            return normalized
        if path.startswith(("http://", "https://")):
            return path
        return append_path(normalized, path)

    return append_path(normalized, method.path)


def build_payload(method: CallMethod, model_id: str, temperature: float) -> dict[str, Any]:
    if method.payload_type == "openai_chat":
        return {
            "model": model_id,
            "messages": [{"role": "user", "content": TEST_MESSAGE}],
            "temperature": temperature,
        }

    if method.payload_type == "openai_responses":
        return {
            "model": model_id,
            "input": TEST_MESSAGE,
            "temperature": temperature,
        }

    if method.payload_type == "anthropic_messages":
        return {
            "model": model_id,
            "max_tokens": 512,
            "messages": [{"role": "user", "content": TEST_MESSAGE}],
            "temperature": temperature,
        }

    if method.payload_type == "azure_openai_chat":
        return {
            "messages": [{"role": "user", "content": TEST_MESSAGE}],
            "temperature": temperature,
        }

    if method.payload_type == "gemini_generate_content":
        return {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": TEST_MESSAGE}],
                }
            ],
            "generationConfig": {"temperature": temperature},
        }

    if method.payload_type == "message_chat":
        return {
            "model": model_id,
            "message": TEST_MESSAGE,
            "messages": [{"role": "user", "content": TEST_MESSAGE}],
            "temperature": temperature,
        }

    if method.payload_type == "ollama_chat":
        return {
            "model": model_id,
            "messages": [{"role": "user", "content": TEST_MESSAGE}],
            "stream": False,
            "options": {"temperature": temperature},
        }

    if method.payload_type == "ollama_generate":
        return {
            "model": model_id,
            "prompt": TEST_MESSAGE,
            "stream": False,
            "options": {"temperature": temperature},
        }

    return {
        "model": model_id,
        "prompt": TEST_MESSAGE,
        "temperature": temperature,
    }


def parse_json_template(
    value: str,
    *,
    field_name: str,
    base_url: str,
    api_key: str,
    model_id: str,
    temperature: float,
    api_version: str,
    fallback: Any,
) -> Any:
    stripped = value.strip()
    source = stripped or json.dumps(fallback, ensure_ascii=False)
    rendered = render_placeholders(
        source,
        base_url=base_url,
        api_key=api_key,
        model_id=model_id,
        temperature=temperature,
        api_version=api_version,
    )
    try:
        return json.loads(rendered)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{field_name} 不是合法 JSON：{exc}") from exc


def build_headers(
    method: CallMethod,
    api_key: str,
    api_version: str,
    custom_headers: dict[str, Any] | None = None,
) -> dict[str, str]:
    if method.auth_type == "custom":
        headers = custom_headers or {}
        return {str(key): str(value) for key, value in headers.items()}

    headers: dict[str, str] = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    stripped_key = api_key.strip()
    if method.auth_type == "bearer" and stripped_key:
        headers["Authorization"] = f"Bearer {stripped_key}"
    elif method.auth_type == "bearer_optional" and stripped_key:
        headers["Authorization"] = f"Bearer {stripped_key}"
    elif method.auth_type == "anthropic":
        if stripped_key:
            headers["x-api-key"] = stripped_key
        headers["anthropic-version"] = api_version.strip() or DEFAULT_ANTHROPIC_VERSION
    elif method.auth_type == "azure_api_key" and stripped_key:
        headers["api-key"] = stripped_key

    return headers


def parse_response_body(response: httpx.Response) -> tuple[Any, str]:
    text = response.text
    if not text:
        return "", ""

    try:
        parsed = response.json()
        return parsed, json.dumps(parsed, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return text, text


def extract_text_from_parts(parts: Any) -> str:
    if not isinstance(parts, list):
        return ""
    texts: list[str] = []
    for part in parts:
        if isinstance(part, dict):
            value = part.get("text")
            if isinstance(value, str):
                texts.append(value)
    return "\n".join(texts)


def extract_answer(raw: Any) -> str:
    if isinstance(raw, dict):
        try:
            content = raw["choices"][0]["message"]["content"]
            if content is not None:
                return str(content)
        except (KeyError, IndexError, TypeError):
            pass

        for key in ("output_text", "content", "text", "response", "answer", "generated_text", "output"):
            value = raw.get(key)
            if isinstance(value, str):
                return value

        anthropic_content = extract_text_from_parts(raw.get("content"))
        if anthropic_content:
            return anthropic_content

        try:
            gemini_parts = raw["candidates"][0]["content"]["parts"]
            gemini_text = extract_text_from_parts(gemini_parts)
            if gemini_text:
                return gemini_text
        except (KeyError, IndexError, TypeError):
            pass

        message = raw.get("message")
        if isinstance(message, dict) and isinstance(message.get("content"), str):
            return message["content"]

        choices = raw.get("choices")
        if isinstance(choices, list) and choices:
            first = choices[0]
            if isinstance(first, dict):
                for key in ("text", "content"):
                    value = first.get(key)
                    if isinstance(value, str):
                        return value

        output = raw.get("output")
        if isinstance(output, list):
            texts: list[str] = []
            for item in output:
                if isinstance(item, dict):
                    text = extract_text_from_parts(item.get("content"))
                    if text:
                        texts.append(text)
            if texts:
                return "\n".join(texts)

        data = raw.get("data")
        if isinstance(data, dict):
            for key in ("content", "text", "response", "answer"):
                value = data.get(key)
                if isinstance(value, str):
                    return value

    if isinstance(raw, str):
        return raw

    return ""


def mask_secret_in_text(value: str, api_key: str) -> str:
    stripped_key = api_key.strip()
    if not stripped_key:
        return value
    return value.replace(stripped_key, mask_api_key(stripped_key))


def sanitize_for_display(value: Any, api_key: str) -> Any:
    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        for key, item in value.items():
            lowered = str(key).lower()
            if any(token in lowered for token in ("authorization", "api-key", "x-api-key", "apikey", "key", "token")):
                sanitized[key] = mask_secret_in_text(str(item), api_key)
            else:
                sanitized[key] = sanitize_for_display(item, api_key)
        return sanitized

    if isinstance(value, list):
        return [sanitize_for_display(item, api_key) for item in value]

    if isinstance(value, str):
        return mask_secret_in_text(value, api_key)

    return value


def prepare_request(
    *,
    base_url: str,
    api_key: str,
    model_id: str,
    method: CallMethod,
    temperature: float,
    api_version: str,
    custom_http_method: str,
    custom_endpoint_path: str,
    custom_headers_json: str,
    custom_body_json: str,
) -> dict[str, Any]:
    request_url = build_request_url(
        base_url=base_url,
        method=method,
        model_id=model_id,
        api_key=api_key,
        api_version=api_version,
        temperature=temperature,
        custom_endpoint_path=custom_endpoint_path,
    )

    if method.name == "custom_request":
        fallback_headers = {"Authorization": "Bearer {api_key}", "Content-Type": "application/json"}
        fallback_body = {
            "model": "{model}",
            "messages": [{"role": "user", "content": "{message}"}],
            "temperature": temperature,
        }
        custom_headers = parse_json_template(
            custom_headers_json,
            field_name="自定义请求头",
            base_url=base_url,
            api_key=api_key,
            model_id=model_id,
            temperature=temperature,
            api_version=api_version,
            fallback=fallback_headers,
        )
        if not isinstance(custom_headers, dict):
            raise ValueError("自定义请求头必须是 JSON object")
        payload = parse_json_template(
            custom_body_json,
            field_name="自定义请求体",
            base_url=base_url,
            api_key=api_key,
            model_id=model_id,
            temperature=temperature,
            api_version=api_version,
            fallback=fallback_body,
        )
        headers = build_headers(method, api_key, api_version, custom_headers)
        return {
            "http_method": custom_http_method.strip().upper() or "POST",
            "request_url": request_url,
            "headers": headers,
            "payload": payload,
        }

    return {
        "http_method": "POST",
        "request_url": request_url,
        "headers": build_headers(method, api_key, api_version),
        "payload": build_payload(method, model_id, temperature),
    }


async def call_once(
    *,
    client: httpx.AsyncClient,
    base_url: str,
    api_key: str,
    model_id: str,
    method: CallMethod,
    temperature: float,
    api_version: str,
    custom_http_method: str,
    custom_endpoint_path: str,
    custom_headers_json: str,
    custom_body_json: str,
) -> dict[str, Any]:
    prepared = prepare_request(
        base_url=base_url,
        api_key=api_key,
        model_id=model_id,
        method=method,
        temperature=temperature,
        api_version=api_version,
        custom_http_method=custom_http_method,
        custom_endpoint_path=custom_endpoint_path,
        custom_headers_json=custom_headers_json,
        custom_body_json=custom_body_json,
    )
    request_url = prepared["request_url"]
    http_method = prepared["http_method"]
    headers = prepared["headers"]
    payload = prepared["payload"]

    try:
        response = await client.request(
            http_method,
            request_url,
            headers=headers,
            json=payload if http_method not in {"GET", "DELETE"} else None,
        )
        raw_body, display_body = parse_response_body(response)
        answer = extract_answer(raw_body)
        success = 200 <= response.status_code < 300

        result: dict[str, Any] = {
            "success": success,
            "method": method.name,
            "method_label": method.label,
            "http_method": http_method,
            "request_url": mask_secret_in_text(request_url, api_key),
            "status_code": response.status_code,
            "raw_response": mask_secret_in_text(display_body, api_key),
            "answer": mask_secret_in_text(answer, api_key),
            "request_headers": sanitize_for_display(headers, api_key),
            "request_payload": sanitize_for_display(payload, api_key),
        }

        if not success:
            result["error"] = mask_secret_in_text(
                f"HTTP {response.status_code} {response.reason_phrase or 'Error'}",
                api_key,
            )
            result["analysis"] = analyze_failure(
                status_code=response.status_code,
                exception_type=None,
                error_text=result["error"],
                response_body=raw_body,
            )

        return result
    except Exception as exc:  # noqa: BLE001 - all transport failures should be reported.
        exception_type = type(exc).__name__
        return {
            "success": False,
            "method": method.name,
            "method_label": method.label,
            "http_method": http_method,
            "request_url": mask_secret_in_text(request_url, api_key),
            "status_code": None,
            "raw_response": "",
            "answer": "",
            "error": mask_secret_in_text(str(exc), api_key),
            "exception_type": exception_type,
            "request_headers": sanitize_for_display(headers, api_key),
            "request_payload": sanitize_for_display(payload, api_key),
            "analysis": analyze_failure(
                status_code=None,
                exception_type=exception_type,
                error_text=str(exc),
                response_body=None,
            ),
        }


async def test_model_endpoint(
    *,
    base_url: str,
    api_key: str,
    model_id: str,
    call_mode: str,
    timeout_seconds: float,
    temperature: float = 0.0,
    api_version: str = "",
    custom_http_method: str = "POST",
    custom_endpoint_path: str = "",
    custom_headers_json: str = "",
    custom_body_json: str = "",
) -> dict[str, Any]:
    validate_common_inputs(model_id, timeout_seconds, temperature)

    if call_mode == "auto":
        selected_methods = [CALL_METHOD_MAP[name] for name in AUTO_METHOD_NAMES]
    else:
        selected = CALL_METHOD_MAP.get(call_mode)
        if not selected:
            raise ValueError("调用方式不受支持")
        selected_methods = [selected]

    attempts: list[dict[str, Any]] = []
    async with httpx.AsyncClient(timeout=httpx.Timeout(timeout_seconds)) as client:
        for method in selected_methods:
            attempt = await call_once(
                client=client,
                base_url=base_url,
                api_key=api_key,
                model_id=model_id.strip(),
                method=method,
                temperature=temperature,
                api_version=api_version,
                custom_http_method=custom_http_method,
                custom_endpoint_path=custom_endpoint_path,
                custom_headers_json=custom_headers_json,
                custom_body_json=custom_body_json,
            )
            attempts.append(attempt)
            if attempt["success"]:
                return {
                    "success": True,
                    "message": "调用成功",
                    "successful_method": attempt["method_label"],
                    "status_code": attempt["status_code"],
                    "request_url": attempt["request_url"],
                    "raw_response": attempt["raw_response"],
                    "answer": attempt["answer"],
                    "attempts": attempts,
                }

    merged_hints: list[str] = []
    for attempt in attempts:
        merged_hints.extend(attempt.get("analysis", []))

    return {
        "success": False,
        "message": "全部调用方式测试失败",
        "successful_method": "",
        "status_code": attempts[-1].get("status_code") if attempts else None,
        "request_url": attempts[-1].get("request_url") if attempts else "",
        "raw_response": attempts[-1].get("raw_response") if attempts else "",
        "answer": "",
        "attempts": attempts,
        "analysis": list(dict.fromkeys(merged_hints)),
    }
