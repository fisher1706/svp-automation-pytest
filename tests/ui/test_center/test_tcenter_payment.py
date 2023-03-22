import allure
import pytest

from src.api.actions.admin_api_actions import AdminApiActions
from src.api.actions.auth_api_actions import AuthApiActions
from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.login_actions import LoginActions
from src.ui.actions.spa_payment_actions import SPAPaymentActions
from test_data.constants import Title


@allure.feature('Payment tab as Test Center Owner')
@pytest.mark.tc
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestTCenterPayment:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.base_actions = BaseActions()
        self.login_actions = LoginActions()
        self.spa_payment_actions = SPAPaymentActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_payment_actions.auth_api_actions,
                                                           is_tcenter=True,
                                                           is_tcenter_activate=True)

    @pytest.fixture()
    def pre_test_without_creation_entities(self, api):
        self.base_actions = BaseActions()
        self.login_actions = LoginActions()
        self.auth_api_actions = AuthApiActions(api)
        self.admin_api_actions = AdminApiActions(api)
        self.spa_payment_actions = SPAPaymentActions(api)

    @allure.title('C10345 Check the ability to add credits as a Test Center')
    def test_tc_get_credits(self, pre_test):
        self.spa_payment_actions.verify_ability_to_add_credits()

    @allure.title('C10346 Check the ability to verify input fields on add credits as a Test Center')
    def test_tc_ability_to_verify_input_fields_on_add_credits(self, pre_test):
        self.spa_payment_actions.verify_input_fields_on_add_credits()

    @allure.title('C6951 C6952 C6953 Checking validate the issuing certificate and showing error message to agree '
                  'before made a duplicate payment as Test Center')
    @pytest.mark.skip('Add possibility to make duplicate payment with date test center owner')
    def test_tc_error_message_to_agree_before_made_duplicate_payment(self,
                                                                     pre_test_without_creation_entities,
                                                                     amount=1):
        self.auth_api_actions.get_token()
        self.admin_api_actions.put_permissions(self.auth_api_actions.token)
        self.login_actions.log_in_to_spa_with_permanent_email()
        self.spa_payment_actions.verify_error_message_duplicate_payment(amount)
        self.base_actions.verify_expected_title(expected_title=Title.PAYMENT_CONFIRMATION)

    @allure.title('Check number of labors and total amount on payment tab as a Test Center')
    def test_tc_number_of_labors_and_total_amount_counters(self, pre_test, amount=1):
        self.spa_payment_actions.upload_group_and_add_credits(amount)
        self.spa_payment_actions.spa_payment.select_last_entry()
        self.spa_payment_actions.spa_payment.verify_number_of_labors(amount)
        self.spa_payment_actions.spa_payment.verify_total_amount(amount)

    @allure.title('Check the ability to download certificate as a Test Center')
    def test_tc_download_certificate(self, pre_test, clear_temp_folder):
        self.spa_payment_actions.verify_download_certificate_report()

    @allure.title('Check Payment Confirmation info and Transaction Information as a Test Center')
    def test_tc_payment_info(self, pre_test):
        self.spa_payment_actions.verify_payment_information()

    @allure.title('Check the ability to download invoice after passing get credits flow as a Test Center')
    def test_tc_invoice_after_passing_get_credits_flow(self, pre_test, clear_temp_folder):
        self.spa_payment_actions.verify_download_invoice(is_zip_file=True)
