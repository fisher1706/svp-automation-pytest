import allure
from selene import command, have, query
from selene.support.conditions import be
from selene.support.shared.jquery_style import s
from selenium.webdriver.common.keys import Keys

from helpers.decorators import for_all_methods
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage
from test_data.constants import ExamResult


class SPALaborsLocators:
    FIELD_NATIONAL_ID = "div[data-label='National ID'] input"
    FIELD_LABOR_NAME = "div[data-label='Labor Name'] input"
    FIELD_PASSPORT_NUMBER = "div[data-label='Passport Number'] input"
    FIELD_EMAIL = "div[data-label='Email'] input"
    DROPDOWN_CATEGORY = "div[data-label='Category'] select"
    DROPDOWN_TCENTER = "div[data-label='Test Centers'] select"
    DROPDOWN_EXAM_DATE = "div[data-label='Exam Date'] input"
    DROPDOWN_EXAM_RESULT = "div[data-label='Exam Result'] select"

    EDIT_EMAIL_FIELD = 'tr:nth-child(1) > td:nth-child(4)'
    FIELD_POPUP_EMAIL = '#email'
    BTN_SAVE = '.btn--primary'

    ENTRY_OF_LABORS_TABLE = '.table tbody tr'
    ALL = '.green'
    PASS = '.dark'
    FAIL = '.blue'
    PENDING = '.orange'
    # uncomment after clarifying test with expired status
    # EXPIRED = '.pink'
    REJECTED = '.grey'
    LIST_COUNT_LOCATORS = [PASS, FAIL, PENDING, REJECTED]
    LIST_ALL_COUNT_LOCATORS = [ALL, PASS, FAIL, PENDING, REJECTED]


@for_all_methods(allure.step)
class SPALaborsPage(SPALaborsLocators, BasePage):

    def __init__(self):
        super().__init__()
        self.page_url = 'labors-list'
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)
        # TODO: Remove after fix wrong redirection
        s('li:nth-child(2) > a > span').click()

    def get_count(self, status):
        for circle, locator in zip(ExamResult.LIST_EXAM_RESULTS, self.LIST_COUNT_LOCATORS):
            if circle == status:
                return int(s(locator).get(query.text))
        return None

    def get_all_counts(self):
        counts = {}
        for circle, locator in zip(ExamResult.LIST_ALL_EXAM_RESULTS, self.LIST_ALL_COUNT_LOCATORS):
            counts[circle] = int(s(locator).get(query.text))
        return counts

    # Filters

    def fill_field_labor_id(self, text: str):
        s(self.FIELD_NATIONAL_ID).perform(command.js.set_value("")).type(text)

    def fill_field_labor_name(self, date: str):
        s(self.FIELD_LABOR_NAME).perform(command.js.set_value("")).type(date)

    def fill_field_passport_number(self, text: str):
        s(self.FIELD_PASSPORT_NUMBER).perform(command.js.set_value("")).type(text)

    def fill_field_email(self, text: str):
        s(self.FIELD_EMAIL).perform(command.js.set_value("")).type(text)

    def select_category_list(self, text: str):
        s(self.DROPDOWN_CATEGORY).all('option').element_by(have.exact_text(text)).click()

    def select_tc_list(self, text: str):
        s(self.DROPDOWN_TCENTER).all('option').element_by(have.text(text)).click()

    def select_view_exam_date(self, exam_date: str):
        s(self.DROPDOWN_EXAM_DATE).perform(command.js.set_value("")).type(exam_date)

    def select_view_exam_results(self, result: str):
        s(self.DROPDOWN_EXAM_RESULT).all('option').element_by(have.exact_text(result.lower())).click()

    def verify_disabling_filters_fields(self, tcenter: bool = True):
        filter_locators = [
            self.FIELD_NATIONAL_ID,
            self.FIELD_LABOR_NAME,
            self.FIELD_PASSPORT_NUMBER,
            self.FIELD_EMAIL,
            self.DROPDOWN_CATEGORY,
            self.DROPDOWN_EXAM_DATE,
            self.DROPDOWN_EXAM_RESULT
        ]
        if not tcenter:
            filter_locators += [self.DROPDOWN_TCENTER]
        for locator in filter_locators:
            BasePage.is_disabled(locator)

    def click_on_email_field(self):
        s(self.EDIT_EMAIL_FIELD).should(be.clickable).click()

    def click_on_save_btn(self):
        s(self.BTN_SAVE).should(be.clickable).click()

    def fill_field_popup_email(self, text: str = ''):
        s(self.FIELD_POPUP_EMAIL).press(Keys.COMMAND + 'a').press(Keys.BACK_SPACE).type(text)

    def wait_until_popup_disappear(self):
        s(self.FIELD_POPUP_EMAIL).wait_until(be.not_.present)
