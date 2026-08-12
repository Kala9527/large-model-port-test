from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.error_analysis import mask_api_key
from app.providers import provider_presets_as_dicts
from app.tester import CALL_METHODS, test_model_endpoint


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Large Model Port Test Tool")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


def template_context(request: Request, **kwargs):
    return {
        "request": request,
        "call_methods": CALL_METHODS,
        "provider_presets": provider_presets_as_dicts(),
        "result": None,
        "form": {
            "provider_id": "custom",
            "base_url": "",
            "api_key_preview": "",
            "model_id": "",
            "call_mode": "auto",
            "timeout_seconds": 30,
            "temperature": 0.0,
            "api_version": "",
            "custom_http_method": "POST",
            "custom_endpoint_path": "",
            "custom_headers_json": "",
            "custom_body_json": "",
        },
        **kwargs,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", template_context(request))


@app.post("/test", response_class=HTMLResponse)
async def test_endpoint(
    request: Request,
    provider_id: str = Form("custom"),
    base_url: str = Form(...),
    api_key: str = Form(""),
    model_id: str = Form(...),
    call_mode: str = Form("auto"),
    timeout_seconds: float = Form(30),
    temperature: float = Form(0.0),
    api_version: str = Form(""),
    custom_http_method: str = Form("POST"),
    custom_endpoint_path: str = Form(""),
    custom_headers_json: str = Form(""),
    custom_body_json: str = Form(""),
):
    form = {
        "provider_id": provider_id,
        "base_url": base_url,
        "api_key_preview": mask_api_key(api_key),
        "model_id": model_id,
        "call_mode": call_mode,
        "timeout_seconds": timeout_seconds,
        "temperature": temperature,
        "api_version": api_version,
        "custom_http_method": custom_http_method,
        "custom_endpoint_path": custom_endpoint_path,
        "custom_headers_json": custom_headers_json,
        "custom_body_json": custom_body_json,
    }

    try:
        result = await test_model_endpoint(
            base_url=base_url,
            api_key=api_key,
            model_id=model_id,
            call_mode=call_mode,
            timeout_seconds=timeout_seconds,
            temperature=temperature,
            api_version=api_version,
            custom_http_method=custom_http_method,
            custom_endpoint_path=custom_endpoint_path,
            custom_headers_json=custom_headers_json,
            custom_body_json=custom_body_json,
        )
    except ValueError as exc:
        result = {
            "success": False,
            "message": "输入校验失败",
            "successful_method": "",
            "status_code": None,
            "request_url": base_url,
            "raw_response": "",
            "answer": "",
            "analysis": [str(exc)],
            "attempts": [],
        }

    return templates.TemplateResponse(
        "index.html",
        template_context(request, result=result, form=form),
    )


@app.get("/health")
async def health():
    return {"status": "ok"}
