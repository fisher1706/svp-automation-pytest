from src.api.features.spa_api import SPAApi
from src.ui.actions.spa_actions import SPAActions
from test_data.constants import Title


class SPAReportsActions(SPAActions):
    def __init__(self, api):
        super().__init__(api)
        self.spa_api = SPAApi(api)

    def pass_steps_for_checking_certificate_scenario(self, msg_certificate, is_valid_scenario=True):
        self.spa_reports.visit()
        serial_number = self.spa_api.get_certificate_number()
        self.base_actions.verify_expected_title(Title.REPORTS)
        self.spa_reports.click_check_validity_btn()
        self.base_actions.verify_expected_title(Title.CHECK_VALIDITY)
        self.spa_reports.verify_btn_verify_is_disabled()
        passport_number = self.csv_helper.passport_numbers[0]
        self.spa_reports.fill_passport_number(passport_number)
        self.spa_reports.fill_certificate_serial_number(serial_number)
        self.spa_reports.click_verify_btn()
        self.spa_reports.verify_msg_certificate(msg_certificate)
        self.spa_reports.verify_results_passport_number(passport_number)
        if is_valid_scenario:
            self.spa_reports.verify_result_certificate_serial_number(serial_number)
            self.spa_reports.verify_labor_name()
            self.spa_reports.verify_passport_number(passport_number)
        else:
            return serial_number
        return None
