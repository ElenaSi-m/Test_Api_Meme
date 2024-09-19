import requests
import allure
import pytest
from endpoints.endpoint import Endpoint


@pytest.mark.usefixtures("cleanup")
class CreateMeme(Endpoint):
    meme_id = None

    @allure.step('Create a new meme')
    def create_new_meme(self, payload, headers=None, token=None, expect_failure=False):
        headers = headers if headers else self.headers
        if token:
            headers['Authorization'] = f"{token}"
        print(f"Headers being sent: {headers}")

        print(f"Sending request to {self.url}/meme")
        print(f"Authorization Header: {headers.get('Authorization')}")
        print(f"Headers: {headers}")
        print(f"Payload: {payload}")
        print(f"Request URL: {self.url}/meme")

        self.response = requests.post(
            f'{self.url}/meme',
            json=payload,
            headers=headers
        )

        print(f"Response status: {self.response.status_code}")
        print(f"Response body: {self.response.text}")
        print(f"Response headers: {self.response.headers}")

        if self.response.status_code in [401, 500]:
            print("Unauthorized! Double-check the token or authorization process.")

        if self.response.status_code == 200 and "application/json" in self.response.headers.get('Content-Type', ''):
            self.json = self.response.json()
            if 'id' in self.json:
                self.meme_id = self.json['id']
                print(self.meme_id)
                return self.response
            else:
                raise KeyError("Response JSON does not contain 'id'")
        elif expect_failure:
            print(f"Expected failure: {self.response.status_code}")
        else:
            print(f"Unexpected failure: {self.response.status_code} - {self.response.text}")
