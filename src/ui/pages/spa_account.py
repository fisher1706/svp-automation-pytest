import allure
from selene import query, command
from selene.support.conditions import be, have
from selene.support.shared.jquery_style import s

from helpers.decorators import for_all_methods
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage
from test_data.validation_message import WarningMessage


class SPAAccountLocators:
    TOGGLE_SHOW_LOGO = 'div:nth-child(2) > ul > li:nth-child(2) > div'
    ADDRESS = 'div:nth-child(2) > ul > li:nth-child(3) > div'
    POSTAL_CODE = 'div:nth-child(2) > ul > li:nth-child(4) > div'
    FULL_NAME = 'div:nth-child(4) > ul > li:nth-child(1) > div'
    PHONE_NUMBER = 'div:nth-child(4) > ul > li:nth-child(2) > div'
    EMAIL = 'div:nth-child(4) > ul > li:nth-child(3) > div'

    BTN_EDIT = '//button[.="Edit"]'
    BTN_SAVE = '//button[.="Save"]'
    BTN_CANCEL = '//button[.="Cancel"]'

    BTN_LOGO_FILE = '#logo'
    TOGGLE_EDIT_SHOW_LOGO = '.switch'
    TOGGLE_STATUS = '.switch input'
    FIELD_ADDRESS = '#address'
    FIELD_POSTAL_CODE = '#postal_code'
    FIELD_FULL_NAME = '#full_name'
    FIELD_PHONE_NUMBER = '#phone_number'
    FIELD_EMAIL = '#email'

    WARNING_POSTAL_CODE = '//input[@id="postal_code"]/parent::div/following-sibling::div/span/span'
    WARNING_NAME = '//input[@id="full_name"]/parent::div/following-sibling::div/span/span'
    WARNING_PHONE_NUMBER = '//input[@id="phone_number"]/parent::div/following-sibling::span'
    WARNING_EMAIL = '//input[@id="email"]/parent::div/following-sibling::div/span/span'


@for_all_methods(allure.step)
class SPAAccountPage(SPAAccountLocators, BasePage):

    def __init__(self):
        super().__init__()
        self.page_url = 'account'
        self.driver_actions = DriverActions()

    # TODO: Need to clarify pass context variable to the static method
    @staticmethod
    def __get_text(locator, is_edit):
        if is_edit:
            return s(locator).should(be.visible).get(query.attribute('value'))
        return s(locator).should(be.visible).get(query.text)

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)

    def get_show_logo(self, is_edit: bool = False):
        if is_edit:
            return s(self.TOGGLE_STATUS).should(be.in_dom).get(query.js_property('checked'))
        return s(self.TOGGLE_SHOW_LOGO).should(be.visible).get(query.text)

    def get_address(self, is_edit: bool = False):
        locator = self.FIELD_ADDRESS if is_edit else self.ADDRESS
        return SPAAccountPage.__get_text(locator, is_edit)

    def get_postal_code(self, is_edit: bool = False):
        locator = self.FIELD_POSTAL_CODE if is_edit else self.POSTAL_CODE
        return SPAAccountPage.__get_text(locator, is_edit)

    def get_full_name(self, is_edit: bool = False):
        locator = self.FIELD_FULL_NAME if is_edit else self.FULL_NAME
        return SPAAccountPage.__get_text(locator, is_edit)

    def get_phone_number(self, is_edit: bool = False):
        locator = self.FIELD_PHONE_NUMBER if is_edit else self.PHONE_NUMBER
        return SPAAccountPage.__get_text(locator, is_edit)

    def get_email(self, is_edit: bool = False):
        locator = self.FIELD_EMAIL if is_edit else self.EMAIL
        return SPAAccountPage.__get_text(locator, is_edit)

    def click_edit_btn(self):
        s(self.BTN_EDIT).should(be.clickable).perform(command.js.scroll_into_view).click()

    def verify_btn_edit_is_disabled(self):
        s(self.BTN_EDIT).should(be.disabled)

    def click_cancel_btn(self):
        s(self.BTN_CANCEL).should(be.clickable).click()

    def click_save_btn(self):
        s(self.BTN_SAVE).should(be.clickable).perform(command.js.scroll_into_view).click()

    def fill_address(self, text):
        s(self.FIELD_ADDRESS).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_postal_code(self, text):
        s(self.FIELD_POSTAL_CODE).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_full_name(self, text):
        s(self.FIELD_FULL_NAME).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_phone_number(self, text):
        s(self.FIELD_PHONE_NUMBER).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_email(self, text):
        s(self.FIELD_EMAIL).should(be.visible).perform(command.js.set_value("")).type(text)

    def select_show_logo_toggle(self):
        s(self.TOGGLE_EDIT_SHOW_LOGO).should(be.in_dom).click()

    def upload_logo_file(self, dir_path=None):
        s(self.BTN_LOGO_FILE).should(be.clickable).type(dir_path)

    def verify_warning_digits_only_postal_code(self):
        s(self.WARNING_POSTAL_CODE).should(be.visible).should(have.text(WarningMessage.TC_ONLY_DIGITS_POSTAL_CODE))

    def verify_warning_en_chars_only_name(self):
        s(self.WARNING_NAME).should(be.visible).should(have.text(WarningMessage.ONLY_EN_CHARS))

    def verify_warning_digits_only_contact_number(self):
        s(self.WARNING_PHONE_NUMBER).should(be.visible).should(have.text(WarningMessage.TC_ONLY_DIGITS_CONTACT_NUMBER))

    def verify_warning_invalid_email_field(self):
        s(self.WARNING_EMAIL).should(be.visible).should(have.text(WarningMessage.TC_VALID_EMAIL))

    def verify_warning_duplicate_email(self):
        s(self.WARNING_EMAIL).should(be.visible).should(have.text(WarningMessage.EMAIL_IS_EXIST))
