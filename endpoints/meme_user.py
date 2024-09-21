import requests
import allure
import pytest
from endpoints.endpoint import Endpoint


class MemeUser:
    token = None

    @allure.step('Authorization in meme Api')
    def on_start(self):
        response = requests.post(
            'http://167.172.172.115:52355/authorize',
            json={'name': 'Bublik'}
        )
        assert response.status_code == 200, "Authorization request failed"

        response_json = response.json()
        print(f"Response JSON: {response_json}")

        self.token = response_json.get('token')
        print(f"Token: {self.token}")
        assert self.token, "Failed to retrieve token"

    @allure.step('Get token for authorization')
    def get_token(self):
        if not self.token:
            self.on_start()
        print(f"Token: {self.token}")
        return self.token
