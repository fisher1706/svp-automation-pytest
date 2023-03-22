import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.spa_actions import SPAActions


@allure.feature('Transaction History tab as Test Center Owner')
@pytest.mark.tc
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestTCenterTransactionHistory:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_tcenter=True,
                                                           is_tcenter_activate=True)
        self.spa_actions.spa_payment.visit()

    @allure.title('Checking the ability to search entry by filters and clear filters on Transaction History tab')
    def test_tc_check_filters_and_clear_filters(self, pre_test):
        self.spa_actions.verify_filters_on_transaction_history()

    @allure.title('C9319 C9320 Checking transaction statuses on Transaction History tab as a a Test Center')
    @allure.issue(url='https://is-takamol.atlassian.net/browse/PVPE-1578',
                  name='[SPA] - Statuses.Prepared_checkout displays on Transactions History Page')
    @pytest.mark.skip
    def test_tc_check_transaction_statuses(self, pre_test):
        self.spa_actions.verify_transactions_statuses()

    @allure.title('Check the ability to download invoice as a Test Center')
    def test_tc_download_certificate(self, pre_test, clear_temp_folder):
        self.spa_actions.verify_download_invoice(is_transaction_history=True)

    @allure.title('Check the ability to download invoice on view payment details as a Test Center')
    def test_tc_download_certificate_on_view_payment_details(self, pre_test, clear_temp_folder):
        self.spa_actions.verify_download_invoice(is_view_payment=True)
