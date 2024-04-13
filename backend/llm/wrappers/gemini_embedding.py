from dotenv import load_dotenv
import os
import numpy as np
import requests 

def get_response(text: str, api_key: str, model: str = "text-embedding-004") -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:embedContent"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "model": f"models/{model}",
        "content": {
            "parts": [{
                "text": text
            }]
        }
    }
    params = {'key': api_key}

    response = requests.post(url, headers=headers, json=payload, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to get response: {response.text}")
    
    return response.json()

def get_response_batch(texts: list[str], api_key: str, model: str = "text-embedding-004") -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:batchEmbedContents"
    headers = {'Content-Type': 'application/json'}
    # Fix the structure of the payload for each text to include the model key
    payload = {
        "requests": [
            {
                "model": f"models/{model}",
                "content": {
                    "parts": [{"text": text}]
                }
            } for text in texts
        ],
    }
    params = {'key': api_key}

    # Send the POST request
    response = requests.post(url, headers=headers, json=payload, params=params)

    # Check the status code and raise an exception if something went wrong
    if response.status_code != 200:
        raise Exception(f"Failed to get response: {response.text}")
    
    # Return the response as a JSON dictionary
    return response.json()

class GeminiEmbeddingClient:
    def __init__(self, 
                 model: str = "text-embedding-004", 
                 api_key: str=None, 
                 debug: bool=False):
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.model = model
        self.api_key = api_key or GEMINI_API_KEY
        self.debug = debug

    def __call__(self, input: str | list[str],  batch: bool = False) -> np.ndarray:
        response = get_response(input, self.api_key, self.model) if not batch else get_response_batch(input, self.api_key, self.model)
        
        print(response)
        if not batch:
            return np.array(response['embedding']['values'])
        else:
            parsed_response = []
            for embedding in response['embeddings']:
                parsed_response.append(embedding['values'])
        return np.array(parsed_response)
    
# Example usage:
if __name__ == "__main__":
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    client = GeminiEmbeddingClient(api_key=GEMINI_API_KEY)
    response = client("Hello, world!")
    print(response)

    texts = ["What is the meaning of life?", "How much wood would a woodchuck chuck?", "How does the brain work?"]
    response = client(texts, batch=True)
    print(response)