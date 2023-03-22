import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.spa_test_centers_actions import SPATestCentersActions


@allure.feature('Test Centers tab as Test Center Owner')
@pytest.mark.tc
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestTCenterTestCenters:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture(autouse=True)
    def pre_test(self, api):
        self.spa_test_centers_actions = SPATestCentersActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_test_centers_actions.auth_api_actions,
                                                           is_tcenter=True,
                                                           is_tcenter_activate=True)

    @allure.title('C9183 C9184 Checking the ability to search entry by filters and clear filters on Test Centers tab')
    def test_tc_check_filters_and_clear_filters_test_centers_tab(self):
        self.spa_test_centers_actions.verify_filters_and_clear_filters()

    @allure.title('C11918 Checking that Test Center Owner can view Edit Test Center form')
    def test_tc_can_view_edit_tcenter_form(self):
        self.spa_test_centers_actions.verify_view_edit_tcenter_form(is_legislator=False)

    @allure.title('C11920 Checking that Test Center Owner can edit a Test Center with valid data')
    def test_tc_can_edit_tcenter_with_valid_data(self):
        self.spa_test_centers_actions.verify_edit_tcenter_with_valid_data(is_legislator=False)

    @allure.title('C12027 Checking that Test Center Owner is not able to change test center Name to Name which already '
                  'exists')
    def test_tc_can_not_edit_owner_name_which_already_exists(self):
        self.spa_test_centers_actions.verify_edit_owner_with_registered_email_and_duplicate_name(is_legislator=False)

    @allure.title('C11922 Checking that Test Center Owner can edit test center with invalid data')
    def test_tc_can_edit_test_center_with_invalid_data(self):
        self.spa_test_centers_actions.spa_test_centers.visit()
        self.spa_test_centers_actions.spa_test_centers.select_edit_of_last_entry()
        self.spa_test_centers_actions.verify_wrong_data_on_edit_form(is_add_btn=False, is_legislator=False)

    @allure.title('C11923 C11924 Checking that Test Center Owner can not edit test center with empty form and can not '
                  'edit country field')
    def test_tc_edit_test_center_with_empty_form_and_can_not_edit_country_field(self):
        self.spa_test_centers_actions.verify_edit_empty_form_and_can_not_edit_country_field(is_legislator=False)

    @allure.title('C9281 Checking that Test Center Owner can view Test Center information')
    def test_tc_can_view_test_center_information(self):
        self.spa_test_centers_actions.verify_view_test_center_information()
