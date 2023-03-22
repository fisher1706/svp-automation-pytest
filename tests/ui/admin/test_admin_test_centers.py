import allure
import pytest

from src.ui.actions.admin_actions import AdminActions
from src.ui.actions.admin_tcenters_actions import AdminTCentersActions
from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.login_actions import LoginActions
from src.ui.pages.admin_tcenters import TCentersPage
from test_data.constants import Title, Countries
from test_data.validation_message import WarningMessage


@allure.feature('Test Centers tab as an Admin')
@pytest.mark.auth_suite
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.usefixtures("go_to_admin_auth_page")
class TestAdminTCenters:  # pylint: disable=attribute-defined-outside-init, unused-argument

    @pytest.fixture()
    def pre_test(self, api):
        self.admin_actions = AdminActions(api)
        self.login_actions = LoginActions()
        self.tcenter_page = TCentersPage()
        self.base_actions = BaseActions()

    @pytest.fixture()
    def pre_test_with_tcenter(self, api):
        self.admin_actions = AdminActions(api)
        self.login_actions = LoginActions()
        self.tcenter_page = TCentersPage()
        self.base_actions = BaseActions()
        self.admin_tcenters_actions = AdminTCentersActions(api)
        self.backgrounds_actions = BackgroundsActions(api)
        self.backgrounds_actions.create_entities_and_log_in(is_tcenter=True,
                                                            login=False)
        return self

    @allure.title('Check ability to add New Test Center with valid data')
    @allure.issue(url='https://is-takamol.atlassian.net/browse/PVPE-1556')
    @allure.testcase(url='https://takamolqa.qtestnet.com/p/101288/portal/project#tab=testdesign&object=1&id=42481746')
    @pytest.mark.skip
    def test_admin_register_test_center(self, pre_test):
        self.admin_actions.register_test_center()

    @allure.title('Check ability to add New Test Center with already existing email')
    @allure.issue(url='https://is-takamol.atlassian.net/browse/PVPE-1556')
    @allure.testcase(url='https://takamolqa.qtestnet.com/p/101288/portal/project#tab=testdesign&object=1&id=42481753')
    @pytest.mark.skip
    def test_admin_verify_email_warning_msg(self, pre_test_with_tcenter):
        email = pre_test_with_tcenter.backgrounds_actions.admin_api_actions.legislator_account.email
        self.admin_tcenters_actions.verify_error_msg_on_tc_create(msg=WarningMessage.EMAIL_IS_EXIST,
                                                                  is_email=True,
                                                                  email=email)

    @allure.title('Check an ability to see the specific message after filtration')
    def test_admin_verify_no_data_msg(self, pre_test):
        self.login_actions.log_in_to_admin()
        self.tcenter_page.visit()
        self.base_actions.verify_expected_title(expected_title=Title.TEST_CENTER)
        self.tcenter_page.select_filter_dropdown_county(Countries.MONTENEGRO)
        self.tcenter_page.click_btn_search()
        self.tcenter_page.verify_no_data_available(spa=False)

    @allure.title('Check an active Admin can view Edit Test Center form')
    def test_admin_can_view_edit_test_center_form(self, pre_test_with_tcenter):
        account = pre_test_with_tcenter.backgrounds_actions.admin_api_actions.tcenter_account
        self.login_actions.log_in_to_admin()
        self.tcenter_page.visit()
        self.base_actions.verify_expected_title(expected_title=Title.TEST_CENTER)
        self.tcenter_page.fill_filter_name_field(account.en_name)
        self.tcenter_page.click_btn_search()
        self.tcenter_page.select_view_of_last_entry()
        self.admin_tcenters_actions.verify_tcenters_view_fields(account)

    @allure.title('Check an active Admin can edit Test Center with valid data')
    @pytest.mark.skip('Todo')
    def test_admin_can_edit_test_center_with_valid_data(self, pre_test):
        pass

    @allure.title('Check an active Admin can not edit owner with registered email')
    @pytest.mark.skip('Todo')
    def test_admin_can_not_edit_owner_with_registered_email(self, pre_test):
        pass
