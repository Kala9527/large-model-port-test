# 中文说明

> 大模型 API 连通性测试 Web 工具，支持 OpenAI 兼容、Responses、Anthropic、Gemini、Azure OpenAI、Ollama 与自定义 JSON。

这个仓库已经改成 **英文优先、中文在后** 的双语 README，方便 GitHub 全球用户第一眼理解项目，同时保留中文开发者阅读体验。

## 为什么值得 Star / Fork

- 目标场景清晰，不是空壳项目。
- 项目规模适合学习、二次开发和快速改造。
- README、路线图、贡献入口和部署说明更完整。
- topics 会尽量贴近当前 GitHub 热门方向，例如 AI、LLM、OpenAI-compatible、TypeScript、developer-tools、automation、local-first、gamedev 等。

## 功能亮点

- Browser-based real request tester
- Auto-detect mode across common LLM protocols
- Provider presets for popular model gateways
- Custom HTTP method, headers, path, and body JSON
- Masked API key display and detailed error analysis

## 快速开始

`ash
python -m venv .venv`n.venv\\Scripts\\activate`npip install -r requirements.txt`npython -m uvicorn main:app --host 0.0.0.0 --port 5181
`

## 部署与安全

- 不要提交 .env、API Key、生成媒体、大型文件、数据库、日志和构建产物。
- 前端项目可以部署 dist/ 到 GitHub Pages、Vercel、Netlify 或 Nginx。
- 桌面/移动端项目建议只发布干净环境构建出来的 release 文件。

## 后续计划

- [ ] Shareable test profiles
- [ ] Batch endpoint health checks
- [ ] Latency charts and exportable reports
- [ ] More provider presets from the community

