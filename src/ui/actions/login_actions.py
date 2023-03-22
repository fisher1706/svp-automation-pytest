import time

import allure

from helpers.decorators import for_all_methods
from src.ui.actions.base_actions import BaseActions
from src.ui.pages.login import LoginPage
from src.ui.pages.spa import SPA
from test_data.constants import UserInfo, Authentication, Title
from test_data.validation_message import WarningMessage, SuccessMessage


@for_all_methods(allure.step)
class LoginActions(LoginPage):

    def __init__(self):
        super().__init__()
        self.base_actions = BaseActions()
        self.spa = SPA()

    def __proceed_2fa(self, two_factor_code=None, click_button=True):
        is_passed = False
        for _ in range(5):
            if not two_factor_code:
                two_factor_code = self.get_2fa_code()
            self.enter_2fa_code(two_factor_code).click_sign_in_btn(click_button)
            time.sleep(3)
            if self.is_warning_msg_displayed():
                two_factor_code = None
            elif self.wait_sign_in_btn_become_disabled():
                continue
            else:
                is_passed = True
                break
        assert is_passed, WarningMessage.OTP_CODE

    def __proceed_2fa_via_email(self, email, two_factor_code=None, click_button=True):
        if not two_factor_code:
            self.base_actions.get_confirmation_code(email)
            two_factor_code = self.base_actions.confirmation_code
        self.enter_2fa_code(two_factor_code).click_sign_in_btn(click_button)

    def __proceed_2fa_api(self, get_otp_code, email, admin, click_button=True):
        is_passed = False
        for _ in range(5):
            auth_api = get_otp_code(email, admin)
            self.enter_2fa_code(auth_api.otp_code).click_sign_in_btn(click_button)
            time.sleep(3)
            if self.wait_sign_in_btn_become_disabled():
                continue
            is_passed = True
            break
        assert is_passed, WarningMessage.OTP_CODE

    def proceed_2fa(self, two_factor_verification='', two_factor_code=None, email='', click_button=True, user_type=''):
        match two_factor_verification:
            case Authentication.EMAIL:
                self.__proceed_2fa_via_email(email, two_factor_code, click_button)
            case Authentication.API:
                self.__proceed_2fa_api(two_factor_code, email, user_type, click_button)
            case Authentication.OTP_FROM_NETWORK:
                two_factor_code = self.base_actions.driver_actions.get_otp_code_from_network()
                self.enter_2fa_code(two_factor_code).click_sign_in_btn(click_button)
                self.base_actions.verify_message(SuccessMessage.LOGIN)
            case '':
                self.__proceed_2fa(two_factor_code, click_button)

    def log_in_user(self, login, password, click_continue=True):
        self.enter_login(login).enter_password(password).click_continue_btn(click_continue)
        return self

    def log_out_user(self):
        self.spa.click_on_profile_menu().click_logout_btn()
        self.wait_page_to_load()

    def log_in_to_spa_with_permanent_email(self, tcenter=True, is_ui=True, auth_api=None):
        self.visit()
        email = UserInfo.TC_LOGIN if tcenter else UserInfo.LEGISLATOR_LOGIN
        self.log_in_user(email, UserInfo.DEFAULT_PASSWORD)
        self.base_actions.verify_message(SuccessMessage.CONFIRM_CODE)
        if is_ui:
            self.proceed_2fa()
        else:
            user_type = 'test center' if tcenter else 'legislator'
            self.proceed_2fa(two_factor_code=auth_api.get_otp_code, email=UserInfo.TC_LOGIN, user_type=user_type)

    def log_in_to_spa(self, email, two_factor_verification=''):
        self.visit()
        self.wait_page_to_load()
        self.log_in_user(email, UserInfo.DEFAULT_PASSWORD)
        self.base_actions.verify_message(SuccessMessage.CONFIRM_CODE)
        self.proceed_2fa(two_factor_verification, email=email)
        self.base_actions.verify_expected_title(expected_title=Title.UPLOADED_FILES)

    def log_in_to_admin(self):
        self.log_in_user(UserInfo.DEFAULT_LOGIN, UserInfo.DEFAULT_PASSWORD)
        self.base_actions.verify_message(SuccessMessage.ADMIN_CONFIRM_CODE)
        self.proceed_2fa()
