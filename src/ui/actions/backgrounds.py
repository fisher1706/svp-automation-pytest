from src.api.actions.admin_api_actions import AdminApiActions
from src.api.actions.auth_api_actions import AuthApiActions
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.login_actions import LoginActions
from src.ui.actions.password_actions import PasswordActions
from test_data.constants import UserInfo, Title


class BackgroundsActions:

    def __init__(self, api):
        super().__init__()
        self.tcenter_name = None
        self.base_actions = BaseActions()
        self.auth_api_actions = AuthApiActions(api)
        self.admin_api_actions = AdminApiActions(api)
        self.password = PasswordActions()
        self.login_actions = LoginActions()

    def __activate_account_and_set_password(self, tcenter):
        self.admin_api_actions.activate_account(tcenter)
        self.password.set_password(UserInfo.DEFAULT_PASSWORD, UserInfo.DEFAULT_PASSWORD, click_continue=True)
        self.base_actions.verify_expected_title(expected_title=Title.SPA_SIGN_IN, timeout=15)

    def create_entities_and_log_in(self, is_legislator=True,
                                   is_legislator_activate=False,
                                   is_tcenter=False,
                                   is_tcenter_activate=False,
                                   login=True,
                                   login_tcenter=True,
                                   is_multiple_categories=False,
                                   two_factor_verification=''):
        self.auth_api_actions.get_token()
        self.admin_api_actions.put_permissions(token=self.auth_api_actions.token,
                                               tcenter=login_tcenter,
                                               multiple_categories=is_multiple_categories)
        if is_legislator:
            self.admin_api_actions.create_legislator(self.auth_api_actions.token)
            if is_legislator_activate:
                self.__activate_account_and_set_password(self.admin_api_actions.legislator_account.email)
        if is_tcenter:
            self.admin_api_actions.create_tcenter(self.auth_api_actions.token)
            self.tcenter_name = self.admin_api_actions.tcenter_account.en_name
            if is_tcenter_activate:
                self.__activate_account_and_set_password(self.admin_api_actions.tcenter_account.email)
        if login:
            email = self.admin_api_actions.tcenter_account.email if login_tcenter else \
                self.admin_api_actions.legislator_account.email
            self.login_actions.log_in_to_spa(email, two_factor_verification)
        return self
