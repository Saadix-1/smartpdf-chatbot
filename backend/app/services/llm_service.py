from openai import OpenAI
from ..core.config import settings

def query_ollama(prompt: str) -> str:
    # Kept function name 'query_ollama' to avoid refactoring endpoints.py right now, but changed internals
    try:
        if not settings.OPENAI_API_KEY:
            return "Error: OPENAI_API_KEY is not set."
            
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant answering queries based on the provided document context."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] OpenAI call failed: {str(e)}")
        return "Sorry, an error occurred while generating the response from OpenAI."
