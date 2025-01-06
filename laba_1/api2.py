import requests

class Api2:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = 'https://ai-content-detector6.p.rapidapi.com/v1/ai-detector'

    def detect(self, text):
        headers = {
			"x-rapidapi-key": self.api_key,
			"x-rapidapi-host": "ai-content-detector6.p.rapidapi.com",
			"Content-Type": "application/json"
		}
        payload = {'text': text}
        response = requests.post(self.api_url, headers=headers, json=payload)
        return response.json()