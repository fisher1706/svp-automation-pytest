import allure
from selene import command, have
from selene.core import query
from selene.support.conditions import be
from selene.support.shared.jquery_style import s, ss
from selenium.webdriver.common.keys import Keys

from helpers.decorators import for_all_methods
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage
from test_data.validation_message import WarningMessage


class SPATestCentersLocators:
    BTN_ADD_TEST_CENTER = '//button[.="Add Test Center"]'
    BTN_CANCEL = '//button[.="Cancel"]'
    BTN_ADD = '//button[.="Add"]'
    BTN_EDIT = '//button[.="Edit"]'
    BTN_CONFIRM = '//button[.="Confirm"]'

    FIELD_FILTER_ID = 'div[data-label="ID"] input'
    FIELD_FILTER_NAME = 'div[data-label="Name"] input'
    FIELD_FILTER_CITY = 'div[data-label="City"] input'
    FIELD_FILTER_TEST_CENTER_OWNER = 'div[data-label="Test Center Owner"] input'
    FIELD_FILTER_STATUS = 'div[data-label="Status"] select'

    ICON_DOTS = 'td[data-label="Actions"]'
    ICON_VIEW_ACTION = 'tr:nth-child(1) a[href="view"]'
    ICON_EDIT_ACTION = 'tr:nth-child(1) a[href="edit"]'
    ICON_REMOVE_ACTION = 'tr:nth-child(1) a[href="delete"]'

    FIELD_NAME = '#name'
    FIELD_OFFICIAL_CONTACT_NUMBER = '#phone_number'
    CATEGORY_LIST = '.checkboxes-list__item'
    FIELD_OWNER_NAME = '#owner_full_name'
    FIELD_EMAIL = '#owner_email'
    FIELD_COUNTRY = '#country'
    FIELD_CITY = '#city'
    FIELD_STREET_NAME = '#streetName'
    FIELD_POSTAL_CODE = '#postal_code'
    VALUE_SEARCH_RESULT = '.pagination-wrap__text'

    LIST_FIELDS_VIEW_TC_INFO = '.test-center-details-list__label + p'

    WARNING_NAME = '//input[@id="name"]/parent::div/following-sibling::div/span/span'
    WARNING_PHONE_NUMBER = '//input[@id="phone_number"]/parent::div/following-sibling::span'
    WARNING_CATEGORY = '.checkboxes-list + span'
    WARNING_OWNER_NAME = '//input[@id="owner_full_name"]/parent::div/following-sibling::div/span/span'
    WARNING_EMAIL = '//input[@id="owner_email"]/parent::div/following-sibling::div/span/span'
    WARNING_CITY = '#city + span'
    WARNING_STREET = '//input[@id="streetName"]/parent::div/following-sibling::div/span/span'
    WARNING_POSTAL_CODE = '//input[@id="postal_code"]/parent::div/following-sibling::div/span/span'


@for_all_methods(allure.step)
class SPATestCentersPage(SPATestCentersLocators, BasePage):  # pylint: disable=R0904

    def __init__(self):
        super().__init__()
        self.page_url = 'centers'
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)
        self.wait_spinners_to_disappear()

    def click_add_test_center_btn(self):
        s(self.BTN_ADD_TEST_CENTER).should(be.clickable).click()

    def click_add_btn(self):
        s(self.BTN_ADD).should(be.clickable).perform(command.js.scroll_into_view).click()

    def click_edit_btn(self):
        s(self.BTN_EDIT).should(be.clickable).perform(command.js.scroll_into_view).click()

    def click_cancel_btn(self):
        s(self.BTN_CANCEL).should(be.clickable).click()

    def click_confirm_btn(self):
        s(self.BTN_CONFIRM).should(be.clickable).click()

    def fill_filter_id(self, text):
        s(self.FIELD_FILTER_ID).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_filter_name(self, text):
        s(self.FIELD_FILTER_NAME).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_filter_city(self, text):
        s(self.FIELD_FILTER_CITY).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_filter_test_center_owner(self, text):
        s(self.FIELD_FILTER_TEST_CENTER_OWNER).should(be.visible).perform(command.js.set_value("")).type(text)

    def select_filter_status(self, text):
        s(self.FIELD_FILTER_STATUS).all('option').element_by(have.exact_text(text)).click()

    def fill_tc_name(self, text):
        s(self.FIELD_NAME).should(be.visible).press(Keys.COMMAND, 'a').press(Keys.BACK_SPACE) \
            .press(Keys.BACK_SPACE).type(text)
        return self

    def fill_phone_number(self, text):
        s(self.FIELD_OFFICIAL_CONTACT_NUMBER).should(be.visible).press(Keys.COMMAND, 'a').press(Keys.BACK_SPACE) \
            .press(Keys.BACK_SPACE).type(text)
        return self

    def select_category(self, name=None):
        locator = s(self.CATEGORY_LIST)
        if not locator.s('input').get(query.js_property('checked')):
            locator.s('label').should(have.text(name)).click()
        else:
            locator.s('label').should(have.text(name))
            locator.s('input').should(have.attribute('checked'))

    def unselect_category(self):
        for category in ss(self.CATEGORY_LIST):
            if category.s('input').get(query.js_property('checked')):
                category.s('label').click()
            else:
                category.s('input').should(have.no.attribute('checked'))

    def select_all_categories(self):
        for category in ss(self.CATEGORY_LIST).all('label'):
            category.click()

    def fill_owner_name(self, text):
        s(self.FIELD_OWNER_NAME).should(be.visible).press(Keys.COMMAND, 'a').press(Keys.BACK_SPACE).type(text)

    def fill_email(self, text):
        s(self.FIELD_EMAIL).should(be.visible).press(Keys.COMMAND, 'a').press(Keys.BACK_SPACE).type(text)

    def fill_tc_city(self, text):
        s(self.FIELD_CITY).should(be.visible).press(Keys.COMMAND, 'a').press(Keys.BACK_SPACE).type(text)

    def fill_street_name(self, text):
        s(self.FIELD_STREET_NAME).should(be.visible).press(Keys.COMMAND, 'a').press(Keys.BACK_SPACE).type(text)

    def fill_postal_code(self, text):
        s(self.FIELD_POSTAL_CODE).should(be.visible).press(Keys.COMMAND, 'a').press(Keys.BACK_SPACE).type(text)

    def get_amount_of_entities(self):
        return int(s(self.VALUE_SEARCH_RESULT).get(query.text).split()[0])

    def verify_search_result_value(self, value: int):
        return s(self.VALUE_SEARCH_RESULT).should(have.text(str(value)))

    def verify_disabling_filters_fields(self):
        filter_locators = [
            self.FIELD_FILTER_ID,
            self.FIELD_FILTER_NAME,
            self.FIELD_FILTER_CITY,
            self.FIELD_FILTER_TEST_CENTER_OWNER
        ]
        for locator in filter_locators:
            BasePage.is_disabled(locator)

    def verify_empty_name_field(self):
        s(self.WARNING_NAME).should(be.visible).should(have.text(WarningMessage.TC_EMPTY_NAME))

    def verify_empty_contact_number_field(self):
        s(self.WARNING_PHONE_NUMBER).should(be.visible).should(have.text(WarningMessage.TC_CONTACT_NUMBER))

    def verify_empty_category_list(self):
        s(self.WARNING_CATEGORY).should(be.visible).should(have.text(WarningMessage.TC_EMPTY_CATEGORY_LIST))

    def verify_empty_owner_name_field(self):
        s(self.WARNING_OWNER_NAME).should(be.visible).should(have.text(WarningMessage.TC_EMPTY_OWNER_NAME))

    def verify_empty_email_field(self):
        s(self.WARNING_EMAIL).should(be.visible).should(have.text(WarningMessage.TC_EMPTY_EMAIL))

    def verify_empty_city_field(self):
        s(self.WARNING_CITY).should(be.visible).should(have.text(WarningMessage.TC_EMPTY_CITY))

    def verify_empty_street_field(self):
        s(self.WARNING_STREET).should(be.visible).should(have.text(WarningMessage.TC_EMPTY_STREET))

    def verify_warning_duplicate_name(self):
        s(self.WARNING_NAME).should(be.visible).should(have.text(WarningMessage.TC_NAME))

    def verify_warning_duplicate_email(self):
        s(self.WARNING_EMAIL).should(be.visible).should(have.text(WarningMessage.EMAIL_IS_EXIST))

    def verify_warning_digits_only_contact_number(self):
        s(self.WARNING_PHONE_NUMBER).should(be.visible).should(have.text(WarningMessage.TC_ONLY_DIGITS_CONTACT_NUMBER))

    def verify_warning_invalid_email(self):
        s(self.WARNING_EMAIL).should(be.visible).should(have.text(WarningMessage.TC_VALID_EMAIL))

    def verify_warning_en_chars_only_city(self):
        s(self.WARNING_CITY).should(be.visible).should(have.text(WarningMessage.ONLY_EN_CHARS))

    def verify_warning_digits_only_postal_code(self):
        s(self.WARNING_POSTAL_CODE).should(be.visible).should(have.text(WarningMessage.TC_ONLY_DIGITS_POSTAL_CODE))

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

    def get_name(self):
        return s(self.FIELD_NAME).should(be.enabled).get(query.attribute('value'))

    def get_official_contact_number(self):
        return s(self.FIELD_OFFICIAL_CONTACT_NUMBER).should(be.enabled).get(query.attribute('value'))

    def verify_category(self, text):
        locator = s(self.CATEGORY_LIST)
        locator.s('input').should(have.attribute("checked"))
        locator.s('label').should(have.text(text))

    def get_owner_name(self):
        return s(self.FIELD_OWNER_NAME).should(be.enabled).get(query.attribute('value'))

    def get_email(self):
        return s(self.FIELD_EMAIL).should(be.enabled).get(query.attribute('value'))

    def get_city(self):
        return s(self.FIELD_CITY).should(be.enabled).get(query.attribute('value'))

    def get_street_name(self):
        return s(self.FIELD_STREET_NAME).should(be.enabled).get(query.attribute('value'))

    def get_tc_info(self):
        return [item.get(query.text) for item in ss(self.LIST_FIELDS_VIEW_TC_INFO)]

    def verify_is_disabled_country_field(self):
        s(self.FIELD_COUNTRY).should(be.disabled)
