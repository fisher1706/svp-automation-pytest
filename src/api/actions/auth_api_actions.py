import time

from src.api.features.auth_api import AuthApi


class AuthApiActions(AuthApi):

    def __init__(self, api):
        super().__init__(api)
        self.token = None
        self.auth_api = AuthApi(api)

    def get_token(self):
        self.auth_api.get_otp_code()
        self.token = None
        for _ in range(4):
            self.auth_api.get_access_token(self.auth_api.otp_code)
            if self.auth_api.support.api.response.status_code == 200:
                self.token = 'Bearer ' + self.support.get_response_body()['access_payload']['access']
                break
            time.sleep(1)
        assert self.token, 'Token wasn\'t received after 5 attempts'
