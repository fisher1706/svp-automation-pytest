import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.password_actions import PasswordActions
from src.ui.actions.spa_actions import SPAActions
from src.ui.actions.spa_registration_actions import SPARegistration
from test_data.constants import Title, Authentication


@allure.feature('Registration Test Center to SVP')
@pytest.mark.tc
@pytest.mark.auth_suite
@pytest.mark.daily
@pytest.mark.ui
class TestTCenterRegistration:  # pylint: disable=attribute-defined-outside-init, unused-argument

    @pytest.fixture()
    def pre_test(self, api):
        self.base_actions = BaseActions()
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_tcenter=True,
                                                           is_tcenter_activate=True,
                                                           two_factor_verification=Authentication.EMAIL)

    @pytest.fixture()
    def pre_test_without_login(self, api):
        self.password_actions = PasswordActions()
        self.spa_registration = SPARegistration()
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_tcenter=True,
                                                           login=False)

    @allure.title('Check receive an invitation email and set password with valid data')
    def test_tc_receive_an_invitation_email_and_set_password_with_valid_data(self, pre_test):
        self.base_actions.verify_expected_title(expected_title=Title.UPLOADED_FILES)

    @allure.title('Check set password with invalid data')
    def test_tc_set_password_with_invalid_data(self, pre_test_without_login):
        self.password_actions.verify_password_with_invalid_data()

    @allure.title("C9327 C9328 Check then password can't be set if it had set and can be set if it hasn't been set "
                  "before")
    def test_tc_password_validation(self, pre_test_without_login):
        self.spa_registration.verify_password_validation()
