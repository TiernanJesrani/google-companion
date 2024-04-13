from dotenv import load_dotenv
import os
import json
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

if __name__ == "__main__":
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    # response = get_response("Hello, world!", GEMINI_API_KEY)
    # print(response)

    texts = ["What is the meaning of life?", "How much wood would a woodchuck chuck?", "How does the brain work?"]
    response = get_response_batch(texts, GEMINI_API_KEY)
    print(response)