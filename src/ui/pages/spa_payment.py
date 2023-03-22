from time import gmtime, strftime

import allure
from selene import command, have
from selene.support.conditions import be
from selene.support.shared.jquery_style import s

from helpers.decorators import for_all_methods
from src.ui.actions.driver_actions import DriverActions
from test_data.constants import Credits


class SPAPaymentLocators:
    BTN_TRANSACTION_HISTORY = '.btn--border-primary'
    BTN_ISSUE = "//button[.='Issue']"
    BTN_GET_CREDIT = "//button[.='Get Credit']"
    BTN_CONFIRM = "//button[.='Confirm']"
    BTN_CANCEL = "//button[.='Cancel']"
    CREDITS_COUNTER = '.green'
    NUMBER_OF_LABORS = '.dark'
    TOTAL_AMOUNT = '.blue'

    FIELD_FILE_ID = 'th:nth-child(1)  .table-main__input'
    PICKER_UPLOAD_DATE = 'th:nth-child(2)  .table-main__input'
    FIELD_NUMBER_OF_PASSED_LABORS = 'th:nth-child(3)  .table-main__input'
    FIELD_TOTAL_LABORS = 'th:nth-child(4)  .table-main__input'
    FIELD_AMOUNT = 'th:nth-child(5)  .table-main__input'
    ACTION_ICON_SELECT = '.toggle-button'
    ENTRY_OF_PAYMENT_TABLE = 'tr:nth-child(1) td'
    BUTTON_PLUS_OF_LAST_ENTRY = 'tr:nth-child(1) td .toggle-button'
    UNSELECT_ALL = '.table-main__mobile-filter-wrap .mb-2'

    # GET CREDIT
    FIELD_CERTIFICATES = '#certificates'
    TOTAL = '.payment-form__total-wrap div'
    BTN_PAY = "//button[.='Pay']"

    # CARD DETAILS
    IFRAME_NUMBER = 'card.number'
    IFRAME_CVV = 'card.cvv'
    FIELD_CARD_NUMBER = "//input[@name='card.number']"
    FIELD_EXPIRY_DATE = '.wpwl-control-expiry'
    FIELD_CVV = "//input[@name='card.cvv']"
    FIELD_CARD_HOLDER = "//input[@name='card.holder']"
    BTN_PAY_NOW = '.custom-pay-btn'
    WARNING_MSG_CARD_NUMBER = '.wpwl-hint-cardNumberError'
    WARNING_MSG_EXPIRY_DATE = '.wpwl-hint-expiryMonthError'
    WARNING_MSG_CVV = '.wpwl-hint-cvvError'
    WARNING_MSG_CARD_HOLDER = '.wpwl-hint-cardHolderError'

    # TRANSACTION STATE
    DROPDOWN_TRANSACTION_STATE = "select[name='returnCode']"
    BTN_TRANSACTION_PAY = 'input[name]'

    # POPUP
    ICON_BIN = '.actions-link'
    ICON_SWITCH = '.switch'

    # PAYMENT CONFIRMATION
    PAYMENT_REFERENCE_NUMBER = ".table-main__table td[data-label='Reference Number']"
    NUMBER_OF_CERTIFICATES = "td[data-label='Number Of Certificates']"
    PRICE_PER_CERTIFICATE = "td[data-label='Price Per Certificate']"
    PAYMENT_TOTAL_AMOUNT = "td[data-label='Total Amount']"
    GRAND_TOTAL = '.files-amount-total__sum'

    # TRANSACTION INFORMATION
    TRANSACTION_REFERENCE_NUMBER = ".table-files td[data-label='Reference Number']"
    AMOUNT = "td[data-label='Amount']"
    DATE = "td[data-label='Date']"
    ICON_INVOICE = "td[data-label='Invoice'] a"

    # CERTIFICATES
    BTN_DOWNLOAD = "//button[.='Download']"
    BTN_SEND_EMAIL = "//button[.='Send Email']"


@for_all_methods(allure.step)
class SPAPaymentPage(SPAPaymentLocators):  # pylint: disable=R0904

    def __init__(self):
        super().__init__()
        self.page_url = 'payment'
        self.driver_actions = DriverActions()

    def visit(self, url=None):
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)

    def click_transaction_history_btn(self):
        s(self.BTN_TRANSACTION_HISTORY).should(be.clickable).click()

    def click_issue_btn(self):
        s(self.BTN_ISSUE).should(be.clickable).click()

    def click_get_credit_btn(self):
        s(self.BTN_GET_CREDIT).should(be.clickable).click()

    def click_confirm_btn(self):
        s(self.BTN_CONFIRM).should(be.clickable).click()

    def verify_pay_now_btn_is_disabled(self):
        s(self.BTN_GET_CREDIT).should(be.disabled)

    def select_last_entry(self):
        s(self.BUTTON_PLUS_OF_LAST_ENTRY).with_(timeout=3).should(be.clickable).click()

    # GET CREDIT

    def fill_field_certificates(self, text: int):
        s(self.FIELD_CERTIFICATES).perform(command.js.set_value("")).type(text)

    def verify_total_price(self, amount: str):
        s(self.TOTAL).should(have.exact_text(amount + '$'))

    def click_btn_pay(self):
        s(self.BTN_PAY).should(be.clickable).click()

    # CARD DETAILS

    def fill_field_card_number(self, text: str):
        self.driver_actions.switch_to_iframe(self.IFRAME_NUMBER)
        s(self.FIELD_CARD_NUMBER).perform(command.js.set_value("")).type(text)
        self.driver_actions.exit_iframe()

    def fill_field_expiry_date(self, text: str):
        s(self.FIELD_EXPIRY_DATE).perform(command.js.set_value("")).type(text)

    def fill_field_cvv(self, text: str):
        self.driver_actions.switch_to_iframe(self.IFRAME_CVV)
        s(self.FIELD_CVV).perform(command.js.set_value("")).type(text).press_tab()
        self.driver_actions.exit_iframe()

    def fill_field_card_holder(self, text: str):
        s(self.FIELD_CARD_HOLDER).perform(command.js.set_value("")).type(text)

    def click_btn_pay_now(self):
        s(self.BTN_PAY_NOW).should(be.clickable).click()

    def verify_btn_transaction_pay_is_disabled(self):
        s(self.BTN_PAY_NOW).should(be.disabled)

    # TRANSACTION_STATE

    def select_dropdown_transaction_state(self, text: str):
        s(self.DROPDOWN_TRANSACTION_STATE).type(text)

    def click_btn_transaction_pay(self):
        s(self.BTN_TRANSACTION_PAY).should(be.clickable).click()

    def confirm_btn_is_disabled(self):
        s(self.BTN_CONFIRM).should(be.disabled)

    def click_icon_bin(self):
        s(self.ICON_BIN).should(be.clickable).click()

    def click_btn_cancel(self):
        s(self.BTN_CANCEL).should(be.clickable).click()

    def click_switch_icon(self):
        s(self.ICON_SWITCH).should(be.visible).click()

    def verify_credits_counter(self, amount: int = 1):
        s(self.CREDITS_COUNTER).should(have.exact_text(str(amount)))

    def verify_number_of_labors(self, amount: int = 1):
        s(self.NUMBER_OF_LABORS).should(have.exact_text(str(amount)))

    def verify_total_amount(self, amount: int = 1):
        s(self.TOTAL_AMOUNT).should(have.exact_text(str(amount * Credits.AMOUNT) + '$'))

    # PAYMENT CONFIRMATION
    def verify_payment_reference_number(self, text: str):
        s(self.PAYMENT_REFERENCE_NUMBER).should(have.exact_text(text))

    def verify_number_of_certificates(self, amount: int = 1):
        s(self.NUMBER_OF_CERTIFICATES).should(have.exact_text(str(amount)))

    def verify_price_per_certificate(self, amount: int = 1):
        s(self.PRICE_PER_CERTIFICATE).should(have.exact_text(str(amount * Credits.AMOUNT) + '$'))

    def verify_payment_total_amount(self, amount: int = 1):
        s(self.PAYMENT_TOTAL_AMOUNT).should(have.exact_text(str(amount * Credits.AMOUNT) + '.00$'))

    def verify_grand_total(self, amount: int = 1):
        s(self.GRAND_TOTAL).should(have.exact_text(str(amount * Credits.AMOUNT) + '.00$'))

    # TRANSACTION INFORMATION
    def verify_transaction_reference_number(self, text: str):
        s(self.TRANSACTION_REFERENCE_NUMBER).should(have.exact_text(text))

    def verify_amount(self, amount: int = 1):
        s(self.AMOUNT).should(have.exact_text(str(amount * Credits.AMOUNT) + '$'))

    def verify_date(self, date: str = ''):
        if not date:
            date = strftime("%d-%m-%y", gmtime())
        s(self.DATE).should(have.text(date))

    def click_icon_invoice(self):
        s(self.ICON_INVOICE).should(be.clickable).click()

    # PAYMENT
    def click_btn_download_certificate(self):
        s(self.BTN_DOWNLOAD).should(be.clickable).click()

    def click_btn_send_email(self):
        s(self.BTN_SEND_EMAIL).should(be.clickable).click()
