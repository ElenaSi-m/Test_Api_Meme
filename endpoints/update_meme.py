import requests
import allure
import pytest
from endpoints.endpoint import Endpoint


@pytest.mark.usefixtures("cleanup")
class UpdateMeme(Endpoint):

    @allure.step('Update meme')
    def update_meme(self, meme_id, payload, token=None, headers=None):
        headers = headers if headers else self.headers
        if token:
            headers['Authorization'] = f"{token}"

        print(f"Sending request to {self.url}/meme/{meme_id}")
        print(f"Authorization Header: {headers.get('Authorization')}")
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")

        self.response = requests.put(
            f'{self.url}/meme/{meme_id}',
            json=payload,
            headers=headers
        )

        print(f"Response status: {self.response.status_code}")
        print(f"Response body: {self.response.text}")
        print(f"Response headers: {self.response.headers}")

        if self.response.status_code in [401, 500]:
            print("Unauthorized! Double-check the token or authorization process.")

        try:
            self.json = self.response.json()
        except requests.exceptions.JSONDecodeError:
            print("Failed to parse JSON response.")
            self.json = None
        return self.response
