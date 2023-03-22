from selene import command, be, query
from selene.support.shared.jquery_style import s

from helpers.logger import yaml_logger
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage

logger = yaml_logger.setup_logging(__name__)


class LoginPageLocators:  # pylint: disable=too-few-public-methods
    LOGIN_FIELD = '#login_email'
    PASSWORD_FIELD = '#login_password'

    TWO_FA_FIELD = '.fk-input-container input'
    SIGN_IN_BUTTON = '.sign-form__button'
    CAPCHA_FIELD = '.input-group__re-captcha'
    OTP_CODE = '.otp-code'
    OTP_CODE_WARNING_MSG = '.validation-message__text'


class LoginPage(BasePage, LoginPageLocators):

    def __init__(self):
        super().__init__()
        self.page_url = 'auth'
        self.driver_actions = DriverActions()

    def visit(self, url=None, admin=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url, admin)

    def enter_login(self, email):
        s(self.LOGIN_FIELD).perform(command.js.set_value("")).type(email)
        return self

    def enter_password(self, pwd):
        s(self.PASSWORD_FIELD).perform(command.js.set_value("")).type(pwd)
        return self

    def get_2fa_code(self):
        return s(self.OTP_CODE).get(query.text).split(' ')[2]

    def is_warning_msg_displayed(self):
        return s(self.OTP_CODE_WARNING_MSG).matching(be.visible)

    def enter_2fa_code(self, code: str):
        s(self.TWO_FA_FIELD).should(be.blank).type(code)
        return self

    def click_sign_in_btn(self, click_button=True):
        button = s(self.SIGN_IN_BUTTON)
        if click_button:
            button.wait_until(be.clickable)
            button.should(be.clickable).click()
        else:
            button.should(be.disabled)
            logger.debug('Skip click on "Sign in" button. Not clickable')
        return self

    def wait_sign_in_btn_become_disabled(self):
        s(self.SIGN_IN_BUTTON).wait_until(be.disabled)

    def is_capcha_displayed(self):
        s(self.CAPCHA_FIELD).should(be.visible)
        return self

    def wait_page_to_load(self):
        s(self.PASSWORD_FIELD).wait_until(be.visible)
        return self

    def is_two_factor_field_displayed(self):
        s(self.TWO_FA_FIELD).matching(be.visible)
        return self
