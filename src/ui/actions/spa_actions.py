import datetime

import allure

from helpers.csv_helper import CSVHelper
from helpers.decorators import for_all_methods
from helpers.file_helper import FileHelper
from src.api.actions.admin_api_actions import AdminApiActions
from src.api.actions.auth_api_actions import AuthApiActions
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.login_actions import LoginActions
from src.ui.actions.password_actions import PasswordActions
from src.ui.pages.base import BasePage
from src.ui.pages.spa import SPA
from src.ui.pages.spa_account import SPAAccountPage
from src.ui.pages.spa_change_password import SPAChangePasswordPage
from src.ui.pages.spa_labors import SPALaborsPage
from src.ui.pages.spa_payment import SPAPaymentPage
from src.ui.pages.spa_reports import SPAReportsPage
from src.ui.pages.spa_test_centers import SPATestCentersPage
from src.ui.pages.spa_transaction_history import SPATransactionHistoryPage
from src.ui.pages.spa_upload import SPAUploadPage
from test_data.constants import Title, ExamResult, UserInfo, Labels, TransactionState, TransactionStatuses, DirPath, \
    DateType
from test_data.dataset import GetCreditsDataset, EditEmailDataset, WrongTestCenterDataset, ChangePasswordDataset, \
    PageNumbersDataset
from test_data.models.model_builder import ModelBuilder
from test_data.validation_message import SuccessMessage, WarningMessage, ErrorMessage


@for_all_methods(allure.step)
class SPAActions(BasePage, SPA):

    def __init__(self, api):
        super().__init__()
        self.tcenter_name = None
        self.account = None
        self.account_tcenter = None
        self.file_id = Labels.FILE_ID
        self.base_actions = BaseActions()
        self.csv_helper = CSVHelper()
        self.file_helper = FileHelper()
        self.admin_api_actions = AdminApiActions(api)
        self.auth_api_actions = AuthApiActions(api)
        self.login_actions = LoginActions()
        self.password = PasswordActions()
        self.spa_account = SPAAccountPage()
        self.spa_change_password = SPAChangePasswordPage()
        self.spa_upload = SPAUploadPage()
        self.spa_labors = SPALaborsPage()
        self.spa_payment = SPAPaymentPage()
        self.spa_test_centers = SPATestCentersPage()
        self.spa_reports = SPAReportsPage()
        self.spa_transactions_history = SPATransactionHistoryPage()

    def pass_labor_flow(self, amount: int = 1):
        self.upload_group_of_labors(amount)
        self.spa_payment.visit()
        self.add_credit(amount)
        self.base_actions.wait_until_page_updates(self.spa_payment.select_last_entry, Title.PAYMENT)
        self.spa_payment.click_issue_btn()
        self.spa_payment.click_confirm_btn()

    def __pass_labor_flow_and_go_to_labors_tab(self, amount: int):
        self.pass_labor_flow(amount)
        self.spa_labors.visit()
        self.base_actions.wait_spinners_to_disappear()

    def add_credit(self, amount):
        self.get_credit(amount)
        self.fill_card_details()
        self.spa_payment.click_btn_pay_now()
        self.spa_payment.select_dropdown_transaction_state(TransactionState.SUCCESS)
        self.spa_payment.click_btn_transaction_pay()
        self.base_actions.wait_spinners_to_disappear()
        self.base_actions.verify_expected_title(expected_title=Title.PAYMENT_CONFIRMATION)
        self.spa_payment.visit()
        self.base_actions.wait_spinners_to_disappear()

    def pass_credit_flow(self, amount, state):
        self.get_credit(amount)
        self.fill_card_details()
        self.spa_payment.click_btn_pay_now()
        if state != TransactionState.PREPARED_CHECKOUT:
            self.spa_payment.select_dropdown_transaction_state(state)
            self.spa_payment.click_btn_transaction_pay()
            self.base_actions.wait_spinners_to_disappear()
            if state == TransactionState.SUCCESS:
                self.base_actions.verify_expected_title(Title.PAYMENT_CONFIRMATION)

    # TODO: Add verifications for file information after corrects on UI
    def __verify_popup_file_information(self):
        pass

    def add_individual_labor(self, tcenter=True):
        self.account = ModelBuilder.build_random_labor()
        self.spa_upload.click_add_individual_btn()
        self.spa_upload.fill_field_national_id(self.account.national_id)
        self.spa_upload.fill_field_labor_name(self.account.labor_name)
        self.spa_upload.fill_field_passport(self.account.passport)
        if not tcenter:
            self.spa_upload.select_tcenter(self.tcenter_name)
        self.spa_upload.select_exam_date(self.account.exam_date)
        self.spa_upload.select_occupation(self.account.occupation)
        self.spa_upload.fill_field_scope(self.account.scope)
        self.spa_upload.click_add_btn()
        self.spa_upload.verify_name(self.account.labor_name)
        self.spa_upload.click_add_btn()
        return self.account

    def add_group_of_labors(self, amount: int, category: str = ModelBuilder.CATEGORY,
                            verify_info_popup: bool = False):
        self.spa_upload.click_add_group_btn()
        self.base_actions.verify_expected_title(Title.ADD_GROUP)
        if not self.tcenter_name:
            self.tcenter_name = UserInfo.TC_NAME
        self.spa_upload.select_tcenter_list(self.tcenter_name)
        self.spa_upload.select_category_list(category)
        self.spa_upload.upload_csv_file(amount)
        if verify_info_popup:
            self.__verify_popup_file_information()
        self.spa_upload.verify_total_labors(amount)
        self.spa_upload.click_add_btn()

    def fill_card_details(self, card_derails=None):
        if not card_derails:
            card_derails = GetCreditsDataset.VALID_CARD_DETAILS
        self.base_actions.verify_expected_title(expected_title=Title.CARD_DETAILS)
        self.spa_payment.fill_field_card_number(card_derails[0])
        self.spa_payment.fill_field_expiry_date(card_derails[1])
        self.spa_payment.fill_field_card_holder(card_derails[2])
        self.spa_payment.fill_field_cvv(card_derails[3])

    def get_credit(self, amount: int):
        self.spa_payment.click_get_credit_btn()
        self.spa_payment.fill_field_certificates(amount)
        self.spa_payment.verify_total_price(str(amount * 25))
        self.spa_payment.click_btn_pay()

    def upload_group_of_labors(self, amount: int = 1, verify_info_popup: bool = False):
        self.csv_helper.prepare_csv_file(amount)
        self.add_group_of_labors(amount, verify_info_popup=verify_info_popup)
        self.spa_upload.verify_added_labors(amount)

    def upload_labor_with_previous_date_and_add_credits(self, amount: int = 1):
        self.spa_upload.visit()
        self.csv_helper.change_timestamp_to_previous_day()
        self.add_group_of_labors(amount)
        self.spa_upload.verify_added_labors(amount)
        self.spa_labors.visit()
        self.wait_until_no_data_available_disappear()
        self.base_actions.wait_spinners_to_disappear()
        self.spa_payment.visit()
        self.add_credit(amount)

    def add_group(self, amount: int = 1, status: str = ExamResult.PASSED, row_count=1, previous_day=None):
        added_labors = amount if status in [ExamResult.PASSED, ExamResult.PENDING] else 0
        if status == ExamResult.PASSED:
            if not previous_day:
                self.__pass_labor_flow_and_go_to_labors_tab(amount)
                return
            self.csv_helper.prepare_csv_file(amount, wrong_timestamp='previous')
        elif status == ExamResult.PENDING:
            self.csv_helper.prepare_csv_file(amount)
        elif status == ExamResult.FAILED:
            self.csv_helper.prepare_csv_file(amount, exam_score=1)
        elif status == ExamResult.REJECTED:
            self.csv_helper.prepare_csv_file(amount, wrong_timestamp='wrong')
        self.add_group_of_labors(amount)
        self.base_actions.wait_until_page_updates(self.spa_upload.verify_added_labors_multiple,
                                                  Title.UPLOADED_FILES,
                                                  row_count)
        self.spa_upload.verify_added_labors(added_labors)
        self.spa_labors.visit()
        self.wait_until_no_data_available_disappear()
        self.base_actions.wait_spinners_to_disappear()

    def create_certain_number_of_test_centers(self, amount):
        self.auth_api_actions.get_token()
        for _ in range(amount):
            self.admin_api_actions.create_tcenter(self.auth_api_actions.token)

    @staticmethod
    def __verify_counts_in_circles(counts, amount: int = 1):
        for status in ExamResult.LIST_ALL_EXAM_RESULTS:
            if status == ExamResult.ALL:
                BaseActions.verify_expected_result(counts[status], 4)
            else:
                BaseActions.verify_expected_result(counts[status], amount)

    def verify_all_count_on_labors_tab(self):
        self.add_group()
        self.spa_upload.visit()
        self.add_group(status=ExamResult.PENDING, row_count=2)
        self.spa_upload.visit()
        self.add_group(status=ExamResult.FAILED, row_count=3)
        self.spa_upload.visit()
        self.add_group(status=ExamResult.REJECTED, row_count=4)
        SPAActions.__verify_counts_in_circles(self.spa_labors.get_all_counts())

    def verify_total_amount_value(self, amount=1):
        for _ in range(PageNumbersDataset.PAGE_VALUES):
            self.csv_helper.prepare_csv_file(amount)
            self.add_group_of_labors(amount)
            self.spa_upload.verify_added_labors(amount)
        self.verify_active_next_btn()
        self.spa_upload.verify_search_result_value(str(PageNumbersDataset.PAGE_VALUES))

    def edit_and_verify_email(self, amount: int = 1):
        self.add_group(amount, ExamResult.PENDING)
        email = self.get_info_of_last_entry()[Labels.EMAIL]
        self.spa_labors.click_on_email_field()
        self.verify_popup_field_email(email='', key=Labels.EMAIL)
        self.spa_labors.click_on_email_field()
        self.verify_popup_field_email(email=email, key=Labels.EMAIL)

    # Labors

    def verify_field_labor_id(self, entry_info, key):
        self.spa_labors.fill_field_labor_id(entry_info[key])
        self.wait_until_no_data_available_disappear()
        self.base_actions.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_field_labor_name(self, entry_info, key):
        self.spa_labors.fill_field_labor_name(entry_info[key])
        self.wait_until_no_data_available_disappear()
        self.base_actions.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_field_passport_number(self, entry_info, key):
        self.spa_labors.fill_field_passport_number(entry_info[key])
        self.wait_until_no_data_available_disappear()
        self.base_actions.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_field_email(self, entry_info, key):
        self.spa_labors.fill_field_email(entry_info[key])
        self.wait_until_no_data_available_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_popup_field_email(self, email, key):
        self.spa_labors.fill_field_popup_email(email)
        self.spa_labors.click_on_save_btn()
        self.spa_labors.wait_until_popup_disappear()
        self.base_actions.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], email)

    def verify_category_list(self, entry_info, key):
        self.spa_labors.select_category_list(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_tc_list(self, entry_info, key):
        self.spa_labors.select_tc_list(BaseActions.make_lower_case_first_char_of_second_name(entry_info[key]))
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_view_exam_date(self, entry_info, key):
        self.spa_labors.select_view_exam_date(entry_info[key])
        self.spa_labors.wait_until_popup_disappear()
        self.base_actions.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_view_exam_results(self, entry_info, key):
        self.spa_labors.select_view_exam_results(entry_info[key])
        self.spa_labors.wait_until_popup_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    # Upload

    def verify_field_file_id(self, entry_info, key):
        self.spa_upload.fill_field_file_id(entry_info[key])
        self.spa_labors.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_upload_date(self, entry_info, key):
        self.spa_upload.select_upload_date(entry_info[key])
        self.spa_labors.wait_spinners_to_disappear()
        self.wait_until_no_data_available_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_field_number_of_passed_labors(self, entry_info, key):
        self.spa_upload.fill_field_number_of_passed_labors(entry_info[key])
        self.spa_labors.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_field_number_of_labors(self, entry_info, key):
        self.spa_upload.fill_field_number_of_labors(entry_info[key])
        self.spa_labors.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_filters_on_uploads_tab(self, amount=1):
        self.upload_group_of_labors(amount)
        self.base_actions.wait_spinners_to_disappear()
        entry_info = self.get_info_of_last_entry()
        keys = list(entry_info.keys())
        self.verify_field_file_id(entry_info, keys[0])
        self.verify_upload_date(entry_info, keys[1])
        self.verify_field_number_of_passed_labors(entry_info, keys[2])
        self.verify_field_number_of_labors(entry_info, keys[3])
        self.click_clear_filter_btn()
        self.spa_upload.verify_disabling_filters_fields()

    def verify_field_view_labor_id(self, entry_info, key):
        self.spa_upload.fill_field_view_labor_id(entry_info[key])
        self.spa_labors.wait_until_popup_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_field_view_labor_name(self, entry_info, key):
        self.spa_upload.fill_field_view_labor_name(entry_info[key])
        self.spa_labors.wait_until_popup_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_field_view_passport_number(self, entry_info, key):
        self.spa_upload.fill_field_view_passport_number(entry_info[key])
        self.spa_labors.wait_until_popup_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_upload_tc_list(self, entry_info, key):
        self.spa_upload.select_tc(BaseActions.make_lower_case_first_char_of_second_name(entry_info[key]))
        self.spa_labors.wait_until_popup_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_category(self, entry_info, key):
        self.spa_upload.select_view_category(entry_info[key])
        self.spa_labors.wait_until_popup_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_exam_date(self, entry_info, key):
        self.base_actions.wait_spinners_to_disappear()
        self.spa_upload.select_view_exam_date(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_exam_results(self, entry_info, key):
        self.spa_upload.select_view_exam_results(entry_info[key])
        self.base_actions.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    # Transaction History

    def verify_reference_number(self, entry_info, key):
        self.spa_transactions_history.fill_reference_number(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_amount(self, entry_info, key):
        self.spa_transactions_history.fill_amount(entry_info[key])
        self.base_actions.wait_spinners_to_disappear()
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_date(self, entry_info, key):
        self.base_actions.wait_spinners_to_disappear()
        self.spa_transactions_history.select_date(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_status(self, key):
        for status, value in TransactionStatuses.TRANSACTION_STATUSES_LIST.items():
            self.spa_transactions_history.select_status(status)
            self.base_actions.wait_spinners_to_disappear()
            actual_status = self.get_info_of_last_entry(date=True)[key]
            if value == TransactionStatuses.FAILED:
                actual_status = actual_status[:-1]
            BaseActions.verify_expected_result(actual_status, value)

    def verify_id_tcenters_tab(self, entry_info, key):
        self.spa_test_centers.fill_filter_id(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_name_tcenters_tab(self, entry_info, key):
        self.spa_test_centers.fill_filter_name(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_city_tcenters_tab(self, entry_info, key):
        self.spa_test_centers.fill_filter_city(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_test_center_owner(self, entry_info, key):
        self.spa_test_centers.fill_filter_test_center_owner(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_test_center_status(self, entry_info, key):
        self.spa_test_centers.select_filter_status(entry_info[key].lower())
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_id_reports_tab(self, entry_info, key):
        self.spa_reports.fill_id(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_group_no(self, entry_info, key):
        self.spa_reports.fill_group_no(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_amount_reports_tab(self, entry_info, key):
        self.spa_reports.fill_amount(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry()[key], entry_info[key])

    def verify_date_reports_tab(self, entry_info, key):
        self.spa_reports.select_date(entry_info[key])
        BaseActions.verify_expected_result(self.get_info_of_last_entry(date=True)[key], entry_info[key])

    def verify_transactions_statuses(self, amount=1):
        for state in TransactionState.TRANSACTION_STATE_LIST:
            count = TransactionState.TRANSACTION_STATE_LIST.index(state) + 1
            self.spa_payment.visit()
            self.pass_credit_flow(amount, state)
            self.spa_transactions_history.visit()
            self.base_actions.wait_spinners_to_disappear()
            self.base_actions.wait_until_page_updates(self.spa_upload.verify_added_labors_multiple,
                                                      Title.TRANSACTION_HISTORY,
                                                      count)
            payment_entry = self.get_info_of_last_entry()
            if state == TransactionState.SUCCESS:
                BaseActions.verify_expected_result(payment_entry[Labels.STATUS], TransactionStatuses.SUCCESS)
            elif state == TransactionState.PREPARED_CHECKOUT:
                BaseActions.verify_expected_result(payment_entry[Labels.STATUS],
                                                   TransactionStatuses.PREPARED_CHECKOUT)
            else:
                BaseActions.verify_expected_result(payment_entry[Labels.STATUS][:-1], TransactionStatuses.FAILED)

    def verify_filters_on_upload_files(self, tcenter=True, amount=1):
        self.upload_group_of_labors(amount)
        self.spa_upload.select_last_entry()
        self.base_actions.wait_spinners_to_disappear()
        entry_info = self.get_info_of_last_entry(date=True)
        keys = list(entry_info.keys())
        self.verify_field_view_labor_id(entry_info, keys[0])
        self.verify_field_view_labor_name(entry_info, keys[1])
        self.verify_field_view_passport_number(entry_info, keys[2])
        if not tcenter:
            self.verify_upload_tc_list(entry_info, keys[3])
        self.verify_category(entry_info, keys[4])
        self.verify_exam_date(entry_info, keys[6])
        self.base_actions.wait_spinners_to_disappear()
        self.verify_exam_results(entry_info, keys[7])
        self.click_clear_filter_btn()
        self.spa_upload.verify_disabling_filters_fields(entry=True)

    def verify_filters_on_transaction_history(self, amount=1):
        self.spa_payment.visit()
        for state in TransactionState.TRANSACTION_STATE_LIST:
            self.pass_credit_flow(amount, state)
            if state == TransactionState.SUCCESS:
                self.base_actions.verify_expected_title(Title.PAYMENT_CONFIRMATION)
            self.spa_payment.visit()
        self.spa_transactions_history.visit()
        self.base_actions.wait_spinners_to_disappear()
        entry_info = self.get_info_of_last_entry(date=True)
        keys = list(entry_info.keys())
        self.verify_reference_number(entry_info, keys[0])
        self.verify_amount(entry_info, keys[1])
        self.verify_date(entry_info, keys[2])
        self.base_actions.wait_spinners_to_disappear()
        self.verify_status(keys[3])
        self.click_clear_filter_btn()
        self.spa_transactions_history.verify_disabling_filters_fields()

    def verify_filters_on_labors_table(self, amount: int = 1, tcenter=True):
        self.add_group(amount)
        entry_info = self.get_info_of_last_entry()
        keys = list(entry_info.keys())
        self.verify_field_labor_id(entry_info, keys[0])
        self.verify_field_labor_name(entry_info, keys[1])
        self.verify_field_passport_number(entry_info, keys[2])
        self.verify_field_email(entry_info, keys[3])
        self.verify_category_list(entry_info, keys[4])
        if tcenter:
            self.verify_view_exam_date(entry_info, keys[6])
            self.verify_view_exam_results(entry_info, keys[7])
        else:
            self.verify_tc_list(entry_info, keys[5])
            self.verify_view_exam_date(entry_info, keys[6])
            self.verify_view_exam_results(entry_info, keys[7])
        self.click_clear_filter_btn()
        self.spa_labors.verify_disabling_filters_fields()

    def verify_pagination_and_search_result_value(self, amount: int = 11):
        for _ in range(amount):
            self.upload_group_of_labors()
        self.spa_labors.visit()
        self.base_actions.wait_spinners_to_disappear()
        self.verify_active_next_btn()
        self.spa_upload.verify_search_result_value(str(amount))

    def verify_validation_edit_email_on_labors_tab(self, status: str = ExamResult.PASSED):
        self.add_group(status=status)
        self.spa_labors.click_on_email_field()
        for wrong_email in EditEmailDataset.INVALID_EMAIL:
            self.spa_labors.fill_field_popup_email(wrong_email)
            self.base_actions.verify_message(ErrorMessage.POPUP_EMAIL_FIELD)

    def verify_counts_on_labors_tab(self, exam_result: str, amount: int = 1):
        BaseActions.verify_expected_result(self.get_info_of_last_entry()['Exam Result'], exam_result)
        BaseActions.verify_expected_result(self.spa_labors.get_count(exam_result), amount)

    def fill_test_center_form(self, multiple_categories=False, warning=False, is_legislator=True):
        self.account_tcenter = ModelBuilder.build_random_account()
        tc_name = self.admin_api_actions.tcenter_account.en_name if warning else self.account_tcenter.en_name
        self.spa_test_centers.fill_tc_name(tc_name)
        self.spa_test_centers.fill_phone_number(self.account_tcenter.sub_number)
        if multiple_categories:
            self.spa_test_centers.select_all_categories()
        else:
            self.spa_test_centers.select_category(self.account_tcenter.category)
        if is_legislator:
            owner_name = self.admin_api_actions.tcenter_account.contact_name if warning else \
                self.account_tcenter.contact_name
            self.spa_test_centers.fill_owner_name(owner_name)
            email = self.admin_api_actions.tcenter_account.email if warning else self.account_tcenter.email
            self.spa_test_centers.fill_email(email)
        self.spa_test_centers.fill_tc_city(self.account_tcenter.city)
        self.spa_test_centers.fill_street_name(self.account_tcenter.address)
        self.spa_test_centers.fill_postal_code(self.account_tcenter.postal_code)

    def verify_upload_csv_file_without_selected_category_and_tcenter(self, tcenter=True):
        self.spa_upload.click_add_group_btn()
        warning_msg = WarningMessage.CHOOSE_FILE_BTN if tcenter else WarningMessage.CHOOSE_FILE_BTN.format('not')
        assert self.spa_upload.is_choose_file_btn_disabled, warning_msg
        self.spa_upload.select_tcenter_list(self.tcenter_name)
        assert self.spa_upload.is_choose_file_btn_disabled, warning_msg
        self.spa_upload.select_category_list(ModelBuilder.CATEGORY)
        assert not self.spa_upload.is_choose_file_btn_disabled(), WarningMessage.CHOOSE_FILE_BTN
        self.spa_upload.click_cancel_btn()

    def clear_all_fields(self, is_legislator=False):
        self.spa_test_centers.fill_tc_name('')
        self.spa_test_centers.fill_phone_number('')
        self.spa_test_centers.unselect_category()
        if is_legislator:
            self.spa_test_centers.fill_owner_name('')
            self.spa_test_centers.fill_email('')
        self.spa_test_centers.fill_tc_city('')
        self.spa_test_centers.fill_street_name('')
        self.spa_test_centers.fill_postal_code('')

    def verify_empty_fields(self, is_legislator=False):
        self.spa_test_centers.verify_empty_name_field()
        self.spa_test_centers.verify_empty_contact_number_field()
        self.spa_test_centers.verify_empty_category_list()
        if is_legislator:
            self.spa_test_centers.verify_empty_owner_name_field()
            self.spa_test_centers.verify_empty_email_field()
        self.spa_test_centers.verify_empty_city_field()
        self.spa_test_centers.verify_empty_street_field()

    @staticmethod
    def __fill_and_verify_field(data, action, btn_action, verification):
        for value in data:
            action(value)
            if btn_action:
                btn_action()
            verification()

    def verify_wrong_data_on_edit_form(self, is_add_btn=True, is_legislator=True):
        btn_action = self.spa_test_centers.click_add_btn if is_add_btn else self.spa_test_centers.click_edit_btn
        SPAActions.__fill_and_verify_field(WrongTestCenterDataset.OFFICIAL_CONTACT_NUMBER,
                                           self.spa_test_centers.fill_phone_number,
                                           btn_action,
                                           self.spa_test_centers.verify_warning_digits_only_contact_number)
        if is_legislator:
            SPAActions.__fill_and_verify_field(WrongTestCenterDataset.EMAIL,
                                               self.spa_test_centers.fill_email,
                                               btn_action,
                                               self.spa_test_centers.verify_warning_invalid_email)
        SPAActions.__fill_and_verify_field(WrongTestCenterDataset.CITY,
                                           self.spa_test_centers.fill_tc_city,
                                           btn_action,
                                           self.spa_test_centers.verify_warning_en_chars_only_city)
        SPAActions.__fill_and_verify_field(WrongTestCenterDataset.POSTAL_CODE,
                                           self.spa_test_centers.fill_postal_code,
                                           btn_action,
                                           self.spa_test_centers.verify_warning_digits_only_postal_code)

    def __verify_account_information(self, account, is_logo=True):
        logo = 'Yes' if is_logo else 'No'
        # TODO: Add verification for logo image
        assert self.spa_account.get_show_logo() == logo
        assert self.spa_account.get_address() == account.address
        assert self.spa_account.get_postal_code() == str(account.postal_code)
        assert self.spa_account.get_full_name() == account.contact_name
        assert self.spa_account.get_phone_number() == account.phone_number
        assert self.spa_account.get_email() == account.email

    def verify_view_account_information(self, account):
        self.spa_account.visit()
        self.base_actions.verify_expected_title(Title.SPA_ACCOUNT_INFORMATION)
        self.wait_spinners_to_disappear()
        self.__verify_account_information(account, is_logo=False)
        self.spa_account.click_edit_btn()
        assert not self.spa_account.get_show_logo(is_edit=True)
        assert self.spa_account.get_address(is_edit=True) == account.address
        assert self.spa_account.get_postal_code(is_edit=True) == str(account.postal_code)
        assert self.spa_account.get_full_name(is_edit=True) == account.contact_name
        assert self.spa_account.get_phone_number(is_edit=True) == account.sub_number
        assert self.spa_account.get_email(is_edit=True) == account.email

    def __go_to_edit_account_form(self):
        self.spa_account.visit()
        self.base_actions.verify_expected_title(Title.SPA_ACCOUNT_INFORMATION)
        self.wait_spinners_to_disappear()
        self.spa_account.click_edit_btn()

    def verify_edit_account_information_with_valid_data(self):
        self.__go_to_edit_account_form()
        account = ModelBuilder.build_random_account()
        self.spa_account.upload_logo_file(account.logo)
        self.spa_account.select_show_logo_toggle()
        self.spa_account.fill_address(account.address)
        self.spa_account.fill_postal_code(account.postal_code)
        self.spa_account.fill_full_name(account.contact_name)
        self.spa_account.fill_phone_number(account.sub_number)
        self.spa_account.fill_email(account.email)
        self.spa_account.click_save_btn()
        self.__verify_account_information(account)

    def verify_edit_account_information_with_invalid_data(self):
        self.__go_to_edit_account_form()
        SPAActions.__fill_and_verify_field(WrongTestCenterDataset.POSTAL_CODE,
                                           self.spa_account.fill_postal_code,
                                           False,
                                           self.spa_account.verify_warning_digits_only_postal_code)
        SPAActions.__fill_and_verify_field(WrongTestCenterDataset.CONTACT_INFORMATION,
                                           self.spa_account.fill_full_name,
                                           False,
                                           self.spa_account.verify_warning_en_chars_only_name)
        # TODO: Uncomment after fix issue with warning message
        # SPAActions.__fill_and_verify_field(WrongTestCenterDataset.OFFICIAL_CONTACT_NUMBER,
        #                                    self.spa_account.fill_phone_number,
        #                                    False,
        #                                    self.spa_account.verify_warning_digits_only_contact_number)
        SPAActions.__fill_and_verify_field(WrongTestCenterDataset.EMAIL,
                                           self.spa_account.fill_email,
                                           False,
                                           self.spa_account.verify_warning_invalid_email_field)

    def verify_edit_account_information_with_empty_data_and_duplicate_email(self):
        self.__go_to_edit_account_form()
        self.spa_account.upload_logo_file(self.admin_api_actions.legislator_account.logo)
        self.spa_account.fill_email(self.admin_api_actions.tcenter_account.email)
        self.spa_account.click_save_btn()
        self.spa_account.verify_warning_duplicate_email()
        self.spa_account.fill_address('')
        self.spa_account.fill_postal_code('')
        self.spa_account.fill_full_name('')
        self.spa_account.fill_phone_number('')
        self.spa_account.fill_email('')
        self.spa_account.verify_btn_edit_is_disabled()

    def verify_view_change_password_form(self):
        self.click_on_profile_menu().click_change_password()
        self.base_actions.verify_expected_title(Title.SPA_CHANGE_PASSWORD)
        self.spa_change_password.click_back_btn()
        self.base_actions.verify_expected_title(Title.UPLOADED_FILES)

    def verify_change_password(self):
        self.spa_change_password.visit()
        self.spa_change_password.fill_current_password(UserInfo.DEFAULT_PASSWORD)
        self.spa_change_password.fill_new_password(UserInfo.CHANGED_PASSWORD)
        self.spa_change_password.fill_confirmed_new_password(UserInfo.CHANGED_PASSWORD)
        self.spa_change_password.click_continue_btn()
        self.base_actions.verify_expected_title(Title.SPA_SIGN_IN)

    def verify_changing_password_with_invalid_new_password(self):
        self.spa_change_password.visit()
        for passwords in ChangePasswordDataset.WRONG_PASSWORDS:
            self.spa_change_password.fill_current_password(passwords[0])
            self.spa_change_password.fill_new_password(passwords[1])
            self.spa_change_password.fill_confirmed_new_password(passwords[2])
            self.spa_change_password.verify_is_change_button_disabled()

    def verify_change_password_with_invalid_password(self):
        self.spa_change_password.visit()
        for description, password in ChangePasswordDataset.LIST_INVALID_PASSWORDS.items():
            self.spa_change_password.fill_current_password(password[0])
            self.spa_change_password.fill_new_password(password[1])
            self.spa_change_password.fill_confirmed_new_password(password[2])
            self.spa_change_password.click_continue_btn()
            if description == ChangePasswordDataset.INVALID_CURRENT_PASSWORD:
                self.spa_change_password.verify_warning_current_password()
            elif description == ChangePasswordDataset.CURRENT_PASSWORD:
                self.spa_change_password.verify_warning_new_password()
            elif description == ChangePasswordDataset.MISMATCH_NEW_PASSWORD:
                self.spa_change_password.verify_warning_new_password()
                self.spa_change_password.verify_warning_confirm_new_password()
            else:
                self.spa_change_password.verify_warning_confirm_new_password()

    def verify_download_csv_sample(self):
        self.spa_upload.click_add_group_btn()
        self.base_actions.verify_expected_title(Title.ADD_GROUP)
        self.spa_upload.click_download_csv_sample()
        downloaded_file = self.file_helper.get_temp_files()[0]
        self.file_helper.check_compatibility_files(DirPath.CSV, downloaded_file)

    def __verify_certificate_info(self):
        self.file_helper.unzip_temp_file()
        pdf_text = list(self.file_helper.read_pdf_file())
        year = datetime.date.today().year + 5
        date = datetime.date.today().replace(year).strftime(DateType.DATE_SEP_DASH)
        passport_number = self.csv_helper.get_passport_number
        BaseActions.verify_expected_result('Name', pdf_text, True)
        BaseActions.verify_expected_result(date, pdf_text, True)
        BaseActions.verify_expected_result(passport_number, pdf_text, True)

    def __verify_report_info(self):
        pdf_text = list(self.file_helper.read_pdf_file())
        date = datetime.date.today().strftime(DateType.DATE_SEP_SLASH)
        for value in ['1 Credits', '25.0 USD', date, 'successful']:
            BaseActions.verify_expected_result(value, pdf_text, True)

    def __is_view_payment(self, is_view_payment):
        if is_view_payment:
            self.spa_reports.click_icon_action()
        self.spa_reports.click_icon_report()

    def __is_report_tab(self, is_certificate, is_view_payment):
        self.spa_reports.visit()
        if is_certificate:
            self.spa_reports.click_icon_certificate()
        else:
            self.__is_view_payment(is_view_payment)

    def verify_download_certificate_report(self, is_certificate=True, is_reports_tab=False, is_view_payment=False):
        self.pass_labor_flow()
        self.base_actions.verify_message(SuccessMessage.CERTIFICATE)
        if is_reports_tab:
            self.__is_report_tab(is_certificate, is_view_payment)
        else:
            self.spa_payment.click_btn_download_certificate()
        if is_certificate:
            self.__verify_certificate_info()
        else:
            self.__verify_report_info()

    def verify_download_invoice(self, is_transaction_history=False, is_view_payment=False, is_zip_file=False):
        self.pass_labor_flow()
        self.base_actions.verify_message(SuccessMessage.CERTIFICATE)
        if is_transaction_history:
            self.spa_transactions_history.visit()
            self.spa_transactions_history.click_invoice_icon()
        elif is_view_payment:
            self.spa_transactions_history.visit()
            self.spa_transactions_history.click_view_item()
            self.spa_payment.click_icon_invoice()
        else:
            self.spa_payment.click_btn_download_certificate()
        if is_zip_file:
            self.file_helper.unzip_temp_file()
        pdf_text = list(self.file_helper.read_pdf_file())
        date_month_name = datetime.date.today().strftime(DateType.DATE_SEP_SPACE)
        date = datetime.date.today().strftime(DateType.DATE_SEP_SLASH)
        for value in ['1 Certificates', '25.0 USD', 'Total Value: 25.0', f'Issued Date: {date}', f' {date_month_name}']:
            BaseActions.verify_expected_result(value, pdf_text, True)
