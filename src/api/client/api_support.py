import json
from pathlib import Path

import allure
import jwt
from cerberus import Validator

from helpers.logger import yaml_logger

logger = yaml_logger.setup_logging(__name__)


class ApiSupport:

    def __init__(self, api):
        self.api = api
        self.session_id = None

    @classmethod
    def get_headers(cls, token):
        return {
            'Content-Type': 'application/json',
            'authorization': token
        }

    def get_response_body(self):
        json_response = self.api.response.json()
        return json_response

    def get_response_value(self, field_name):
        try:
            return self.api.response.json()[field_name]
        except KeyError as error:
            logger.error('\n', 'KeyError: ', error,
                         '\n', 'Payload: ', self.api.response.json())
        return None

    def parse_cookies(self, field_name, default_value=None):
        return next((c.value for c in self.api.response.cookies if field_name in c.name), default_value)

    @staticmethod
    def parse_json(filename):
        base_dir = Path(__file__).parent.parent.joinpath("schemas").joinpath(filename)
        with open(base_dir, encoding='utf-8') as schema_file:
            return json.loads(schema_file.read())

    def set_cookie_from_response_cookie(self, header_name):
        self.api.json_headers[header_name] = self.parse_cookies(field_name=header_name)

    def set_cookie_from_response_header(self, header_name, cookie_name):
        self.api.json_headers[header_name] = self.api.response.headers.get(cookie_name).split(";")[0]

    def get_http_header(self, header_name):
        return self.api.response.headers[header_name]

    def get_session_id(self):
        token = self.get_http_header("authorization")
        decoded_token = jwt.decode(token, options={"verify_signature": False})
        self.session_id = decoded_token['session-key']

    @allure.step
    def check_status_code(self, name: str, expect_code: int = 200):
        actual_code = self.api.response.status_code
        assert actual_code == expect_code, f"Request for {name} failed.\n" \
                                           f"Request URL: {self.api.response.request.url}\n" \
                                           f"Request body: {self.api.response.request.body}\n" \
                                           f"Expected status code: {expect_code}\n" \
                                           f"Actual status code: {actual_code}\n" \
                                           f"Reason: {self.api.response.reason}\n" \
                                           f"Text: {self.api.response.text}"

    @allure.step
    def check_response_field(self, field_name, nested_field=None, expected_value=None):
        """
        Current implementation supports 1 level of nested fields.

        Leave `nested_field` value as None in case the response structure is simple, like:
        {"field_name": "message"}

        Define `nested_field` value if the response structure contains nested fields, like:
        {"field_name": {"nested_field_name": "message"}}
        """
        json_response = self.api.response.json()
        actual_message = json_response[field_name]
        if nested_field:
            expected_value = nested_field
        assert actual_message == expected_value, f"Invalid [{field_name}] field value." \
                                                 f"Request URL: {self.api.response.request.mlsd_url}\n" \
                                                 f"Expected message: {expected_value}\n" \
                                                 f"Actual message  : {actual_message}\n" \
                                                 f"Reason: {self.api.response.reason}\n" \
                                                 f"Text: {self.api.response.text}"

    @allure.step
    def validate_response_attribute(self, field_name, expected_value):
        response = self.get_response_body()
        actual_value = response['data']['attributes'][field_name]
        assert str(actual_value) == str(
            expected_value), f"Value for {field_name}: {actual_value} but expected: {expected_value}"

    @allure.step
    def validate_response_error(self, field_name, expected_value, initial_field=None):
        """
        Use `initial_field` if the response structure is:
        { "initial_field": { "errors": { "field_name": ""}}}
        """
        response = self.get_response_body()
        try:
            if initial_field:
                actual_value = response[initial_field]["errors"][field_name]
            else:
                actual_value = response["errors"][field_name]
        except KeyError as error:
            raise Exception(f"field '{field_name}' was not found in response: {response}") from error
        assert actual_value == expected_value, f"Response message: {actual_value} but expected: {expected_value}"

    @allure.step
    def check_response_schema(self, schema_name):
        schema = self.parse_json(f"response/{schema_name}")
        json_response = self.api.response.json()
        validator = Validator(schema)
        is_valid = validator.validate(json_response)
        assert is_valid, validator.errors
        return self
