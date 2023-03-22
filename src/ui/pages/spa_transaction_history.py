import allure
from selene import command, have
from selene.support.conditions import be
from selene.support.shared.jquery_style import s, ss

from helpers.decorators import for_all_methods
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage


class SPATransactionHistoryLocators:
    FIELD_REFERENCE_NUMBER = "div[data-label='Reference Number'] input"
    FIELD_AMOUNT = "div[data-label='Amount'] input"
    FIELD_DATE = "div[data-label='Date'] input"
    FIELD_STATUS = "div[data-label='Status'] select"
    ICON_INVOICE = "td[data-label='Invoice'] a"
    ACTIONS = "td[data-label='Actions'] a"


@for_all_methods(allure.step)
class SPATransactionHistoryPage(SPATransactionHistoryLocators, BasePage):  # pylint: disable=R0904

    def __init__(self):
        super().__init__()
        self.page_url = 'history'
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)

    def fill_reference_number(self, text):
        s(self.FIELD_REFERENCE_NUMBER).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_amount(self, text):
        s(self.FIELD_AMOUNT).should(be.visible).perform(command.js.set_value("")).type(text)

    def select_date(self, text):
        s(self.FIELD_DATE).should(be.visible).perform(command.js.set_value("")).type(text)

    def select_status(self, text):
        s(self.FIELD_STATUS).all('option').element_by(have.exact_text(text)).click()

    def verify_disabling_filters_fields(self):
        filter_locators = [
            self.FIELD_REFERENCE_NUMBER,
            self.FIELD_AMOUNT,
            self.FIELD_DATE,
            self.FIELD_STATUS
        ]
        for locator in filter_locators:
            BasePage.is_disabled(locator)

    def click_invoice_icon(self):
        ss(self.ICON_INVOICE).first.should(be.visible).click()

    def click_view_item(self):
        ss(self.ACTIONS).first.should(be.visible).click()
