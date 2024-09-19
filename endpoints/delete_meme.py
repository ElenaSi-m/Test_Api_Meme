import requests
import allure
import pytest
from endpoints.endpoint import Endpoint


@pytest.mark.usefixtures("cleanup")
class DeleteMeme(Endpoint):

    @allure.step('Delete meme')
    def delete_meme(self, meme_id, headers=None, token=None):
        headers = headers if headers else self.headers
        if token:
            headers['Authorization'] = f"{token}"

        self.response = requests.delete(
            f'{self.url}/meme/{meme_id}',
            headers=headers
        )
        print(f"Response status: {self.response.status_code}")
        print(f"Response body: {self.response.text}")

        if self.response.status_code == 200 or self.response.status_code == 204:
            if 'application/json' in self.response.headers.get('Content-Type', ''):
                try:
                    self.json = self.response.json()
                except requests.exceptions.JSONDecodeError:
                    print("Failed to parse JSON response.")
                    self.json = None
            else:
                self.json = self.response.text
        else:
            self.json = self.response.text

    @allure.step('Check if meme was deleted')
    def check_if_meme_deleted(self):
        print(f"Response status: {self.response.status_code}")
        print(f"Response body: {self.response.text}")
        assert self.response.status_code in [200, 204], 'status is not 200, 204'

    def check_status_of_deleted_meme(self, meme_id):
        headers = self.headers
        self.response = requests.get(
            f'{self.url}/meme/{meme_id}',
            headers=headers
        )
        print(f"Response status of follow-up GET request: {self.response.status_code}")
        print(f"Response body of follow-up GET request: {self.response.text}")

        if self.response.status_code == 404:
            assert self.response.status_code == 404, 'Meme still exists after deletion'
        else:
            raise AssertionError(f"Unexpected status code: {self.response.status_code}")
