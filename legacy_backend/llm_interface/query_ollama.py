import requests

def query_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",  # ou llama2, orca-mini, etc.
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        print(f"[ERREUR] Appel à Ollama échoué : {str(e)}")
        return "Désolé, une erreur est survenue lors de la génération."
