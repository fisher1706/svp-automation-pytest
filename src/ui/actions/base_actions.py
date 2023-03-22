import time

import allure
import pytest
from selene import be, have
from selene.core.exceptions import ConditionNotMatchedError
from selene.support.shared.jquery_style import s
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from helpers.decorators import for_all_methods
from helpers.email.email_client import EmailClient
from helpers.random_manager import RandomManager
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage


@for_all_methods(allure.step)
class BaseActions(BasePage):

    def __init__(self):
        super().__init__()
        self.confirmation_url = None
        self.confirmation_code = None
        self.random_manager = RandomManager()

    def verify_message(self, expected_message=None, timeout=10):
        if not expected_message:
            return
        try:
            if expected_message["type"] in self.MESSAGE_LOCATOR:
                message_element = s(self.MESSAGE_LOCATOR[expected_message["type"]])
                message_element.wait_until(be.visible)
                message_element.should(have.text(expected_message["text"]), timeout=timeout)
        except (TimeoutException, NoSuchElementException):
            pytest.mark.xfail(f"Expected message was not found on the page in defined timeout. {expected_message}")

    def verify_expected_title(self, expected_title=None, timeout=5):
        if not expected_title:
            return
        if isinstance(expected_title, str):
            expected_title = {'type': 'header', 'text': expected_title}
        try:
            if expected_title["type"] in self.TITLE_LOCATOR:
                message_element = s(self.TITLE_LOCATOR[expected_title["type"]])
                message_element.wait_until(be.visible)
                message_element.should(have.text(expected_title["text"]), timeout=timeout)
        except (TimeoutException, NoSuchElementException):
            pytest.mark.xfail(f"Expected title was not found on the page in defined timeout. {expected_title}")

    @classmethod
    def verify_page_url(cls, page_url):
        current_url = DriverActions().get_url()
        assert current_url.startswith(page_url), f"Current page url [{current_url}] doesn't match expected [{page_url}]"

    def activate_account(self, email_to_confirm, visit=True):
        email_client = EmailClient()
        email_client.receive_confirmation_url(email_to_confirm)
        self.confirmation_url = email_client.confirmation_url
        if visit:
            self.visit(url=self.confirmation_url)
        return self

    def get_confirmation_code(self, email):
        email_client = EmailClient()
        email_client.get_confirmation_code(email)
        self.confirmation_code = email_client.confirmation_code
        return self

    @classmethod
    def click_on_locator(cls, locator):
        return s(locator).click() if isinstance(locator, str) else locator.click()

    @staticmethod
    def verify_expected_result(actual, expected, condition=False):
        result = actual in expected if condition else actual == expected
        assert result, f"Actual result does not match expected\n" \
                       f"Actual: {actual}\n" \
                       f"Expected: {expected}"

    @staticmethod
    def make_lower_case_first_char_of_second_name(text: str):
        text = text.split(' ')
        return text[0] + ' ' + text[1].lower()

    def wait_until_page_updates(self, action, expected_title, arg=None):
        for _ in range(10):
            try:
                if arg:
                    action(arg)
                else:
                    action()
                break
            except (TimeoutException, NoSuchElementException, ConditionNotMatchedError, AssertionError):
                time.sleep(1)
                self.refresh_page()
                self.verify_expected_title(expected_title)
                continue
