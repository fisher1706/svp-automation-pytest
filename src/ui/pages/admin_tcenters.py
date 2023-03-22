from selene import command, be, have
from selene.support.shared.jquery_style import s, ss

from helpers.logger import yaml_logger
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage
from test_data.constants import Filters, Status

logger = yaml_logger.setup_logging(__name__)


class TCentersPageLocators:  # pylint: disable=too-few-public-methods
    BTN_NEW_TEST_CENTER = "//a[text() = 'New Test Center']"
    BTN_SEARCH = "//button[text() = 'Search']"
    DROPDOWN_NAME = "label[for='englishName'] + div select"
    FILTER_FIELD_NAME = '#englishName'
    DROPDOWN_CITY = "label[for='city'] + div select"
    DROPDOWN_STATUSES = '#status'

    ICON_DOTS = 'td[data-label="Actions"]'
    ICON_VIEW_ACTION = "//ul[@class = 'table-main__actioins-list']//a[text() = 'View']"
    ICON_EDIT_ACTION = "//ul[@class = 'table-main__actioins-list']//a[text() = 'Edit']"
    ICON_REMOVE_ACTION = "//ul[@class = 'table-main__actioins-list']//a[text() = 'Delete']"

    BTN_CREATE_TEST_CENTER = "//button[text() = 'Create Test Center']"
    BTN_CANCEL = "//button[text() = 'Cancel']"
    FIELD_NAME = '#name'
    DROPDOWN_COUNTRY = '#country'
    DROPDOWN_CATEGORY = '.arrow'
    DROPDOWN_CATEGORY_ITEM = '.multiselect__element span'
    FIELD_CITY = '#city'
    FIELD_ADDRESS = '#address'
    FIELD_CONTACT_PHONE = '#phoneNumber'
    DROPDOWN_LEGISLATOR = '#legislator'
    FIELD_CONTACT_NAME = '#testCenterOwnerName'
    FIELD_EMAIL = '#testCenterOwnerEmail'

    TITLE = 'h1'
    locator = "//span[@class='details-list__title' and text()='{}']//following::div/span"
    NAME = locator.format('Name')
    ADDRESS = locator.format('Address')
    SUPPORTED_CATEGORIES = locator.format('Supported categories')
    COUNTRY = locator.format('Country')
    CITY = locator.format('City')
    STATUS = locator.format('Status')
    PHONE_NUMBER = locator.format('Phone Number')
    LEGISLATOR = locator.format('Legislator')
    TEST_CENTER_OWNER_NAME = locator.format('Test Center Owner Name')
    TEST_CENTER_OWNER_EMAIL = locator.format('Test Center Owner Email')


class TCentersPage(BasePage, TCentersPageLocators):

    def __init__(self):
        super().__init__()
        self.page_url = 'centers'
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url, admin=True)

    # Test Centers

    def click_btn_new_test_center(self):
        s(self.BTN_NEW_TEST_CENTER).should(be.clickable).click()

    def click_btn_search(self):
        s(self.BTN_SEARCH).should(be.clickable).click()

    def click_btn_cancel(self):
        s(self.BTN_NEW_TEST_CENTER).should(be.clickable).click()

    def select_dropdown_name(self, key=Filters.CONTAINS):
        s(self.DROPDOWN_NAME).all('option').element_by(have.exact_text(key)).click()

    def fill_filter_name_field(self, text):
        s(self.FILTER_FIELD_NAME).should(be.visible).perform(command.js.set_value("")).type(text)

    def select_filter_dropdown_county(self, country: str):
        s(self.DROPDOWN_COUNTRY).all('option').element_by(have.exact_text(country)).click()

    def select_dropdown_city(self, key=Filters.CONTAINS):
        s(self.DROPDOWN_CITY).all('option').element_by(have.exact_text(key)).click()

    def fill_filter_city_field(self, text):
        s(self.FIELD_CITY).should(be.visible).perform(command.js.set_value("")).type(text)

    def select_dropdown_statuses(self, key=Status.ACTIVE):
        s(self.DROPDOWN_CITY).all('option').element_by(have.exact_text(key)).click()

    def select_view_of_last_entry(self):
        s(self.ICON_DOTS).hover()
        s(self.ICON_VIEW_ACTION).should(be.clickable).click()

    def select_edit_of_last_entry(self):
        s(self.ICON_DOTS).hover()
        s(self.ICON_EDIT_ACTION).should(be.clickable).click()
        self.wait_spinners_to_disappear()

    def select_remove_of_last_entry(self):
        s(self.ICON_DOTS).hover()
        s(self.ICON_REMOVE_ACTION).should(be.clickable).click()

    # New Test Center

    def click_btn_create_test_center(self):
        s(self.BTN_CREATE_TEST_CENTER).should(be.clickable).click()

    def select_dropdown_county(self, text: str):
        s(self.DROPDOWN_COUNTRY).should(be.clickable).type(text).press_escape()

    def select_dropdown_category(self, text):
        s(self.DROPDOWN_CATEGORY).click()
        ss(self.DROPDOWN_CATEGORY_ITEM).all('span').element_by(have.exact_text(text)).click()

    def fill_name_field(self, text: str):
        s(self.FIELD_NAME).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_city_field(self, text: str):
        s(self.FIELD_CITY).type(text)
        ss('.pac-item').first.click()

    def fill_address_field(self, text: str):
        s(self.FIELD_ADDRESS).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_phone_field(self, text: str):
        s(self.FIELD_CONTACT_PHONE).should(be.visible).perform(command.js.set_value("")).type(text)

    def select_legislator(self, text):
        s(self.DROPDOWN_LEGISLATOR).all('option').element_by(have.exact_text(text)).click()

    def fill_tc_owner_name_field(self, text: str):
        s(self.FIELD_CONTACT_NAME).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_email_field(self, text: str):
        s(self.FIELD_EMAIL).should(be.visible).perform(command.js.set_value("")).type(text)

    # View

    def verify_name_in_title(self, text):
        s(self.TITLE).should(be.visible).should(have.text(text))

    def verify_name(self, text):
        s(self.NAME).should(be.visible).should(have.text(text))

    def verify_adress(self, text):
        s(self.ADDRESS).should(be.visible).should(have.text(text))

    def verify_category(self, text):
        s(self.SUPPORTED_CATEGORIES).should(be.visible).should(have.text(text))

    def verify_country(self, text):
        s(self.COUNTRY).should(be.visible).should(have.text(text))

    def verify_city(self, text):
        s(self.CITY).should(be.visible).should(have.text(text))

    def verify_status(self, status=Status.ACTIVE):
        s(self.STATUS).should(be.visible).should(have.text(status))

    def verify_phone_number(self, text):
        s(self.PHONE_NUMBER).should(be.visible).should(have.text(text))

    def verify_legislator(self, text='Autotest'):
        s(self.LEGISLATOR).should(be.visible).should(have.text(text))

    def verify_tcenter_owner_name(self, text):
        s(self.TEST_CENTER_OWNER_NAME).should(be.visible).should(have.text(text))

    def verify_tcenter_owner_email(self, text):
        s(self.TEST_CENTER_OWNER_EMAIL).should(be.visible).should(have.text(text))
