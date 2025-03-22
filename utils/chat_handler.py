from openai import OpenAI
from utils.file_handler import add_to_vector_store
from dotenv import load_dotenv, set_key
import os

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
    print(response.model_dump())
    result = response.model_dump()["output"]
    for obj in result:
        if "content" in obj:
            return obj["content"][0]["text"]
    return "I'm sorry, I don't have an answer for that."

def generate_context_from_files(file_path):
    file_list = add_to_vector_store(client, vector_store, file_path)
    file_ids = [file.id for file in file_list]
    
    return file_ids