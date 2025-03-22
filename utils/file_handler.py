import requests
from io import BytesIO
from openai import OpenAI

def create_file(client: OpenAI, file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        # Download the file content from the URL
        response = requests.get(file_path)
        file_content = BytesIO(response.content)
        file_name = file_path.split("/")[-1]
        file_tuple = (file_name, file_content)
        result = client.files.create(
            file=file_tuple,
            purpose="assistants"
        )
    else:
        # Handle local file path
        with open(file_path, "rb") as file_content:
            result = client.files.create(
                file=file_content,
                purpose="assistants"
            )
    return result.id

def add_to_vector_store(client: OpenAI,vector_store ,file_path):
    file_id = create_file(client, file_path)
    client.vector_stores.files.create(
        vector_store_id=vector_store.id,
        file_id=file_id
    )
    result = client.vector_stores.files.list(vector_store_id=vector_store.id)
    print(result)
    return result