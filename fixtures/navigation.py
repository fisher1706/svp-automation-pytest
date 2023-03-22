import pytest

from src.ui.pages.login import LoginPage


@pytest.fixture()
def go_to_admin_auth_page():
    login_page = LoginPage()
    login_page.visit(admin=True)
    login_page.wait_page_to_load()
    yield
    login_page.driver_actions.remove_item_from_local_storage('auth_token_default')


@pytest.fixture()
def go_to_auth_page():
    login_page = LoginPage()
    login_page.visit()
    login_page.wait_page_to_load()
    yield
    login_page.driver_actions.remove_item_from_local_storage('auth_token_default')
