import allure
import pytest

from src.api.features.spa_api import SPAApi
from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.spa_actions import SPAActions
from src.ui.actions.spa_reports_actions import SPAReportsActions
from test_data.constants import Title
from test_data.dataset import WrongCertificateDataset
from test_data.validation_message import WarningMessage, ErrorMessage


@allure.feature('Reports tab as Legislator')
@pytest.mark.legislator
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestLegislatorReports:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.spa_api = SPAApi(api)
        self.spa_actions = SPAActions(api)
        self.spa_reports_actions = SPAReportsActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           is_tcenter=True,
                                                           login_tcenter=False)

    @allure.title('Checking the ability to search entry by filters and clear filters on Reports tab')
    def test_legislator_check_filters_and_clear_filters_reports_tab(self, pre_test):
        self.spa_actions.add_group()
        self.spa_actions.spa_reports.visit()
        self.spa_actions.base_actions.verify_expected_title(Title.REPORTS)
        entry_info = self.spa_actions.get_info_of_last_entry(date=True)
        keys = list(entry_info.keys())
        self.spa_actions.verify_id_reports_tab(entry_info, keys[0])
        self.spa_actions.verify_group_no(entry_info, keys[1])
        self.spa_actions.verify_amount_reports_tab(entry_info, keys[2])
        self.spa_actions.verify_date_reports_tab(entry_info, keys[3])
        self.spa_actions.spa_reports.verify_success_status()
        self.spa_actions.base_actions.wait_spinners_to_disappear()
        self.spa_actions.click_clear_filter_btn()
        self.spa_actions.spa_reports.verify_disabling_filters_fields()

    @allure.title('Checking the certificate is valid scenario')
    def test_legislator_valid_scenario(self, pre_test):
        self.spa_actions.add_group()
        self.spa_reports_actions.pass_steps_for_checking_certificate_scenario(ErrorMessage.MSG_EXPIRED_CERTIFICATE)

    @allure.title('Checking the certificate is expired scenario')
    def test_legislator_certificate_is_expired(self, pre_test):
        self.spa_actions.add_group()
        self.spa_actions.spa_upload.visit()
        self.spa_actions.upload_labor_with_previous_date_and_add_credits()
        serial_number = self.spa_reports_actions.pass_steps_for_checking_certificate_scenario(
            ErrorMessage.MSG_EXPIRED_CERTIFICATE,
            is_valid_scenario=False)
        self.spa_actions.spa_reports.click_check_validity_btn()
        self.spa_actions.base_actions.verify_expected_title(Title.CHECK_VALIDITY)
        self.spa_actions.spa_reports.verify_btn_verify_is_disabled()
        passport_number = self.spa_actions.csv_helper.passport_numbers[0]
        self.spa_actions.spa_reports.fill_passport_number(passport_number)
        self.spa_actions.spa_reports.fill_certificate_serial_number(serial_number)
        self.spa_actions.spa_reports.click_verify_btn()
        self.spa_actions.spa_reports.verify_msg_certificate(ErrorMessage.MSG_EXPIRED_CERTIFICATE)
        self.spa_actions.spa_reports.verify_results_passport_number(passport_number)
        self.spa_actions.spa_reports.verify_result_certificate_serial_number(WrongCertificateDataset.WRONG_CERTIFICATE)

    @allure.title('Checking the passport number is valid but its not for the certificate entered serial number '
                  'scenario')
    def test_legislator_wrong_certificate(self, pre_test):
        self.spa_actions.add_group()
        self.spa_actions.spa_reports.visit()
        self.spa_actions.spa_reports.click_check_validity_btn()
        passport_number = self.spa_actions.csv_helper.passport_numbers[0]
        self.spa_actions.spa_reports.fill_passport_number(passport_number)
        self.spa_actions.spa_reports.fill_certificate_serial_number(WrongCertificateDataset.WRONG_CERTIFICATE)
        self.spa_actions.spa_reports.click_verify_btn()
        self.spa_actions.spa_reports.verify_msg_certificate(WarningMessage.MSG_WRONG_CERTIFICATE)
        self.spa_actions.spa_reports.verify_results_passport_number(passport_number)
        self.spa_actions.spa_reports.verify_result_certificate_serial_number(WrongCertificateDataset.WRONG_CERTIFICATE)

    @allure.title('Checking the passport number does not match for this certificate serial number scenario')
    def test_legislator_wrong_passport_number(self, pre_test):
        self.spa_actions.add_group()
        self.spa_actions.spa_reports.visit()
        serial_number = self.spa_api.get_certificate_number()
        self.spa_actions.spa_reports.click_check_validity_btn()
        self.spa_actions.spa_reports.fill_passport_number(WrongCertificateDataset.WRONG_PASSPORT_NUMBER)
        self.spa_actions.spa_reports.fill_certificate_serial_number(serial_number)
        self.spa_actions.spa_reports.click_verify_btn()
        self.spa_actions.spa_reports.verify_msg_certificate(ErrorMessage.MSG_WRONG_CERTIFICATE)
        self.spa_actions.spa_reports.verify_results_passport_number(WrongCertificateDataset.WRONG_PASSPORT_NUMBER)
        self.spa_actions.spa_reports.verify_result_certificate_serial_number(serial_number)

    @allure.title('Checking the certificate does not exist scenario')
    def test_legislator_certificate_does_not_exist(self, pre_test):
        self.spa_actions.add_group()
        self.spa_actions.spa_reports.visit()
        self.spa_actions.spa_reports.click_check_validity_btn()
        self.spa_actions.spa_reports.fill_passport_number(WrongCertificateDataset.INCORRECT_NUMBER)
        self.spa_actions.spa_reports.fill_certificate_serial_number(WrongCertificateDataset.INCORRECT_NUMBER)
        self.spa_actions.spa_reports.click_verify_btn()
        self.spa_actions.spa_reports.verify_msg_certificate(ErrorMessage.MSG_CERTIFICATE_NOT_EXIST)
        self.spa_actions.spa_reports.verify_results_passport_number(WrongCertificateDataset.INCORRECT_NUMBER)
        self.spa_actions.spa_reports.verify_result_certificate_serial_number(WrongCertificateDataset.INCORRECT_NUMBER)

    @allure.title('Check the ability to download certificate as a Legislator on Reports tab')
    def test_legislator_download_certificate(self, pre_test, clear_temp_folder):
        self.spa_actions.verify_download_certificate_report(is_reports_tab=True)

    @allure.title('Check the ability to download report as a Legislator')
    def test_legislator_download_report(self, pre_test, clear_temp_folder):
        self.spa_actions.verify_download_certificate_report(is_certificate=False, is_reports_tab=True)

    @allure.title('Check the ability to download report on view payment details as a Legislator')
    def test_legislator_download_report_on_view_payment_details(self, pre_test, clear_temp_folder):
        self.spa_actions.verify_download_certificate_report(is_certificate=False,
                                                            is_reports_tab=True,
                                                            is_view_payment=True)
