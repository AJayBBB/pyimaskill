from pyimaskill import ImaClient


with ImaClient() as client:
    kb_list = client.knowledge.search_knowledge_base(query="")
    if not kb_list.info_list:
        print("No knowledge bases found")
        exit(1)

    kb_id = kb_list.info_list[0].id
    print(f"Uploading to: {kb_list.info_list[0].name}")

    result = client.knowledge.upload_file(
        file_path="report.pdf",
        knowledge_base_id=kb_id,
    )
    print(f"Uploaded: {result.media_id}")
