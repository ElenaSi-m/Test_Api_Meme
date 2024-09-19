import requests
import allure
import pytest
from endpoints.endpoint import Endpoint


@pytest.mark.usefixtures("cleanup")
class GetAllMeme(Endpoint):
    allure.step('Get all memes')

    def get_all_meme(self, headers=None, token=None):
        headers = headers if headers else self.headers
        if token:
            headers['Authorization'] = f"{token}"
        elif 'Authorization' in headers:
            del headers['Authorization']

        self.response = requests.get(
            f'{self.url}/meme',
            headers=headers
        )

        if self.response.status_code == 200 and "application/json" in self.response.headers.get('Content-Type', ''):
            self.json = self.response.json()
            return self.json
