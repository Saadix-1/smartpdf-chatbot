import requests

def query_ollama(prompt, model="mistral"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    response.raise_for_status()
    return response.json()["response"]

# Exemple d'utilisation :
if __name__ == "__main__":
    print(query_ollama("Donne-moi un résumé du PDF sur les toric orbifolds."))
