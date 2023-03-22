import allure
from selene import command, have
from selene.support.conditions import be
from selene.support.shared.jquery_style import s, ss

from helpers.decorators import for_all_methods
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage
from test_data.constants import DirPath


class SPAUploadLocators:
    BTN_ADD_INDIVIDUAL = '.btn--border-primary'
    BTN_ADD_GROUP = '.btn--primary'
    TD_PASSED_LABORS = '.table tr:nth-child(1) > td:nth-child(3)'
    TABLE_ROWS = 'tbody tr'

    # Upload page locators
    FIELD_FILE_ID = 'th:nth-child(1)  .table-main__input'
    PICKER_UPLOAD_DATE = 'th:nth-child(2)  .table-main__input'
    FIELD_NUMBER_OF_PASSED_LABORS = 'th:nth-child(3)  .table-main__input'
    FIELD_NUMBER_OF_LABORS = 'th:nth-child(4)  .table-main__input'
    LAST_ENTRY = 'tbody tr:nth-child(1) td[data-label="Actions"]'
    VALUE_SEARCH_RESULT = '.pagination-wrap__text'

    # Popup File Information
    BTN_DOWNLOAD_CSV_SAMPLE = '.upload-modal .q-page-box__header a'
    FIELD_POPUP_FILE_NAME = 'td[data-label="File Name"] span'
    FIELD_POPUP_NUMBER_OF_PASSED_LABORS = 'td[data-label="Number of Passed Labors"] span'
    FIELD_POPUP_TOTAL_LABORS = 'td[data-label="Total Labors"] span'
    FIELD_POPUP_PRICE_PER_LABOR = 'td[data-label="Price Per Labor"] span'
    FIELD_POPUP_PRICE_PER_LABOR_LAST = 'td[data-label="Price Per Labor"] span'

    # View locators
    FIELD_VIEW_LABOR_ID = 'div[data-label="National ID"] input'
    FIELD_VIEW_LABOR_NAME = 'div[data-label="Labor Name"] input'
    FIELD_VIEW_PASSPORT_NUMBER = 'div[data-label="Passport Number"] input'
    DROPDOWN_CATEGORY = 'div[data-label="Category"] select'
    DROPDOWN_TEST_CENTER = 'div[data-label="Test Centers"] select'
    DROPDOWN_VIEW_EXAM_DATE = 'div[data-label="Exam Date"] input'
    DROPDOWN_VIEW_EXAM_RESULT = 'div[data-label="Exam Result"] select'

    ICON_VIEW = '.actions-link'

    BTN_CANCEL = '.close-upload-btn'
    BTN_ADD = '.btn-info'

    FIELD_NATIONAL_ID = '#nationalId'
    FIELD_LABOR_NAME = '#laborName'
    FIELD_PASSPORT = '#passport'
    FIELD_SCOPE = '#score'
    FIELD_FILE_NAME = '.table-files-wrapper td:nth-child(1)'
    DROPDOWN_OCCUPATION = '#occupation'
    DROPDOWN_EXAM_DATE = 'label[for=examDate] + span input'
    DROPDOWN_TCENTER = '#testCenter'

    DROPDOWN_TCENTER_LIST = "//label[.='Test Centers List']/following-sibling::div"
    DROPDOWN_CATEGORY_LIST = "//label[.='Category List']/following-sibling::div"
    BTN_CHOOSE_FILE = '#upload_file'


@for_all_methods(allure.step)
class SPAUploadPage(SPAUploadLocators, BasePage):  # pylint: disable=R0904

    def __init__(self):
        super().__init__()
        self.page_url = 'upload'
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)

    def click_add_individual_btn(self):
        s(self.BTN_ADD_INDIVIDUAL).should(be.clickable).click()

    def click_add_group_btn(self):
        s(self.BTN_ADD_GROUP).should(be.clickable).click()

    def click_cancel_btn(self):
        s(self.BTN_CANCEL).should(be.clickable).click()

    def click_add_btn(self):
        s(self.BTN_ADD).should(be.clickable).click()

    def verify_added_labors(self, amount: int = 1):
        s(self.TD_PASSED_LABORS).with_(timeout=5).should(have.exact_text(str(amount)))

    def verify_added_labors_multiple(self, number):
        ss(self.TABLE_ROWS).with_(timeout=3).should(have.size_greater_than_or_equal(number))

    def verify_total_labors(self, amount: int = 1):
        s(self.FIELD_POPUP_TOTAL_LABORS).should(have.exact_text(str(amount)))

    def click_view_icon(self):
        s(self.ICON_VIEW).should(be.clickable).click()

    def select_last_entry(self):
        s(self.LAST_ENTRY).should(be.clickable).click()

    def verify_search_result_value(self, value: str):
        s(self.VALUE_SEARCH_RESULT).should(have.text(value))

    # Upload page filters

    def fill_field_file_id(self, text: str):
        s(self.FIELD_FILE_ID).perform(command.js.set_value("")).type(text)

    def select_upload_date(self, date: str):
        s(self.PICKER_UPLOAD_DATE).perform(command.js.set_value("")).type(date)

    def fill_field_number_of_passed_labors(self, text: str):
        s(self.FIELD_NUMBER_OF_PASSED_LABORS).perform(command.js.set_value("")).type(text)

    def fill_field_number_of_labors(self, text: str):
        s(self.FIELD_NUMBER_OF_LABORS).perform(command.js.set_value("")).type(text)

    # View filters

    def fill_field_view_labor_id(self, text: str):
        s(self.FIELD_VIEW_LABOR_ID).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_field_view_labor_name(self, text: str):
        s(self.FIELD_VIEW_LABOR_NAME).perform(command.js.set_value("")).type(text)

    def fill_field_view_passport_number(self, text: str):
        s(self.FIELD_VIEW_PASSPORT_NUMBER).perform(command.js.set_value("")).type(text)

    def select_tc(self, text: str):
        s(self.DROPDOWN_TEST_CENTER).all('option').element_by(have.exact_text(text)).click()

    def select_view_category(self, text: str):
        s(self.DROPDOWN_CATEGORY).all('option').element_by(have.exact_text(text)).click()

    def select_view_exam_date(self, exam_date: str):
        locator = self.DROPDOWN_VIEW_EXAM_DATE
        s(locator).perform(command.js.set_value("")).type(exam_date)

    def select_view_exam_results(self, result: str):
        results = result if result == 'Passed' else 'Pending'
        locator = self.DROPDOWN_VIEW_EXAM_RESULT
        s(locator).all('option').element_by(have.exact_text(results.lower())).click()

    # Add Individual popup

    def fill_field_national_id(self, text: str):
        s(self.FIELD_NATIONAL_ID).perform(command.js.set_value("")).type(text)

    def fill_field_labor_name(self, text: str):
        s(self.FIELD_LABOR_NAME).perform(command.js.set_value("")).type(text)

    def fill_field_passport(self, text: str):
        s(self.FIELD_PASSPORT).perform(command.js.set_value("")).type(text)

    def fill_field_scope(self, text: str):
        s(self.FIELD_SCOPE).perform(command.js.set_value("")).type(text)

    def select_occupation(self, text: str):
        s(self.DROPDOWN_OCCUPATION).all('option').element_by(have.exact_text(text)).click()

    def select_exam_date(self, exam_date: str):
        s(self.DROPDOWN_EXAM_DATE).perform(command.js.set_value("")).type(exam_date)

    def select_tcenter(self, name: str):
        s(self.DROPDOWN_TCENTER).perform(command.js.set_value("")).type(name)

    def verify_name(self, name: str):
        s(self.FIELD_FILE_NAME).should(have.exact_text(name))

    # Add Group popup

    def click_download_csv_sample(self):
        s(self.BTN_DOWNLOAD_CSV_SAMPLE).should(be.clickable).click()

    def is_choose_file_btn_disabled(self):
        return s(self.BTN_CHOOSE_FILE).matching(be.disabled)

    def is_add_btn_disabled(self):
        return s(self.BTN_ADD).matching(be.disabled)

    def select_tcenter_list(self, text: str):
        s(self.DROPDOWN_TCENTER_LIST).all('option').element_by(have.exact_text(text)).click()

    def select_category_list(self, text: str):
        s(self.DROPDOWN_CATEGORY_LIST).all('option').element_by(have.exact_text(text)).click()

    def upload_csv_file(self, count):
        csv_file = DirPath.CSV if count == 1 else DirPath.CSV_5
        s(self.BTN_CHOOSE_FILE).should(be.clickable).type(csv_file)

    def verify_disabling_filters_fields(self, entry: bool = False):
        if entry:
            filter_locators = [
                self.FIELD_VIEW_LABOR_ID,
                self.FIELD_VIEW_LABOR_NAME,
                self.FIELD_VIEW_PASSPORT_NUMBER,
                self.DROPDOWN_CATEGORY,
                self.DROPDOWN_VIEW_EXAM_DATE,
                self.DROPDOWN_VIEW_EXAM_RESULT
            ]
        else:
            filter_locators = [
                self.FIELD_FILE_ID,
                self.PICKER_UPLOAD_DATE,
                self.FIELD_NUMBER_OF_PASSED_LABORS,
                self.FIELD_NUMBER_OF_LABORS
            ]
        for locator in filter_locators:
            BasePage.is_disabled(locator)
