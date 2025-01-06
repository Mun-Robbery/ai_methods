import requests

class Api1:
    '''
    
    '''
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = 'https://ai-content-detector-ai-gpt.p.rapidapi.com/api/detectText/'

    def detect(self, text: str) -> dict:
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "ai-content-detector-ai-gpt.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        payload = {'text': text}
        response = requests.post(self.api_url, headers=headers, json=payload)
        return response.json()

    
