import requests
import os




class CustomHttpClient:
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}
        self.timeout = 30

    def get(self, path=None, params=None):
        url = f"{self.base_url}{path}" if path is not None else f"{self.base_url}"
        response = requests.get(
            url, params=params, headers=self.headers, timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def post(self, path=None, data=None, json=None):
        url = f"{self.base_url}{path}" if path is not None else f"{self.base_url}"
        response = requests.post(
            url, data=data, json=json, headers=self.headers, timeout=self.timeout
        )
        response.raise_for_status()
        return response



SMS_LARAVEL_SESSION = os.getenv("SMS_LARAVEL_SESSION")

class SMSClient(CustomHttpClient):
    def __init__(self, base_url):

        headers = {
            "Cookie": f"laravel_session={SMS_LARAVEL_SESSION}"
        }

        super().__init__(base_url, headers)



