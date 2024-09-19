import allure
import requests


class Endpoint:
    url = 'http://167.172.172.115:52355'
    response = None
    json = None
    headers = {'Content-Type': 'application/json'}

    @allure.step('Check that text is the same as sent')
    def check_response_text_is_correct(self, text):
        assert self.response is not None, "Response is None!"
        assert self.json is not None, "JSON response is None!"
        assert self.json.get('text') == text, 'text does not match the expected text'

    @allure.step('Check that url is the same as sent')
    def check_response_url_is_correct(self, url):
        assert self.response is not None, "Response is None!"
        assert self.json is not None, "JSON response is None!"
        assert self.json.get('url') == url, 'url does not match the expected url'

    @allure.step('Check that tags are the same as sent')
    def check_response_tags_is_correct(self, tags):
        assert self.response is not None, "Response is None!"
        assert self.json is not None, "JSON response is None!"
        assert self.json.get('tags') == tags, 'tags do not match the expected tags'

    @allure.step('Check that info is the same as sent')
    def check_response_info_is_correct(self, expected_info):
        response_info = self.json.get("info", {})
        assert response_info.get("colors") == expected_info["colors"], 'colors do not match the expected'
        assert response_info.get("objects") == expected_info["objects"], 'objects do not match the expected'

    @allure.step('Check if response is 200')
    def check_that_status_is_200(self):
        print(f"Response status: {self.response.status_code}")
        print(f"Response body: {self.response.text}")
        assert self.response.status_code == 200, 'status is not 200'

    @allure.step('Check if response is 400')
    def check_that_status_is_400(self):
        print(f"Response status: {self.response.status_code}")
        print(f"Response body: {self.response.text}")
        assert self.response.status_code == 400, 'Supposed to be invalid format, status code is not 400'

    @allure.step('Check if response is 401')
    def check_that_status_is_401(self):
        print(f"Response status: {self.response.status_code}")
        print(f"Response body: {self.response.text}")
        assert self.response.status_code in [401, 500], 'Supposed to be UNAUTHORIZED, status code is not 401'

    @allure.step('Check if response is 405')
    def check_that_status_is_405(self):
        print(f"Response status: {self.response.status_code}")
        print(f"Response body: {self.response.text}")
        assert self.response.status_code == 405, 'Supposed to be invalid url format, status code is not 405'

    @allure.step('Check if response is 404')
    def check_that_status_is_404(self):
        print(f"Response status: {self.response.status_code}")
        print(f"Response body: {self.response.text}")
        assert self.response.status_code == 404, 'Supposed to be NOT FOUND, status code is 404'


class MemeUser:
    token = None

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

    def get_token(self):
        if not self.token:
            self.on_start()
        print(f"Token: {self.token}")
        return self.token
