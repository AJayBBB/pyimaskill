# pyimaskill

[![PyPI](https://img.shields.io/pypi/v/pyimaskill.svg)](https://pypi.org/project/pyimaskill/)
[![Python](https://img.shields.io/pypi/pyversions/pyimaskill.svg)](https://pypi.org/project/pyimaskill/)
[![License](https://img.shields.io/pypi/l/pyimaskill.svg)](https://github.com/AJayBBB/pyimaskill/blob/main/LICENSE)

`pyimaskill` 是一个面向 **IMA OpenAPI** 的 Python **同步客户端**，支持个人笔记和知识库的常见操作。

## 功能特性

- **笔记管理**：搜索、列出笔记本、列出笔记、新建、追加、读取
- **知识库管理**：搜索、浏览、导入网页、上传文件
- **类型安全**：基于 Pydantic 模型自动解析响应
- **同步设计**：基于 `requests.Session`，无需 `async/await`
- **凭证友好提示**：支持 `api_key` 过期时间校验（有效期一个月）

## 安装

```bash
pip install pyimaskill
```

开发环境：

```bash
git clone https://github.com/AJayBBB/pyimaskill.git
cd pyimaskill
pip install -e ".[dev]"
```

## 快速开始

### 1. 获取凭证

前往 [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface) 获取：

- `client_id`：客户端 ID
- `api_key`：API 密钥（**支持一个月有效期**）

### 2. 初始化客户端

```python
from pyimaskill import ImaClient

client = ImaClient(
    client_id="your-client-id",
    api_key="your-api-key",
)
```

### 3. 笔记操作示例

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
    print("创建成功:", doc_id)
```

### 4. 知识库操作示例

```python
from pyimaskill import ImaClient

client = ImaClient(client_id="your-client-id", api_key="your-api-key")

# 获取知识库列表
kb_result = client.knowledge.search_knowledge_base(query="", cursor="", limit=20)

if not kb_result.info_list:
    print("您还没有创建任何知识库，请先创建知识库后再试。")
else:
    print(f"找到 {len(kb_result.info_list)} 个知识库：")
    for idx, kb in enumerate(kb_result.info_list, 1):
        print(f"  {idx}. {kb.name} (ID: {kb.id})")

# 导入微信公众号文章到知识库
kb_id = "your-knowledge-base-id"
article_url = "https://mp.weixin.qq.com/s/xxxxx"

import_result = client.knowledge.import_urls(
    knowledge_base_id=kb_id,
    urls=[article_url],
)

url_result = import_result.results.get(article_url)
if url_result and url_result.ret_code == 0:
    print(f"添加成功！媒体ID: {url_result.media_id}")
else:
    print(f"添加失败: {url_result.errmsg if url_result else '未知错误'}")
```

## 可选参数

```python
client = ImaClient(
    client_id="your-client-id",
    api_key="your-api-key",
    api_key_expires_at="2026-05-06T08:00:00+08:00",  # 可选，用于过期提醒
    base_url="https://ima.qq.com",  # 可选，默认值
    timeout=30.0,  # 可选，默认值
)
```

## 文档

- [详细中文使用说明](docs/使用说明.md)
- [API 文档](docs/api.md)
- [更新日志](CHANGELOG.md)

## 许可证

MIT License
