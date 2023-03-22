import time

import allure

from helpers.decorators import for_all_methods
from src.ui.actions.base_actions import BaseActions
from src.ui.pages.password import PasswordPage
from test_data.dataset import SetPasswordDataset
from test_data.validation_message import ErrorMessage


@for_all_methods(allure.step)
class PasswordActions(PasswordPage):
    def __init__(self):
        super().__init__()
        self.base_actions = BaseActions()

    def set_password(self, password, confirmed_password, click_continue=True):
        self.enter_password(password).enter_confirmed_password(confirmed_password).click_continue_btn(click_continue)
        return self

    def verify_password_with_invalid_data(self):
        self.base_actions.visit(url=self.base_actions.confirmation_url)
        for password in SetPasswordDataset.INVALID_PASSWORD:
            self.set_password(password[0], password[1])
            time.sleep(1)
            if password == SetPasswordDataset.INVALID_PASSWORD[-1]:
                self.base_actions.verify_message(ErrorMessage.CONFIRMED_PASS_WARNING)
            else:
                self.base_actions.verify_message(ErrorMessage.PASS_WARNING)
