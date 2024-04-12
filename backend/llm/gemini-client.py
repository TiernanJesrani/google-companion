from dotenv import load_dotenv
import os
import json
import requests 
from pydantic import BaseModel

class GeminiClient:
    def __init__(self, api_key: str=None, structure: BaseModel = None, debug: bool=False):
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.api_key = api_key or GEMINI_API_KEY
        self.debug = debug
        self.structure = structure

    def __call__(self, prompt: str, schema: str):

        prompt = f"""
            Respond to the provided prompt. Your output should be a JSON object that matches the provided schema.
            Prompt: {prompt}
            Schema: {schema}
        """

        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [
                {"parts": [{"text": prompt}]}
            ],
            "generationConfig": {"response_mime_type": "application/json"}
        }
        params = {'key': self.api_key}

        response = requests.post(url, headers=headers, json=payload, params=params)

        if self.debug:
            return response.json()  # Returns the JSON response directly
        else:
            response_json = response.json()
            response_text = response_json['candidates'][0]['content']['parts'][0]['text']
            response_dict = json.loads(response_text)
            return self.structure(**response_dict) if self.structure else response_dict


# Example Usage:
if __name__ == "__main__":
    class Currency(BaseModel):
        name: str
        symbol: str
        price: float

    class Currencies(BaseModel):
        currencies: list[Currency]
    
    client = GeminiClient(structure=Currencies)

    response = client(
        prompt="Generate a list of the top 10 most popular cryptocurrencies.",
        schema=f"{Currencies.model_json_schema()}",
    )
    print(response)
