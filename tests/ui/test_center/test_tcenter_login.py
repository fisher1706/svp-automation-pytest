import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.login_actions import LoginActions
from src.ui.actions.spa_actions import SPAActions
from test_data.constants import Title, UserType


@allure.feature('Login as Test Center to SVP')
@pytest.mark.tc
@pytest.mark.auth_suite
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestTCenterLogin:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.spa_actions = SPAActions(api)
        self.login_actions = LoginActions()
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_tcenter=True,
                                                           is_tcenter_activate=True)

    @pytest.fixture()
    def pre_test_via_email(self, api):
        self.spa_actions = SPAActions(api)
        self.login_actions = LoginActions()
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions, is_tcenter=True,
                                                           is_tcenter_activate=True,
                                                           two_factor_verification='email')

    @allure.title('Check valid Login and Password 2fa via email')
    def test_tc_with_valid_credentials_via_email(self, pre_test_via_email):
        self.spa_actions.base_actions.verify_message(UserType.TEST_CENTER_OWNER)

    @allure.title('C8819 Check valid Login and Password')
    def test_tc_with_valid_credentials(self, pre_test):
        self.spa_actions.base_actions.verify_message(UserType.TEST_CENTER_OWNER)

    @allure.title('C8840 Check ability to log out from system')
    def test_tc_log_out_from_spa(self, pre_test):
        self.login_actions.log_out_user()
        self.spa_actions.base_actions.verify_expected_title(Title.SPA_SIGN_IN)
