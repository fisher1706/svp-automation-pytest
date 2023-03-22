import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.spa_actions import SPAActions


@allure.feature('Account as Legislator')
@pytest.mark.legislator
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestLegislatorAccount:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           login_tcenter=False)
        return self

    @pytest.fixture()
    def pre_test_with_tcenter(self, api):
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           is_tcenter=True,
                                                           is_tcenter_activate=True,
                                                           login_tcenter=False)

    @allure.title('Checking the ability to view account information')
    def test_legislator_view_account_information(self, pre_test):
        account = pre_test.background_actions.admin_api_actions.legislator_account
        self.spa_actions.verify_view_account_information(account)

    @allure.title('Checking the ability to edit account information with valid data')
    def test_legislator_edit_account_information_with_valid_data(self, pre_test):
        self.spa_actions.verify_edit_account_information_with_valid_data()

    @allure.title('Checking the ability to edit account information with invalid data')
    def test_legislator_edit_account_information_with_invalid_data(self, pre_test):
        self.spa_actions.verify_edit_account_information_with_invalid_data()

    @allure.title('Checking the ability to edit account information with empty data and duplicate email')
    def test_legislator_edit_account_information_with_empty_data_and_duplicate_email(self, pre_test_with_tcenter):
        self.spa_actions.verify_edit_account_information_with_empty_data_and_duplicate_email()
