import allure
from selene import command
from selene.support.conditions import be, have
from selene.support.shared.jquery_style import s

from helpers.decorators import for_all_methods
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage


class SPAReportsLocators:
    FIELD_ID = "div[data-label='ID'] input"
    GROUP_NO = "div[data-label='Group No'] input"
    FIELD_AMOUNT = "div[data-label='Amount'] input"
    FIELD_DATE = "div[data-label='Date'] input"
    ICON_CERTIFICATES = "td[data-label='Certificates'] a"
    ICON_REPORT = "td[data-label='Report'] a"
    ACTIONS = "td[data-label='Actions'] a"

    BTN_CHECK_VALIDITY = '.check-validity-link'
    FIELD_PASSPORT_NUMBER = '#passport'
    FIELD_CERTIFICATE_SERIAL_NUMBER = '#certificate'
    BTN_VERIFY = '.btn--border-primary'
    FIELD_STATUS = "td[data-label='Status'] span"
    MSG_VALID_CERTIFICATE = '.results__message'
    RESULT_PASSPORT_NUMBER = '.results__heading + div div:nth-child(2) div'
    RESULT_CERTIFICATE_SERIAL_NUMBER = '.results__heading + div div:nth-child(3) div'
    LABOR_NAME = "//div[.='Labor Name']/following-sibling::div"
    PASSPORT_NUMBER = "//div[@class='results']//div[.='Passport Number']/following-sibling::div"


@for_all_methods(allure.step)
class SPAReportsPage(SPAReportsLocators, BasePage):  # pylint: disable=R0904

    def __init__(self):
        super().__init__()
        self.page_url = 'reports'
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)
        # TODO: Remove after fix wrong redirection
        s('li:nth-child(6) > a > span').click()

    def click_check_validity_btn(self):
        s(self.BTN_CHECK_VALIDITY).should(be.visible).click()

    def click_verify_btn(self):
        s(self.BTN_VERIFY).should(be.visible).click()

    def click_icon_certificate(self):
        s(self.ICON_CERTIFICATES).should(be.visible).click()

    def click_icon_report(self):
        s(self.ICON_REPORT).should(be.visible).click()

    def click_icon_action(self):
        s(self.ACTIONS).should(be.visible).click()

    def verify_btn_verify_is_disabled(self):
        s(self.BTN_VERIFY).should(be.disabled)

    def fill_id(self, text):
        s(self.FIELD_ID).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_group_no(self, text):
        s(self.GROUP_NO).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_amount(self, text):
        s(self.FIELD_AMOUNT).should(be.visible).perform(command.js.set_value("")).type(text)

    def select_date(self, text):
        s(self.FIELD_DATE).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_passport_number(self, text):
        s(self.FIELD_PASSPORT_NUMBER).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_certificate_serial_number(self, text):
        s(self.FIELD_CERTIFICATE_SERIAL_NUMBER).should(be.visible).perform(command.js.set_value("")).type(text)

    def verify_success_status(self):
        s(self.FIELD_STATUS).should(be.visible).should(have.exact_text('Success'))

    def verify_disabling_filters_fields(self):
        filter_locators = [
            self.FIELD_ID,
            self.GROUP_NO,
            self.FIELD_AMOUNT,
            self.FIELD_DATE
        ]
        for locator in filter_locators:
            BasePage.is_disabled(locator)

    def verify_msg_certificate(self, text: str):
        s(self.MSG_VALID_CERTIFICATE).should(be.visible).should(have.text(text))

    def verify_results_passport_number(self, expected_passport_number):
        s(self.RESULT_PASSPORT_NUMBER).should(be.visible).should(have.text(expected_passport_number))

    def verify_result_certificate_serial_number(self, expected_number):
        s(self.RESULT_CERTIFICATE_SERIAL_NUMBER).should(be.visible).should(have.text(expected_number))

    def verify_labor_name(self):
        s(self.LABOR_NAME).should(be.visible).should(have.exact_text('Name'))

    def verify_passport_number(self, text: str):
        s(self.PASSPORT_NUMBER).should(be.visible).should(have.exact_text(text))
