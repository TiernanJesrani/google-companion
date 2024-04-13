"""
Abstract wrapper for the Gemini API.

Features:
- Prompting and request generation
- Structured output handling
- Memory for conversational context
- Retries on rate limiting

To-Do:
- Function calling
"""

from dotenv import load_dotenv
import os
import json
import requests 
from pydantic import BaseModel
import time

def prettify(string: str) -> str:
    # turn a camel case string into a human readable string
    return ' '.join([word.capitalize() for word in string.split('_')])

def memory_to_string(memory: list[dict]) -> str:
    return "\n\n".join([f"{prettify(k), v}" for item in memory for k, v in item.items()])

def get_response(query: str, api_key: str, model: str = "gemini-1.5-pro-latest") -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {"parts": [{"text": query}]}
        ],
        "generationConfig": {"response_mime_type": "application/json"}
    }
    params = {'key': api_key}

    response = requests.post(url, headers=headers, json=payload, params=params)

    if response.status_code == 429:
        # wait and retry
        print("Rate limited. Waiting 5 seconds and retrying.")
        time.sleep(5)
        return get_response(query, api_key, model)
    
    if response.status_code != 200:
        raise Exception(f"Failed to get response: {response.text}")
    
    
    return response.json()

"""
Abstract class for Gemini API
Can be inherited to add memory

Use the structure parameter to define the schema of the response
If structure is provided for a response, the response structure will override the constructor structure param
"""
class GeminiClient:
    def __init__(self, 
                 model: str = "gemini-1.5-pro-latest", 
                 api_key: str=None, 
                 structure: BaseModel = None, 
                 debug: bool=False,
                 system_message: str=None,
                 verbose: bool=False):
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.model = model
        self.api_key = api_key or GEMINI_API_KEY
        self.structure = structure
        self.debug = debug
        self.system_message = system_message
        self.verbose = verbose

    def __call__(self, prompt: str, structure: BaseModel | None = None, 
                 context: str | None = None) -> dict | BaseModel:
        prompt = f"""
            {self.system_message if self.system_message else ""}
            Respond to the provided prompt. Your output should be a JSON object that matches the provided schema.
            Prompt: {prompt}
            Schema: {structure.model_json_schema() if structure else self.structure.model_json_schema()}

            {"Context: " + context if context else ""}
        """ if self.structure or structure else prompt

        response = get_response(prompt, self.api_key, self.model)

        if self.verbose:
            print("Prompt: ", prompt)
            print("Raw response: ", response)

        if self.debug:
            return response  # Returns the JSON response directly
        else:
            response_text = response['candidates'][0]['content']['parts'][0]['text']
            response_dict = json.loads(response_text)
            if structure:
                return structure(**response_dict)
            if self.structure:
                return self.structure(**response_dict)
            return response_dict
        
# Inherited class with memory
class GeminiClientWithMemory(GeminiClient):
    def __init__(self, model: str = "gemini-1.5-pro-latest", 
                       api_key: str=None, 
                       structure: BaseModel = None, 
                       debug: bool=False, 
                       system_message: str=None,
                       verbose: bool=False):
        super().__init__(model, api_key, structure, debug)
        self.verbose = verbose

        memory = [{"system_message": system_message}] if system_message else []
        if self.structure:
            memory.extend([{"system_message": f"Adhere to this schema with every response: {self.structure.model_json_schema()}"}])
        self.memory = memory

    def __call__(self, prompt: str, structure: BaseModel | None = None, 
                 context: str | None = None) -> dict | BaseModel:
        if structure:
            self.memory.extend([{"system_message": f"For the next message, adhere to the below schema: {structure.model_json_schema()}"}])
        self.memory.extend([{"human_message": prompt}])
        chat_history: str = memory_to_string(self.memory)
        if context:
            chat_history += "Context: " + context + "\n"
        chat_history += "AI Message:"

        response = get_response(chat_history, self.api_key, self.model)

        self.memory.extend([{"AI_Message": response['candidates'][0]['content']['parts'][0]['text']}])

        if self.verbose:
            print(memory_to_string(self.memory))

        if self.debug:
            return response
        else:
            response_text = response['candidates'][0]['content']['parts'][0]['text']
            response_dict = json.loads(response_text)
            if structure:
                return structure(**response_dict)
            if self.structure:
                return self.structure(**response_dict)
            return response_dict

# Example Usage:
if __name__ == "__main__":
    class Currency(BaseModel):
        name: str
        symbol: str
        price: float

    class Currencies(BaseModel):
        currencies: list[Currency]

    ### Without Memory
    client = GeminiClient(structure=Currencies)

    response = client(
        prompt="Generate a list of the top 10 most popular cryptocurrencies.",
    )
    print(response)

    ### With Memory
    client = GeminiClientWithMemory(structure=Currencies, system_message="You are a cryptocurrency chatbot.", verbose=True)

    response = client(
        prompt="What is the current price of Bitcoin?",
    )

    response = client(
        prompt="How far away is that number from 50,000?",
    )

