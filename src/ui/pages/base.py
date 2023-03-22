import time

import allure
from selene import be, by
from selene.support.conditions import have
from selene.support.shared.jquery_style import s

from helpers.decorators import for_all_methods
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.spa_payment import SPAPaymentLocators
from test_data.validation_message import InfoMessages


class BaseLocators:
    MESSAGE_LOCATOR = {
        'success': '.alert-text-holder p',
        'otp code': '.login-form__text.pb-3',
        'email code': '.login-form__text.pb-3',
        'invalid credentials error': '.validation-message--margin-bottom > span',
        'legislator creation': '.alert-message > p',
        'pass warning': '.validation-message--default > span > span',
        'token warning': '.validation-message--margin-bottom > span',
        'spa user type': '.user-info__role',
        'card number': SPAPaymentLocators.WARNING_MSG_CARD_NUMBER,
        'card expiry date': SPAPaymentLocators.WARNING_MSG_EXPIRY_DATE,
        'card cvv': SPAPaymentLocators.WARNING_MSG_CVV,
        'card holder': SPAPaymentLocators.WARNING_MSG_CARD_HOLDER,
        'popup edit email': '.validation-message__text span',
        'active certificate': '.modal-form__heading',
        'test center creation': "div[role='status'] div"
    }
    TITLE_LOCATOR = {
        'header': '.header-section h1',
        'spa login': '.sign-template__header h1',
        'header payment': '.payment-box__header-text',
        'spa': '.q-page-box__header h2',
        'modal': '.modal-box .q-page-box__header',
        'home': '.home-section__heading'
    }
    OLD_WAITING_SPINNER = by.css('.q-spinner-inner')
    WAITING_SPINNER = by.css('.app-spinner span')
    CONTINUE_BUTTON = '#continue_button'
    SPA_NO_DATA_AVAILABLE = '.modal-box--empty-text'
    ADMIN_NO_DATA_AVAILABLE = '.table-no-data'


@for_all_methods(allure.step)
class BasePage(BaseLocators):

    def __init__(self):
        super().__init__()
        self.driver_actions = DriverActions()

    def visit(self, **kwargs):
        self.driver_actions.visit(kwargs.get('url'), kwargs.get('admin'))

    def refresh_page(self):
        time.sleep(1)
        self.driver_actions.refresh_page()
        time.sleep(1)
        return self

    def wait_spinners_to_disappear(self):
        s(self.WAITING_SPINNER).wait_until(be.not_.visible)
        return self

    @staticmethod
    def is_disabled(locator_name: str):
        assert s(locator_name).should(have.value(''))

    def click_continue_btn(self, click_button=True):
        element = s(self.CONTINUE_BUTTON)
        if click_button:
            element.should(be.clickable).click()
        else:
            element.should(be.disabled)
        return self

    def verify_no_data_available(self, spa=True):
        no_data_available = s(self.SPA_NO_DATA_AVAILABLE) if spa else s(self.ADMIN_NO_DATA_AVAILABLE)
        no_data_available.wait_until(be.present)
        no_data_available.should(have.exact_text(InfoMessages.NO_DATA_AVAILABLE))
