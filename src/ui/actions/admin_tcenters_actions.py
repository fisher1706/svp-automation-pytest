import allure

from helpers.decorators import for_all_methods
from src.ui.actions.admin_actions import AdminActions
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.login_actions import LoginActions
from src.ui.pages.admin_legislators import LegislatorsPage
from src.ui.pages.admin_tcenters import TCentersPage
from test_data.constants import Title
from test_data.models.model_builder import ModelBuilder


@for_all_methods(allure.step)
class AdminTCentersActions(LegislatorsPage, TCentersPage):

    def __init__(self, api):
        super().__init__()
        self.account = None
        self.admin_actions = AdminActions(api)
        self.login_actions = LoginActions()
        self.base_actions = BaseActions()

    def verify_error_msg_on_tc_create(self, legislator='Autotest',
                                      msg='',
                                      is_name=False,
                                      name='',
                                      is_email=False,
                                      email=''):
        self.account = ModelBuilder.build_random_account()
        self.login_actions.log_in_to_admin()
        self.visit()
        self.click_btn_new_test_center()
        self.base_actions.verify_expected_title(expected_title=Title.NEW_TEST_CENTER)
        name = name if is_name else self.account.en_name
        self.fill_name_field(name)
        self.select_dropdown_county(self.account.country)
        self.select_dropdown_category(self.account.category)
        self.fill_city_field(self.account.city)
        self.fill_address_field(self.account.address)
        self.fill_phone_field(self.account.sub_number)
        self.select_legislator(legislator)
        self.fill_tc_owner_name_field(self.account.contact_name)
        email = email if is_email else self.account.email
        self.fill_email_field(email)
        self.click_btn_create_test_center()
        self.base_actions.verify_message(expected_message=msg)

    def verify_tcenters_view_fields(self, account):
        self.verify_name_in_title(account.en_name)
        self.verify_name(account.en_name)
        self.verify_adress(account.address)
        self.verify_category(account.category)
        self.verify_country(account.country)
        self.verify_city(account.city)
        self.verify_status()
        self.verify_phone_number(account.phone_number)
        self.verify_legislator()
        self.verify_tcenter_owner_name(account.contact_name)
        self.verify_tcenter_owner_email(account.email)
