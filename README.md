# pyimaskill

[![CI](https://github.com/AJayBBB/pyimaskill/actions/workflows/ci.yml/badge.svg)](https://github.com/AJayBBB/pyimaskill/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/pyimaskill.svg)](https://pypi.org/project/pyimaskill/)
[![Python](https://img.shields.io/pypi/pyversions/pyimaskill.svg)](https://pypi.org/project/pyimaskill/)
[![License](https://img.shields.io/pypi/l/pyimaskill.svg)](https://github.com/AJayBBB/pyimaskill/blob/main/LICENSE)

[中文说明](#中文说明) | [English](#english)

## 中文说明

`pyimaskill` 是一个面向 **IMA OpenAPI** 的 Python **同步客户端**，支持个人笔记和知识库的常见操作。无需 `asyncio`，代码简单直接，非常适合 Python 初学者和国内开发者使用。

### 功能

- **笔记**：搜索、列出笔记本、列出笔记、新建、追加、读取
- **知识库**：搜索、浏览、导入网页、上传文件
- **类型安全**：基于 Pydantic 模型自动解析响应
- **同步设计**：基于 `requests.Session`，无需 `async/await`
- **凭证友好提示**：支持 `api_key` 过期时间校验（有效期一个月）

### 安装

```bash
pip install pyimaskill
```

开发环境：

```bash
git clone https://github.com/AJayBBB/pyimaskill.git
cd pyimaskill
pip install -e ".[dev]"
```

### 认证方式

`pyimaskill` 使用 `client_id + api_key` 方式认证，通过 `ImaClient` 初始化时传入：

- `client_id`：从 [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface) 获取
- `api_key`：从 [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface) 获取，**支持一个月有效期**

### 快速开始

```python
from pyimaskill import ImaClient

with ImaClient(client_id="your-client-id", api_key="your-api-key") as client:
    # 搜索笔记
    result = client.notes.search(query="Python", start=0, end=20)
    for note in result.docs:
        print(note.doc.basic_info.title)

    # 新建笔记
    doc_id = client.notes.import_doc(
        content="# 示例笔记\n\n这里是 Markdown 正文。",
    )
    print("created:", doc_id)
```

### 可选参数

```python
client = ImaClient(
    client_id="your-client-id",
    api_key="your-api-key",
    api_key_expires_at="2026-05-06T08:00:00+08:00",  # 可选，用于过期提醒
    base_url="https://ima.qq.com",  # 可选，默认值
    timeout=30.0,  # 可选，默认值
)
```

### 文档

- [详细中文使用说明](docs/使用说明.md)
- [API 文档](docs/api.md)
- [更新日志](CHANGELOG.md)

## English

`pyimaskill` is a **synchronous** Python client for **IMA OpenAPI**. It covers common note and knowledge-base workflows and adds lifecycle hints for `api_key`. No `asyncio` required.

### Features

- Notes: search, list folders, list notes, create, append, read
- Knowledge bases: search, browse, import URLs, upload files
- Typed response models powered by Pydantic
- Sync-first implementation on top of `requests.Session`
- Credential lifecycle checks for `api_key` (one-month validity)

### Install

```bash
pip install pyimaskill
```

For development:

```bash
git clone https://github.com/AJayBBB/pyimaskill.git
cd pyimaskill
pip install -e ".[dev]"
```

### Authentication

`pyimaskill` uses `client_id + api_key` authentication via class initialization:

- `client_id`: Get from [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface)
- `api_key`: Get from [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface), **supports one-month validity**

### Quick Start

```python
from pyimaskill import ImaClient

with ImaClient(client_id="your-client-id", api_key="your-api-key") as client:
    notes = client.notes.search(query="release")
    print(notes.total_hit_num)
```

### Optional Parameters

```python
client = ImaClient(
    client_id="your-client-id",
    api_key="your-api-key",
    api_key_expires_at="2026-05-06T08:00:00+08:00",  # optional, for expiry warnings
    base_url="https://ima.qq.com",  # optional, default
    timeout=30.0,  # optional, default
)
```

### Docs

- [Chinese Usage Guide](docs/使用说明.md)
- [API Reference](docs/api.md)
- [Changelog](CHANGELOG.md)
