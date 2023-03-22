import pytest
from selenium.common import WebDriverException

from helpers.file_helper import FileHelper
from src.ui.pages.login import LoginPage


@pytest.fixture()
def logout_after_test():
    yield
    try:
        LoginPage().driver_actions.remove_item_from_local_storage('auth_token_default')
    except WebDriverException:
        pass


@pytest.fixture()
def clear_temp_folder():
    yield
    FileHelper().clear_temp_folder(check=False)
