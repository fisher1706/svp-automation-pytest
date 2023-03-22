import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.spa_actions import SPAActions


@allure.feature('Change Password as Test Center Owner')
@pytest.mark.tc
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestTCenterRestorePassword:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_tcenter=True,
                                                           is_tcenter_activate=True)

    @allure.title('Checking the ability to view Change Password form')
    @pytest.mark.skip('The back button returns to the home page instead of the application page')
    def test_tc_view_change_password_form(self, pre_test):
        self.spa_actions.verify_view_change_password_form()

    @allure.title('Checking the ability to change password')
    def test_tc_change_password(self, pre_test):
        self.spa_actions.verify_change_password()

    @allure.title('C8839 Check ability to change password with invalid "new password"')
    def test_tc_change_password_with_invalid_new_password(self, pre_test):
        self.spa_actions.verify_changing_password_with_invalid_new_password()

    @allure.title('Check ability to change password with invalid password as Legislator')
    # Covered tests
    # C8838 Check ability to change password with invalid current password
    # C8841 Check ability to change password with mismatch "New password"
    # C8842 Check ability to change password with invalid "confirm password"
    # C8843 Check ability to change password with current Password
    def test_tc_change_password_with_invalid_password(self, pre_test):
        self.spa_actions.verify_change_password_with_invalid_password()
