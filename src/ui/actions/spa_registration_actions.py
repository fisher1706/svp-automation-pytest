from src.ui.actions.base_actions import BaseActions
from src.ui.actions.password_actions import PasswordActions
from test_data.constants import UserInfo, Title
from test_data.validation_message import ErrorMessage


class SPARegistration:
    def __init__(self):
        self.password_actions = PasswordActions()
        self.base_actions = BaseActions()

    def verify_password_validation(self):
        self.base_actions.visit(url=self.base_actions.confirmation_url)
        self.base_actions.verify_expected_title(expected_title=Title.SPA_SET_PASSWORD)
        self.password_actions.set_password(UserInfo.DEFAULT_PASSWORD, UserInfo.DEFAULT_PASSWORD, click_continue=True)
        self.base_actions.verify_expected_title(expected_title=Title.SPA_SIGN_IN)
        self.base_actions.visit(url=self.base_actions.confirmation_url)
        self.password_actions.set_password(UserInfo.DEFAULT_PASSWORD, UserInfo.DEFAULT_PASSWORD, click_continue=True)
        self.base_actions.verify_message(ErrorMessage.TOKEN_INVALID)
