# Changelog

## 1.1.3 (2025-04-17)

### Features

- 首个公开发布的同步版本。
- 支持笔记：搜索、列出笔记本、列出笔记、新建、追加、读取正文。
- 支持知识库：搜索知识库、浏览内容、导入网页、上传文件到 COS。
- 基于 `requests.Session` 的同步 HTTP 客户端，无需 asyncio。
- 基于 Pydantic 的类型安全响应模型。
- 支持 `api_key` 过期时间校验与友好提示。
- 自动注入 `ima-openapi-ctx: skill_version=1.1.3` 请求头。

### Notes

- 适配 IMA OpenAPI Skill 规范 v1.1.3。
- 端点已更新为最新版本：`list_notebook`、`list_note` 等。
