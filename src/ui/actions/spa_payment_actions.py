import pytest

from src.ui.actions.spa_actions import SPAActions
from test_data.constants import TransactionState, Title, ExamResult
from test_data.dataset import GetCreditsDataset
from test_data.validation_message import WarningMessage, ErrorMessage, SuccessMessage


class SPAPaymentActions(SPAActions):
    def __verify_payment_entry(self, uploaded_entry: dict, entry: dict):
        if uploaded_entry[self.file_id] != entry[self.file_id]:
            pytest.fail(f"Payment entry with id {entry[self.file_id]} doesn't exist")

    def __issue_certificate(self):
        self.spa_payment.click_issue_btn()
        self.spa_payment.click_confirm_btn()
        self.spa_payment.click_switch_icon()
        self.spa_payment.click_confirm_btn()

    def upload_group_and_add_credits(self, amount: int):
        self.add_group(amount, ExamResult.PENDING)
        self.spa_payment.visit()
        self.add_credit(amount)

    def verify_ability_to_add_credits(self, amount=1):
        self.spa_payment.visit()
        for state in TransactionState.TRANSACTION_STATE_LIST[:-1]:
            self.pass_credit_flow(amount, state)
            title = Title.PAYMENT_CONFIRMATION if state == TransactionState.SUCCESS else Title.PAYMENT
            self.base_actions.verify_expected_title(title)
            self.spa_payment.visit()
            self.spa_payment.verify_credits_counter(amount)

    def verify_error_message_duplicate_payment(self, amount: int):
        self.add_group(amount)
        self.spa_upload.visit()
        self.add_group(amount, previous_day=True)
        self.spa_upload.visit()
        uploaded_entry = self.get_info_of_last_entry()
        self.spa_payment.visit()
        self.add_credit(amount)
        payment_entry = self.get_info_of_last_entry()
        self.__verify_payment_entry(uploaded_entry, payment_entry)
        self.spa_payment.select_last_entry()
        self.spa_payment.click_issue_btn()
        self.spa_payment.click_confirm_btn()
        self.base_actions.verify_message(WarningMessage.ACTIVE_CERTIFICATE)
        self.spa_payment.confirm_btn_is_disabled()
        self.spa_payment.click_icon_bin()
        self.verify_no_data_available()
        self.spa_payment.click_btn_cancel()
        self.__issue_certificate()

    def verify_input_fields_on_add_credits(self):
        self.spa_payment.visit()
        self.spa_payment.click_get_credit_btn()
        for item in GetCreditsDataset.INVALID_CERTIFICATES:
            self.spa_payment.fill_field_certificates(item)
            self.spa_payment.verify_pay_now_btn_is_disabled()
        self.spa_payment.fill_field_certificates(1)
        self.spa_payment.click_btn_pay()
        for card_details in GetCreditsDataset.INVALID_CARD_DETAILS:
            self.fill_card_details(card_details)
            self.base_actions.verify_message(ErrorMessage.CARD_NUMBER)
            self.base_actions.verify_message(ErrorMessage.CARD_EXPIRY_DATE)
            self.base_actions.verify_message(ErrorMessage.CARD_CVV)
            self.base_actions.verify_message(ErrorMessage.CARD_HOLDER)
            self.spa_payment.verify_btn_transaction_pay_is_disabled()

    def verify_payment_information(self):
        self.pass_labor_flow()
        self.base_actions.verify_message(SuccessMessage.CERTIFICATE)
        # TODO: Add possibility to get Reference Number for checking on ui
        # self.spa_payment.verify_payment_reference_number()
        self.spa_payment.verify_number_of_certificates()
        self.spa_payment.verify_price_per_certificate()
        self.spa_payment.verify_total_amount()
        self.spa_payment.verify_grand_total()
        # TODO: Add possibility to get Reference Number for checking on ui
        # self.spa_payment.verify_transaction_reference_number()
        self.spa_payment.verify_amount()
        self.spa_payment.verify_date()
