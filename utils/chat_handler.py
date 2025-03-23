from openai import OpenAI
from utils.file_handler import add_to_vector_store
from dotenv import load_dotenv, set_key
import os
import json

json_history = []

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
vector_store_id = os.getenv("OPENAI_VECTOR_STORE_ID")
if vector_store_id:
    vector_store = client.vector_stores.retrieve(
            vector_store_id=vector_store_id
        )
else:
    vector_store = client.vector_stores.create(
        name="knowledge base"
    )
    set_key(".env", "OPENAI_VECTOR_STORE_ID", vector_store.id)

def upload_vector_store():
        # Get list of files in uploads directory
    upload_files = [f for f in os.listdir('uploads') if os.path.isfile(os.path.join('uploads', f))]
    
    # Get list of files in vector store
    vector_files = client.vector_stores.files.list(vector_store_id=vector_store.id)
    stored_files = [client.files.retrieve(f.id) for f in vector_files.data]
    vector_filenames = [f.filename for f in stored_files]

    print("Files in vector store:", vector_filenames)
    print("Files in uploads folder:", upload_files)

    # Add missing files to vector store
    for filename in upload_files:
        if filename not in vector_filenames:
            file_path = os.path.join('uploads', filename)
            print(f"Adding {filename} to vector store...")
            add_to_vector_store(client, vector_store, file_path)

def ask_chatbot(question, history):
    prompt = ''
    if history:
        for q, a in history.items():
            prompt += f"User: {q}\nAssistant: {a}\n"
    prompt += f"User: {question}"
    response = client.responses.create(
        model="gpt-4o-mini",
        input=question,
        tools=[{
            "type": "file_search",
            "vector_store_ids": [vector_store.id]
        }],
        include=["file_search_call.results"]
    )
    res = response.model_dump()
    json_history.append({"question": question, "response": res})
    with open("history.json", "w") as f:
        f.write(json.dumps(json_history))
    result = res["output"]
    for obj in result:
        if "content" in obj:
            return obj["content"][0]["text"]
    return "I'm sorry, I don't have an answer for that."

def generate_context_from_files(file_path):
    file_list = add_to_vector_store(client, vector_store, file_path)
    file_ids = [file.id for file in file_list]
    
    return file_ids