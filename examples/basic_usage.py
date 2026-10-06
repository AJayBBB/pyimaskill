from pyimaskill import ImaClient


with ImaClient() as client:
    results = client.notes.search(query="Python", start=0, end=20)
    for note in results.search_note_infos:
        print(f"- {note.note_book_info.title}")

    note_id = client.notes.import_doc(
        content="# My Note\n\nThis is a markdown note.",
    )
    print(f"Created note: {note_id}")

    content = client.notes.get_content(note_id)
    print(content)

    kb_list = client.knowledge.search_knowledge_base(query="")
    for kb in kb_list.info_list:
        print(f"KB: {kb.name} ({kb.id})")

    if kb_list.info_list:
        kb_id = kb_list.info_list[0].id
        items = client.knowledge.get_knowledge_list(
            knowledge_base_id=kb_id,
            limit=20,
        )
        for item in items.knowledge_list:
            print(f"  - {item.title}")

    if kb_list.info_list:
        kb_id = kb_list.info_list[0].id
        client.knowledge.import_urls(
            knowledge_base_id=kb_id,
            urls=["https://example.com/article"],
        )
