# IMA OpenAPI Python Client

## Configuration

### Credentials

Initialize `ImaClient` with required `client_id` and `api_key`:

```python
from pyimaskill import ImaClient

client = ImaClient(
    client_id="your-client-id",  # required
    api_key="your-api-key",      # required
    api_key_expires_at="2026-05-06T08:00:00+08:00",  # optional, for expiry warnings
    base_url="https://ima.qq.com",  # optional, default
    timeout=30.0,  # optional, default
)
```

## Notes API

### Search Notes

```python
result = client.notes.search(
    query="Python",
    search_type=SearchType.TITLE,  # 0=title, 1=content
    sort_type=SortType.MODIFY_TIME,  # 0=modify, 1=create, 2=title, 3=size
    start=0,
    end=20,
)
for doc in result.docs:
    print(doc.doc.basic_info.title)
```

### List Folders

```python
result = client.notes.list_folders(cursor="0", limit=20)
for folder in result.note_book_folders:
    print(folder.folder.basic_info.name)
```

### List Notes in Folder

```python
result = client.notes.list_notes(
    folder_id="folder_123",
    sort_type=SortType.MODIFY_TIME,  # 0=modify_time (default), 1=create_time, 2=title, 3=size
    cursor="",
    limit=20,
)
for note in result.note_book_list:
    print(note.basic_info.title)
```

### Create Note

```python
doc_id = client.notes.import_doc(
    content="# Title\n\nMarkdown content here.",
    folder_id="folder_123",  # optional
)
```

### Append to Note

```python
doc_id = client.notes.append_doc(
    doc_id="doc_123",
    content="\n\nAdditional content.",
)
```

### Get Note Content

```python
content = client.notes.get_content(doc_id="doc_123")
```

## Knowledge API

### Get Knowledge Base Info

```python
result = client.knowledge.get_knowledge_base(ids=["kb_123", "kb_456"])
for kb_id, info in result.infos.items():
    print(f"{kb_id}: {info.name}")
```

### List Knowledge Content

```python
result = client.knowledge.get_knowledge_list(
    knowledge_base_id="kb_123",
    folder_id="folder_456",  # optional
    cursor="",
    limit=20,
)
for item in result.knowledge_list:
    print(item.title)
```

### Search Knowledge

```python
result = client.knowledge.search_knowledge(
    query="Python",
    knowledge_base_id="kb_123",
    cursor="",
)
for item in result.info_list:
    print(f"{item.title} - {item.highlight_content}")
```

### Search Knowledge Bases

```python
result = client.knowledge.search_knowledge_base(
    query="my search",
    cursor="",
    limit=20,
)
for kb in result.info_list:
    print(kb.name)
```

### Get Addable Knowledge Base List

```python
result = client.knowledge.get_addable_knowledge_base_list(
    cursor="",
    limit=20,
)
for kb in result.addable_knowledge_base_list:
    print(kb.name)
```

### Check Repeated Names

```python
result = client.knowledge.check_repeated_names(
    knowledge_base_id="kb_123",
    params=[
        {"name": "report.pdf", "media_type": 1},
    ],
    folder_id="folder_456",  # optional
)
for r in result.results:
    print(f"{r.name}: {'repeated' if r.is_repeated else 'available'}")
```

### Import URLs

```python
result = client.knowledge.import_urls(
    knowledge_base_id="kb_123",
    urls=["https://example.com/article"],
    folder_id="folder_456",  # optional
)
for url, data in result.results.items():
    print(f"{url}: media_id={data.media_id}, ret_code={data.ret_code}")
```

### Upload File

```python
result = client.knowledge.upload_file(
    file_path="/path/to/document.pdf",
    knowledge_base_id="kb_123",
    folder_id="folder_456",  # optional
    title="My Document",  # optional, defaults to filename
)
print(f"Uploaded: {result.media_id}")
```

## Enums

| Enum | Values |
|------|--------|
| `SearchType` | `TITLE = 0`, `CONTENT = 1` |
| `SortType` | `MODIFY_TIME = 0`, `CREATE_TIME = 1`, `TITLE = 2`, `SIZE = 3` |
| `ContentFormat` | `PLAINTEXT = 0`, `MARKDOWN = 1`, `JSON = 2` |
| `FolderType` | `USER_CREATED = 0`, `ALL_NOTES = 1`, `UNCATEGORIZED = 2` |
| `MediaType` | `PDF = 1`, `WEBPAGE = 2`, `WORD = 3`, `PPT = 4`, `EXCEL = 5`, `WECHAT = 6`, `MARKDOWN = 7`, `IMAGE = 9`, `NOTE = 11`, `AI_SESSION = 12`, `TXT = 13`, `XMIND = 14`, `AUDIO = 15`, `VIDEO = 16` |

## Pagination

```python
from pyimaskill.utils.pagination import paginate

for result in paginate(
    client.notes.list_folders,
    cursor_key="cursor",
    limit=20,
):
    for folder in result.note_book_folders:
        print(folder.folder.basic_info.name)
```

## UTF-8 Validation

```python
from pyimaskill.utils.encoding import ensure_utf8, sanitize_text

content = ensure_utf8(user_input)
content = sanitize_text(content)
client.notes.import_doc(content=content)
```

## Error Handling

```python
from pyimaskill.exceptions import (
    ImaError,
    ImaAuthError,
    ImaNotFoundError,
    ImaRateLimitError,
)

try:
    client.notes.search(query="test")
except ImaAuthError as e:
    print(f"Auth failed: {e.errmsg}")
except ImaNotFoundError as e:
    print(f"Not found: {e.errmsg}")
except ImaRateLimitError as e:
    print(f"Rate limited: {e.errmsg}")
except ImaError as e:
    print(f"API error [{e.retcode}]: {e.errmsg}")
```
