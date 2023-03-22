import json

import allure

from src.api.client.api_support import ApiSupport
from test_data.constants import UserInfo


class AuthApi:

    def __init__(self, api):
        self.api = api
        self.support = ApiSupport(api)
        self.otp_code = None

    @allure.step("POST api/v1/login?locale=en :: get otp code")
    def get_otp_code(self, email=UserInfo.DEFAULT_LOGIN, user_type='admin', expect_code=401):
        json_body = {
            "user": {
                "login": email,
                "password": UserInfo.DEFAULT_PASSWORD,
                "fe_app": user_type
            }
        }
        self.api.post(url=self.api.api_url, endpoint='api/v1/login?locale=en', body=json.dumps(json_body))
        self.support.check_status_code(name="Two factor auth", expect_code=expect_code)
        self.otp_code = self.support.get_response_value('otp_code')
        return self

    @allure.step("POST api/v1/login?locale=en :: get access token")
    def get_access_token(self, otp_code, email=UserInfo.DEFAULT_LOGIN, fe_app='admin'):
        json_body = {
            'user': {
                'login': email,
                'password': UserInfo.DEFAULT_PASSWORD,
                'fe_app': fe_app,
                'otp_attempt': otp_code
            }
        }
        self.api.post(url=self.api.api_url, endpoint='api/v1/login?locale=en', body=json.dumps(json_body))
        return self

    @allure.step("DELETE api/v1/login?locale=en :: logout")
    def logout_user(self, expect_code=200):
        self.api.delete(url=self.api.api_url, endpoint='api/v1/logout?locale=en')
        self.support.check_status_code(name="Logout", expect_code=expect_code)
        return self

    @allure.step("POST /session/language/locale :: change language")
    def change_locale(self, locale, expect_code=200, expect_schema='identities.json'):
        self.api.post(url=self.api.api_url, endpoint=f"/session/language/{locale}")
        self.support.check_status_code(name="Change locale", expect_code=expect_code)
        if expect_code == 200:
            self.support.check_response_schema(schema_name=expect_schema)

    @allure.step("PUT api/v1/users/set_password?locale=en :: put set password")
    def put_set_password(self, token, expect_code=200):
        json_body = {
            'password': UserInfo.DEFAULT_PASSWORD,
            'password_confirmation': UserInfo.DEFAULT_PASSWORD,
            'password_token': token,
        }
        self.api.post(url=self.api.api_url, endpoint='api/v1/users/set_password?locale=en', body=json.dumps(json_body))
        self.support.check_status_code(name='Put set password', expect_code=expect_code)
