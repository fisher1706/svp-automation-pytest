import pytest

from helpers.logger.yaml_logger import setup_logging
from src.api.client.api_client import ApiClient


@pytest.fixture(scope="session", autouse=True)
def api():
    setup_logging()
    api_client = ApiClient()
    yield api_client
    api_client.clean_session_cookies()
