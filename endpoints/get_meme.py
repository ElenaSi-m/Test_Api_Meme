import requests
import allure
import pytest
from endpoints.endpoint import Endpoint
from endpoints.meme_user import MemeUser


@pytest.mark.usefixtures("cleanup")
class GetMeme(Endpoint):

    allure.step('Get meme by id')
    def get_meme_by_id(self, meme_req_id, headers=None, token=None):
        headers = headers if headers else self.headers
        if token:
            headers['Authorization'] = f"{token}"
        elif 'Authorization' in headers:
            del headers['Authorization']

        self.response = requests.get(
            f'{self.url}/meme/{meme_req_id}',
             headers=headers
        )

        if self.response.status_code == 200 and "application/json" in self.response.headers.get('Content-Type', ''):
            self.json = self.response.json()
            return self.json
        elif self.response.status_code == 404:
            print(f"Meme with ID {meme_req_id} not found.")
            return None
