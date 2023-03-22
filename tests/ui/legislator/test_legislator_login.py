import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.login_actions import LoginActions
from src.ui.actions.spa_actions import SPAActions
from test_data.constants import Title, UserType, UserInfo
from test_data.dataset import LoginDataset
from test_data.validation_message import SuccessMessage


@allure.feature('Login as Legislator to SVP')
@pytest.mark.legislator
@pytest.mark.auth_suite
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestLegislatorLogin:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture(autouse=True)
    def pre_test(self, api):
        self.login_actions = LoginActions()
        self.base_actions = BaseActions()
        self.spa_actions = SPAActions(api)

    @pytest.fixture()
    def pre_test_legislator(self, api):
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           login_tcenter=False)

    @pytest.fixture()
    def pre_test_legislator_via_email(self, api):
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           login_tcenter=False,
                                                           two_factor_verification='email')

    @allure.title('C8820 Check invalid login and password')
    @pytest.mark.parametrize("login,password,expected_message", LoginDataset.INVALID_CREDENTIALS_UI)
    def test_legislator_with_invalid_credentials(self, go_to_auth_page, login, password, expected_message):
        self.login_actions.log_in_user(login, password)
        self.base_actions.verify_message(expected_message)

    @allure.title('Check valid Login and Password 2fa via email')
    def test_legislator_with_valid_credentials_via_email(self, pre_test_legislator_via_email):
        self.spa_actions.base_actions.verify_message(UserType.LEGISLATOR)

    @allure.title('C8819 Check valid Login and Password')
    def test_legislator_with_valid_credentials(self, pre_test_legislator):
        self.spa_actions.base_actions.verify_message(UserType.LEGISLATOR)

    @allure.title('C8821 Check log in without entering email and password')
    def test_legislator_without_entering_email_and_password(self, go_to_auth_page):
        self.login_actions.log_in_user('', '', click_continue=False)

    @allure.title('C8840 Check ability to log out from system')
    def test_legislator_log_out_from_spa(self, pre_test_legislator):
        self.login_actions.log_out_user()
        self.spa_actions.base_actions.verify_expected_title(Title.SPA_SIGN_IN)

    @allure.title('C8863 Back to Home page from "Confirm verification code')
    def test_legislator_back_to_home_from_2fa(self, go_to_auth_page):
        self.login_actions.login_user(UserInfo.LEGISLATOR_LOGIN, UserInfo.DEFAULT_PASSWORD)
        self.spa_actions.base_actions.verify_message(SuccessMessage.CONFIRM_CODE)
        self.spa_actions.spa_change_password.click_back_btn()
        self.spa_actions.base_actions.verify_expected_title(Title.SPA_PROFESSIONAL_ACCREDITATION_PROGRAM)