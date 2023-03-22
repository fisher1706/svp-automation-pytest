from selene import command, be
from selene.support.shared.jquery_style import s, ss

from helpers.logger import yaml_logger
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage

logger = yaml_logger.setup_logging(__name__)


class LegislatorsPageLocators:  # pylint: disable=too-few-public-methods
    BTN_NEW_LEGISLATORS = "//*[contains(text(),'New Legislator')]"
    BTN_CREATE_LEGISLATOR = "//*[contains(text(),'Create Legislator')]"
    BTN_CANCEL = "//*[contains(text(),'Cancel')]"
    FIELD_NAME = '#englishName'
    BTN_LOGO_FILE = '#logo'
    DROPDOWN_COUNTRY = '#country'
    FIELD_CITY = '#city'
    FIELD_ADDRESS = '#address'
    FIELD_CONTACT_NAME = '#name'
    FIELD_CONTACT_PHONE = '.input-group__input[type=tel]'
    FIELD_EMAIL = '#email'


class LegislatorsPage(BasePage, LegislatorsPageLocators):

    def __init__(self):
        super().__init__()
        self.page_url = 'legislators'
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)

    def click_btn_new_legislators(self):
        s(self.BTN_NEW_LEGISLATORS).should(be.clickable).click()

    def click_btn_create_legislator(self):
        s(self.BTN_CREATE_LEGISLATOR).should(be.clickable).click()

    def upload_logo_file(self, dir_path=None):
        s(self.BTN_LOGO_FILE).should(be.clickable).type(dir_path)

    def select_dropdown_county(self, text: str):
        s(self.DROPDOWN_COUNTRY).type(text)

    def fill_name_field(self, text: str):
        s(self.FIELD_NAME).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_city_field(self, text: str):
        s(self.FIELD_CITY).type(text)
        ss('.pac-item').first.click()

    def fill_address_field(self, text: str):
        s(self.FIELD_ADDRESS).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_contact_name_field(self, text: str):
        s(self.FIELD_CONTACT_NAME).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_phone_field(self, text: str):
        s(self.FIELD_CONTACT_PHONE).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_email_field(self, text: str):
        s(self.FIELD_EMAIL).should(be.visible).perform(command.js.set_value("")).type(text)
