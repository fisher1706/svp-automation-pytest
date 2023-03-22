import time

import allure

from helpers.decorators import for_all_methods
from src.api.features.admin_api import AdminApi
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.driver_actions import DriverActions
from src.ui.actions.login_actions import LoginActions
from src.ui.pages.admin_dashboard import DashboardPage
from src.ui.pages.admin_legislators import LegislatorsPage
from src.ui.pages.admin_tcenters import TCentersPage
from test_data.constants import Title
from test_data.models.model_builder import ModelBuilder
from test_data.validation_message import SuccessMessage


@for_all_methods(allure.step)
class AdminActions(LegislatorsPage):

    def __init__(self, api):
        super().__init__()
        self.account = None
        self.email_actions = None
        self.dashboard = DashboardPage()
        self.base_actions = BaseActions()
        self.login_actions = LoginActions()
        self.admin_api = AdminApi(api)
        self.tcenter_page = TCentersPage()
        self.driver_actions = DriverActions()

    def _get_token(self):
        return self.driver_actions.get_item_from_local_storage('auth_token_default')

    def create_new_legislator(self):
        self.account = ModelBuilder.build_random_account()
        self.fill_name_field(self.account.en_name)
        self.upload_logo_file(self.account.logo)
        self.select_dropdown_county(self.account.country)
        self.fill_city_field(self.account.city)
        self.fill_address_field(self.account.address)
        self.fill_contact_name_field(self.account.contact_name)
        self.fill_phone_field(self.account.sub_number)
        self.fill_email_field(self.account.email)
        self.click_btn_create_legislator()
        self.base_actions.verify_expected_title(self.account.en_name, timeout=30)

    def register_legislator(self, permissions=None):
        self.login_actions.log_in_to_admin()
        if permissions:
            self.admin_api.put_permissions(self._get_token(), tcenter=False)
        self.dashboard.click_user_tab()
        self.base_actions.verify_expected_title(expected_title=Title.LEGISLATORS)
        self.click_btn_new_legislators()
        self.base_actions.verify_expected_title(expected_title=Title.NEW_LEGISLATOR)
        self.create_new_legislator()
        self.base_actions.verify_message(SuccessMessage.LEGISLATOR_CREATION)
        self.login_actions.log_out_user()
        self.email_actions = self.base_actions.activate_account(self.account.email)
        self.base_actions.verify_expected_title(expected_title=Title.SPA_SET_PASSWORD)
        return self

    def create_new_test_center(self, legislator):
        self.account = ModelBuilder.build_random_account()
        self.tcenter_page.fill_name_field(self.account.en_name)
        self.tcenter_page.select_dropdown_county(self.account.country)
        # TODO: Need to add method for adding category for specific country
        time.sleep(1)
        self.tcenter_page.select_dropdown_category(self.account.category)
        self.tcenter_page.fill_city_field(self.account.city)
        self.tcenter_page.fill_address_field(self.account.address)
        self.tcenter_page.fill_phone_field(self.account.sub_number)
        self.tcenter_page.select_legislator(legislator)
        self.tcenter_page.fill_tc_owner_name_field(self.account.contact_name)
        self.tcenter_page.fill_email_field(self.account.email)
        self.tcenter_page.click_btn_create_test_center()
        self.base_actions.verify_expected_title(self.account.en_name, timeout=30)
        return self.account

    def register_test_center(self, legislator_name='Autotest', permissions=None):
        self.login_actions.log_in_to_admin()
        if permissions:
            self.admin_api.put_permissions(self._get_token())
        self.dashboard.click_tcenter_tab(is_test_centers=True)
        self.tcenter_page.click_btn_new_test_center()
        self.base_actions.verify_expected_title(expected_title=Title.NEW_TEST_CENTER)
        self.account = self.create_new_test_center(legislator_name)
        self.base_actions.verify_message(SuccessMessage.TEST_CENTER_CREATION)
        self.login_actions.log_out_user()
        self.email_actions = self.base_actions.activate_account(self.account.email)
        self.base_actions.verify_expected_title(expected_title=Title.SPA_SET_PASSWORD)
        return self
