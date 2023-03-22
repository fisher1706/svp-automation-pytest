import allure
from selene import command
from selene.support.conditions import be, have
from selene.support.shared.jquery_style import s

from helpers.decorators import for_all_methods
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage
from test_data.validation_message import WarningMessage


class SPAChangePasswordLocators:
    BTN_BACK = '.btn-auth'
    BTN_CHANGE_PASSWORD = '#continue_button'

    FIELD_CURRENT_PASSWORD = '#current_password'
    ICON_VIEW_CURRENT_PASSWORD = f'{FIELD_CURRENT_PASSWORD} + span'
    FIELD_NEW_PASSWORD = '#password'
    ICON_VIEW_NEW_PASSWORD = f'{FIELD_NEW_PASSWORD} + span'
    FIELD_CONFIRMED_NEW_PASSWORD = '#confirmedPassword'
    ICON_VIEW_CONFIRMED_NEW_PASSWORD = f'{FIELD_CONFIRMED_NEW_PASSWORD} + span'

    WARNING_CURRENT_PASSWORD = '//input[@id="current_password"]/parent::div/following-sibling::div/span/span'
    WARNING_NEW_PASSWORD = '//input[@id="password"]/parent::div/following-sibling::div/span/span'
    WARNING_CONFIRM_NEW_PASSWORD = '//input[@id="confirmedPassword"]/parent::div/following-sibling::div/span/span'


@for_all_methods(allure.step)
class SPAChangePasswordPage(SPAChangePasswordLocators, BasePage):

    def __init__(self):
        super().__init__()
        self.page_url = 'auth/change-pass'
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)

    def click_back_btn(self):
        s(self.BTN_BACK).should(be.clickable).click()

    def fill_current_password(self, text):
        s(self.FIELD_CURRENT_PASSWORD).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_new_password(self, text):
        s(self.FIELD_NEW_PASSWORD).should(be.visible).perform(command.js.set_value("")).type(text)

    def fill_confirmed_new_password(self, text):
        s(self.FIELD_CONFIRMED_NEW_PASSWORD).should(be.visible).perform(command.js.set_value("")).type(text)

    def verify_warning_current_password(self):
        s(self.WARNING_CURRENT_PASSWORD).should(be.visible).should(have.text(WarningMessage.INVALID_CURRENT_PASSWORD))

    def verify_warning_new_password(self):
        s(self.WARNING_NEW_PASSWORD).should(be.visible).should(have.text(WarningMessage.SAME_NEW_PASSWORD))

    def verify_warning_confirm_new_password(self):
        s(self.WARNING_CONFIRM_NEW_PASSWORD).should(be.visible).should(have.text(WarningMessage.MISMATCH_PASSWORD))

    def verify_is_change_button_disabled(self):
        s(self.BTN_CHANGE_PASSWORD).should(be.disabled)
