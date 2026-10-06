# IMA OpenAPI Python Client

## Configuration

### Credentials

Initialize `ImaClient` with required `client_id` and `api_key`:

```python
from pyimaskill import ImaClient

client = ImaClient(
    client_id="your-client-id",
    api_key="your-api-key",
    api_key_expires_at="2026-05-06T08:00:00+08:00",
    base_url="https://ima.qq.com",
    timeout=30.0,
)
```

## Notes API

### Search Notes

```python
result = client.notes.search(
    query="Python",
    search_type=SearchType.TITLE,
    sort_type=SortType.MODIFY_TIME,
    start=0,
    end=20,
)
for note in result.search_note_infos:
    print(note.note_book_info.title)
```

### List Folders

```python
result = client.notes.list_folders(cursor="0", limit=20)
for folder in result.note_folder_infos:
    print(folder.name)
```

### List Notes in Folder

```python
result = client.notes.list_notes(
    folder_id="folder_123",
    sort_type=SortType.MODIFY_TIME,
    cursor="",
    limit=20,
)
for note in result.note_book_list:
    print(note.title)
```

### Create Note

```python
note_id = client.notes.import_doc(
    content="# Title\n\nMarkdown content here.",
    folder_id="folder_123",
)
```

### Append to Note

```python
note_id = client.notes.append_doc(
    note_id="note_123",
    content="\n\nAdditional content.",
)
```

### Get Note Content

```python
content = client.notes.get_content(note_id="note_123")
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
    folder_id="folder_456",
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
    folder_id="folder_456",
)
for r in result.results:
    print(f"{r.name}: {'repeated' if r.is_repeated else 'available'}")
```

### Import URLs

```python
result = client.knowledge.import_urls(
    knowledge_base_id="kb_123",
    urls=["https://example.com/article"],
    folder_id="folder_456",
)
for url, data in result.results.items():
    print(f"{url}: media_id={data.media_id}, ret_code={data.ret_code}")
```

### Get Media Info

```python
result = client.knowledge.get_media_info(media_id="media_123")
if result.url_info:
    print(f"URL: {result.url_info.url}")
elif result.notebook_ext_info:
    print(f"Notebook ID: {result.notebook_ext_info.notebook_id}")
```

### Upload File

```python
result = client.knowledge.upload_file(
    file_path="/path/to/document.pdf",
    knowledge_base_id="kb_123",
    folder_id="folder_456",
    title="My Document",
)
print(f"Uploaded: {result.media_id}")
```

## Enums

| Enum | Values |
|------|--------|
| `SearchType` | `TITLE = 0`, `CONTENT = 1` |
| `SortType` | `MODIFY_TIME = 0`, `CREATE_TIME = 1`, `TITLE = 2`, `SIZE = 3` |
| `ContentFormat` | `PLAINTEXT = 0`, `MARKDOWN = 1`, `JSON = 2` |
| `FolderType` | `USER_CREATE = 0`, `TOTAL = 1`, `UN_CATEGORIZED = 2` |
| `MediaType` | `PDF = 1`, `WEBPAGE = 2`, `WORD = 3`, `PPT = 4`, `EXCEL = 5`, `WECHAT = 6`, `MARKDOWN = 7`, `IMAGE = 9`, `NOTE = 11`, `AI_SESSION = 12`, `TXT = 13`, `XMIND = 14`, `AUDIO = 15`, `VIDEO = 16` |

## Pagination

```python
from pyimaskill.utils.pagination import paginate

for result in paginate(
    client.notes.list_folders,
    cursor_key="cursor",
    limit=20,
):
    for folder in result.note_folder_infos:
        print(folder.name)
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
    print(f"Auth failed: {e.msg}")
except ImaNotFoundError as e:
    print(f"Not found: {e.msg}")
except ImaRateLimitError as e:
    print(f"Rate limited: {e.msg}")
except ImaError as e:
    print(f"API error [{e.code}]: {e.msg}")
```
