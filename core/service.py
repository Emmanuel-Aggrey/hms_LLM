import requests
import json
from django.conf import settings


class CoreService:
    def __init__(self) -> None:
        pass

    def generate_response(self, text):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=\
            {settings.LLM_API_KEY}"
        payload = json.dumps({
            "contents": [
                {
                    "parts": [
                        {
                            "text": text
                        }
                    ]
                }
            ]
        })
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response
        except requests.exceptions.RequestException as e:
            raise ValueError(f"LLM API request failed: {e}")
