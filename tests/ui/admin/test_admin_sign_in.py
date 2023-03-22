import allure
import pytest

from src.ui.actions.base_actions import BaseActions
from src.ui.actions.login_actions import LoginActions
from test_data.constants import UserInfo
from test_data.dataset import LoginDataset
from test_data.validation_message import SuccessMessage


@allure.feature('Login to SVP')
@pytest.mark.auth_suite
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.usefixtures("go_to_admin_auth_page")
class TestAdminSignIn:  # pylint: disable=attribute-defined-outside-init

    @pytest.fixture(autouse=True)
    def pre_test(self):
        self.logins_action = LoginActions()
        self.base_actions = BaseActions()

    @allure.title('C6249 Check invalid login and password')
    @pytest.mark.parametrize("login,password,expected_message", LoginDataset.INVALID_CREDENTIALS_UI)
    def test_login_with_invalid_credentials(self, login, password, expected_message):
        self.logins_action.log_in_user(login, password)
        self.base_actions.verify_message(expected_message)

    @allure.title('C6248 Check valid Login and Password')
    def test_login_with_valid_credentials(self):
        self.logins_action.log_in_user(UserInfo.DEFAULT_LOGIN, UserInfo.DEFAULT_PASSWORD)
        self.base_actions.verify_message(SuccessMessage.ADMIN_CONFIRM_CODE)
        self.logins_action.proceed_2fa(user_type=True)
        self.logins_action.driver_actions.clear_local_storage()

    @allure.title('C6250 Check log in without entering email and password')
    def test_login_without_entering_email_and_password(self):
        self.logins_action.log_in_user('', '', click_continue=False)
