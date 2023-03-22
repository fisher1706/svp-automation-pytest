from selene import command, be
from selene.support.shared.jquery_style import s

from helpers.logger import yaml_logger
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage

logger = yaml_logger.setup_logging(__name__)


class PasswordPageLocators:  # pylint: disable=too-few-public-methods
    PASSWORD_FIELD = '#password'
    CONFIRMED_PASSWORD = '#confirmedPassword'


class PasswordPage(BasePage, PasswordPageLocators):

    def __init__(self):
        super().__init__()
        self.page_url = 'auth'
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)

    def enter_password(self, pwd):
        s(self.PASSWORD_FIELD).perform(command.js.set_value("")).type(pwd).press_tab()
        return self

    def enter_confirmed_password(self, email):
        s(self.CONFIRMED_PASSWORD).perform(command.js.set_value("")).type(email).press_tab()
        return self

    def wait_page_to_load(self):
        s(self.PASSWORD_FIELD).wait_until(be.visible)
        return self
