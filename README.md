# Large Model Port Test

[中文说明](./README_CN.md)

> Web tool for testing LLM API connectivity across OpenAI-compatible, Responses, Anthropic, Gemini, Azure OpenAI, Ollama, and custom JSON protocols.  

This repository is packaged to be easy to **star, fork, run, remix, and contribute to**. It keeps the first screen English-first for global GitHub discovery, while preserving a Chinese guide below.

## Why Star This

- Practical project idea with a clear real-world use case.
- Small enough to fork, study, and customize quickly.
- English-first bilingual README for both global and Chinese-speaking developers.
- Clean setup instructions, project structure, roadmap, and contribution entry points.
- Built around popular GitHub themes such as AI tools, TypeScript, developer tools, local-first apps, automation, and indie-friendly workflows when relevant.

## What It Does

Web tool for testing LLM API connectivity across OpenAI-compatible, Responses, Anthropic, Gemini, Azure OpenAI, Ollama, and custom JSON protocols.

## Highlights

- Browser-based real request tester
- Auto-detect mode across common LLM protocols
- Provider presets for popular model gateways
- Custom HTTP method, headers, path, and body JSON
- Masked API key display and detailed error analysis

## Tech Stack

`	ext
Python, FastAPI, Uvicorn, Jinja2, httpx
`

## Quick Start

`ash
python -m venv .venv`n.venv\\Scripts\\activate`npip install -r requirements.txt`npython -m uvicorn main:app --host 0.0.0.0 --port 5181
`

## Project Structure

`	ext
.
|-- src/ or app/          Main source code
|-- public/ or assets/    Static assets when available
|-- docs/                 Notes, specs, or deployment docs when available
|-- README.md             English-first bilingual project guide
-- package / project files
`

## Deployment / Packaging

- Do not commit generated builds, local databases, API keys, private logs, or large media files.
- For frontend projects, deploy the production dist/ folder to GitHub Pages, Vercel, Netlify, Nginx, or package it with DistDesktopLauncher.
- For desktop/mobile projects, publish only release artifacts from a clean build environment.
- Keep configuration examples public and real credentials private.

## Roadmap

- [ ] Shareable test profiles
- [ ] Batch endpoint health checks
- [ ] Latency charts and exportable reports
- [ ] More provider presets from the community

## Contributing

Issues and pull requests are welcome. Useful contributions include better screenshots, demos, docs, templates, presets, provider guides, compatibility fixes, tests, and translations.

If this project helps you, a star and fork make it easier for more people to discover it.


