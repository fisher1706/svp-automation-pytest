import os

import requests


class ApiClient:

    def __init__(self):
        self.session = requests.session()
        self.api_url = os.environ.get('API_URL')
        self.response = None
        self.json_headers = {'Content-Type': 'application/json'}

    def get(self, url, endpoint, body=None, params=None, headers=None):
        self.response = self.session.get(url=url + endpoint, data=body, params=params,
                                         headers=self.json_headers if not headers else headers)

    def post(self, url, endpoint, body=None, params=None, headers=None):
        self.response = self.session.post(url=url + endpoint, data=body, params=params,
                                          headers=self.json_headers if not headers else headers)

    def delete(self, url, endpoint, body=None, params=None):
        self.response = self.session.delete(url=url + endpoint, data=body, params=params, headers=self.json_headers)

    def patch(self, url, endpoint, body=None, params=None):
        self.response = self.session.patch(url=url + endpoint, data=body, params=params, headers=self.json_headers)

    def put(self, url, endpoint, body=None, params=None, headers=None):
        self.response = self.session.put(url=url + endpoint, data=body, params=params,
                                         headers=self.json_headers if not headers else headers)

    def clean_session_cookies(self):
        self.session.cookies.clear()
        self.json_headers = {'Content-Type': 'application/json'}
