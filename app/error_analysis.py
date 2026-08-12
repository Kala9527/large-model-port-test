from __future__ import annotations

import json
from typing import Any


def mask_api_key(api_key: str | None) -> str:
    """Return a display-safe API key preview."""
    if not api_key:
        return "(empty)"

    stripped = api_key.strip()
    if len(stripped) <= 8:
        return f"{stripped[:2]}***{stripped[-1:]}"

    return f"{stripped[:4]}...{stripped[-4:]}"


def compact_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def analyze_failure(
    *,
    status_code: int | None,
    exception_type: str | None,
    error_text: str,
    response_body: Any | None = None,
) -> list[str]:
    """Convert raw transport/API errors into practical troubleshooting hints."""
    hints: list[str] = []
    body_text = ""

    if isinstance(response_body, (dict, list)):
        body_text = compact_json(response_body).lower()
    elif response_body is not None:
        body_text = str(response_body).lower()

    combined = f"{error_text}\n{body_text}".lower()

    if status_code in (401, 403) or "unauthorized" in combined or "forbidden" in combined:
        hints.append("api_key 可能无效、已过期、权限不足，或目标服务不接受 Bearer Token 鉴权。")

    if status_code == 404 or "model not found" in combined or "not found" in combined:
        hints.append("请求地址或模型_id 可能不存在，请确认 base_url 是否需要包含 /v1，以及模型名称是否在服务端注册。")

    if status_code == 400:
        hints.append("请求体格式可能与目标接口不兼容，或模型_id、messages/prompt 字段不符合服务端要求。")

    if status_code == 422:
        hints.append("目标服务已收到请求但校验失败，常见原因是字段名、消息结构或参数类型不符合该接口格式。")

    if status_code == 429:
        hints.append("触发限流或额度不足，请稍后重试，或检查账号额度、并发限制和服务端限流策略。")

    if status_code is not None and 500 <= status_code <= 599:
        hints.append("目标模型服务返回 5xx，通常是模型后端、网关、推理服务或上游依赖异常。")

    if exception_type:
        lowered = exception_type.lower()
        if "timeout" in lowered:
            hints.append("网络或模型推理超时，请检查服务是否可达、模型是否加载完成，并适当增大超时时间。")
        elif "connect" in lowered:
            hints.append("无法建立连接，请检查 URL、端口、防火墙、代理、服务监听地址和 HTTP/HTTPS 协议。")
        elif "invalidurl" in lowered or "unsupportedprotocol" in lowered:
            hints.append("URL 格式不正确，请使用 http:// 或 https:// 开头的完整地址。")
        elif "ssl" in lowered or "certificate" in combined:
            hints.append("HTTPS 证书校验失败，可能是自签名证书、证书过期或服务地址与证书域名不匹配。")

    if "invalid api key" in combined or "incorrect api key" in combined:
        hints.append("服务端明确提示 API Key 不正确，请重新生成或替换 api_key。")

    if "does not exist" in combined or "unknown model" in combined:
        hints.append("服务端明确提示模型不存在，请检查模型_id 拼写、命名空间和部署名称。")

    if "connection refused" in combined:
        hints.append("端口拒绝连接，说明目标主机可达但该端口没有服务监听或被本机/网关拒绝。")

    if "name resolution" in combined or "nodename" in combined or "getaddrinfo" in combined:
        hints.append("域名解析失败，请检查域名、DNS、内网域名访问环境或代理配置。")

    if "not a valid json" in combined or "jsondecode" in combined:
        hints.append("响应不是合法 JSON，目标可能不是 OpenAI 兼容接口，或返回了 HTML/网关错误页。")

    if not hints:
        hints.append("未能自动识别具体原因，请重点核对 URL、api_key、模型_id、接口路径和服务端日志。")

    return list(dict.fromkeys(hints))
