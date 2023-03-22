import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.spa_test_centers_actions import SPATestCentersActions


@allure.feature('Test Centers tab as Legislator')
@pytest.mark.legislator
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestLegislatorTestCenters:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.spa_test_centers_actions = SPATestCentersActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_test_centers_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           login_tcenter=False)

    @pytest.fixture()
    def pre_test_multiple_categories(self, api):
        self.spa_test_centers_actions = SPATestCentersActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_test_centers_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           login_tcenter=False,
                                                           is_multiple_categories=True)

    @pytest.fixture()
    def pre_test_with_tcenter(self, api):
        self.spa_test_centers_actions = SPATestCentersActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_test_centers_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           is_tcenter=True,
                                                           login_tcenter=False)

    @pytest.fixture()
    def pre_test_with_tcenter_and_login(self, api):
        self.spa_test_centers_actions = SPATestCentersActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_test_centers_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           is_tcenter=True,
                                                           is_tcenter_activate=True)

    @allure.title('C9169 Checking the ability to add new Test Center with valid data')
    def test_legislator_check_ability_to_add_new_tcenter_with_valid_data(self, pre_test):
        self.spa_test_centers_actions.verify_adding_new_test_center()

    @allure.title('C9181 Checking the ability to select one/multiple categories')
    def test_legislator_check_ability_to_select_one_multiple_categories(self, pre_test_multiple_categories):
        self.spa_test_centers_actions.verify_adding_new_test_center(multiple_categories=True)

    @allure.title('C9183 C9184 Checking the ability to search entry by filters and clear filters on Test Centers tab')
    def test_legislator_check_filters_and_clear_filters_test_centers_tab(self, pre_test_with_tcenter):
        self.spa_test_centers_actions.verify_filters_and_clear_filters()

    @allure.title('C9180 Checking that there is no ability to add new Test Center with empty form')
    def test_legislator_add_new_tcenter_with_empty_form(self, pre_test):
        self.spa_test_centers_actions.go_to_new_test_centers_form()
        self.spa_test_centers_actions.spa_test_centers.click_add_btn()
        self.spa_test_centers_actions.verify_empty_fields()

    @allure.title('C9171 C9179 Checking the ability to add owner with registered email')
    def test_legislator_check_ability_to_add_owner_with_registered_email(self, pre_test_with_tcenter):
        self.spa_test_centers_actions.add_new_test_center(warning=True)
        self.spa_test_centers_actions.spa_test_centers.verify_warning_duplicate_name()
        self.spa_test_centers_actions.spa_test_centers.verify_warning_duplicate_email()

    @allure.title('C9182 Checking the ability to see the list of Test Centers, pagination')
    def test_legislator_check_ability_see_the_list_of_test_centers_pagination(self, pre_test):
        self.spa_test_centers_actions.create_certain_number_of_test_centers(11)
        self.spa_test_centers_actions.spa_test_centers.visit()
        self.spa_test_centers_actions.spa_test_centers.verify_search_result_value(11)
        self.spa_test_centers_actions.verify_active_next_btn()

    @allure.title('C9178 Checking the ability to add new Test Center with invalid data')
    def test_legislator_check_ability_to_add_new_tcenter_with_invalid_data(self, pre_test):
        self.spa_test_centers_actions.go_to_new_test_centers_form()
        self.spa_test_centers_actions.verify_wrong_data_on_edit_form()

    @allure.title('C9189 Checking that Legislator can view Edit Test Center form')
    def test_legislator_can_view_edit_tcenter_form(self, pre_test_with_tcenter):
        self.spa_test_centers_actions.verify_view_edit_tcenter_form()

    @allure.title('C9190 Checking that Legislator can edit a Test Center with valid data')
    def test_legislator_can_edit_tcenter_with_valid_data(self, pre_test_with_tcenter):
        self.spa_test_centers_actions.verify_edit_tcenter_with_valid_data()

    @allure.title('C9191 Checking that Legislator can not edit owner with registered email and duplicate name')
    def test_legislator_can_not_edit_owner_with_registered_email_and_duplicate_name(self, pre_test_with_tcenter):
        self.spa_test_centers_actions.verify_edit_owner_with_registered_email_and_duplicate_name()

    @allure.title('C11914 Checking that Legislator can edit test center with invalid data')
    def test_legislator_can_edit_test_center_with_invalid_data(self, pre_test_with_tcenter):
        self.spa_test_centers_actions.spa_test_centers.visit()
        self.spa_test_centers_actions.spa_test_centers.select_edit_of_last_entry()
        self.spa_test_centers_actions.verify_wrong_data_on_edit_form(is_add_btn=False)

    @allure.title('C9193 C9194 Checking that Legislator can not edit test center with empty form and can not edit '
                  'country field')
    def test_legislator_edit_test_center_with_empty_form_and_can_not_edit_country_field(self, pre_test_with_tcenter):
        self.spa_test_centers_actions.verify_edit_empty_form_and_can_not_edit_country_field()

    @allure.title('C9281 Checking that Legislator can view Test Center information')
    def test_legislator_can_view_test_center_information(self, pre_test_with_tcenter):
        self.spa_test_centers_actions.verify_view_test_center_information()

    @allure.title('C9281 Checking that Legislator can delete a Test Center')
    def test_legislator_can_delete_test_center(self, pre_test_with_tcenter):
        self.spa_test_centers_actions.verify_removing_tcenter()

    @allure.title('C9282 Checking that Legislator can view the list of upload files of deleted Test Center')
    def test_legislator_can_view_the_list_of_upload_files_of_deleted_test_center(self, pre_test_with_tcenter_and_login):
        self.spa_test_centers_actions.upload_group_of_labors()
        self.spa_test_centers_actions.login_actions.log_out_user()
        self.spa_test_centers_actions.admin_api_actions.activate_permission(tcenter=False)
        self.spa_test_centers_actions.login_actions.log_in_to_spa(
            self.spa_test_centers_actions.admin_api_actions.tcenter_account)
        self.spa_test_centers_actions.verify_removing_tcenter()
        self.spa_test_centers_actions.spa_upload.visit()
        self.spa_test_centers_actions.spa_upload.verify_added_labors()
        self.spa_test_centers_actions.spa_upload.verify_search_result_value('1')
