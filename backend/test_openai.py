from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        api_key = api_key.strip()
    client = OpenAI(api_key=api_key)
    resp = client.embeddings.create(input=["Test"], model="text-embedding-3-small")
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()
