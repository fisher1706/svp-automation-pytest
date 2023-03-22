from src.ui.actions.base_actions import BaseActions
from src.ui.actions.spa_actions import SPAActions
from test_data.constants import Title


class SPATestCentersActions(SPAActions):
    def go_to_new_test_centers_form(self):
        self.spa_test_centers.visit()
        self.spa_test_centers.click_add_test_center_btn()
        self.base_actions.wait_spinners_to_disappear()
        self.base_actions.verify_expected_title(expected_title=Title.SPA_NEW_TEST_CENTER)

    def add_new_test_center(self, multiple_categories=False, warning=False):
        self.go_to_new_test_centers_form()
        self.fill_test_center_form(multiple_categories, warning)
        self.spa_test_centers.click_add_btn()

    def verify_adding_new_test_center(self, multiple_categories=False):
        self.spa_test_centers.visit()
        self.add_new_test_center(multiple_categories)
        self.base_actions.wait_spinners_to_disappear()
        # TODO: Need to debug verification alert message
        # self.base_actions.verify_message(SuccessMessage.TEST_CENTER_CREATION)
        self.spa_test_centers.verify_search_result_value(1)

    def verify_filters_and_clear_filters(self):
        self.spa_test_centers.visit()
        entry_info = self.get_info_of_last_entry()
        keys = list(entry_info.keys())
        self.verify_id_tcenters_tab(entry_info, keys[0])
        self.verify_name_tcenters_tab(entry_info, keys[1])
        self.verify_city_tcenters_tab(entry_info, keys[2])
        self.verify_test_center_owner(entry_info, keys[3])
        self.verify_test_center_status(entry_info, keys[4])
        self.base_actions.wait_spinners_to_disappear()
        self.click_clear_filter_btn()
        self.spa_test_centers.verify_disabling_filters_fields()

    def verify_view_edit_tcenter_form(self, is_legislator=True):
        self.spa_test_centers.visit()
        self.spa_test_centers.select_edit_of_last_entry()
        tcenter_account = self.admin_api_actions.tcenter_account
        BaseActions.verify_expected_result(self.spa_test_centers.get_name(), tcenter_account.en_name)
        BaseActions.verify_expected_result(self.spa_test_centers.get_official_contact_number(),
                                           tcenter_account.sub_number)
        self.spa_test_centers.verify_category(tcenter_account.category)
        if is_legislator:
            BaseActions.verify_expected_result(self.spa_test_centers.get_owner_name(),
                                               tcenter_account.contact_name)
            BaseActions.verify_expected_result(self.spa_test_centers.get_email(), tcenter_account.email)
        BaseActions.verify_expected_result(self.spa_test_centers.get_city(), tcenter_account.city)

    def verify_edit_tcenter_with_valid_data(self, is_legislator=True):
        self.spa_test_centers.visit()
        self.spa_test_centers.select_edit_of_last_entry()
        self.fill_test_center_form(is_legislator=is_legislator)
        self.spa_test_centers.click_edit_btn()
        self.base_actions.wait_spinners_to_disappear()
        # TODO: Need to debug verification alert message
        # self.base_actions.verify_message(SuccessMessage.TEST_CENTER_CREATION)
        entry_info = self.get_info_of_last_entry()
        keys = list(entry_info.keys())
        name = BaseActions.make_lower_case_first_char_of_second_name(entry_info[keys[1]])
        BaseActions.verify_expected_result(name, self.account_tcenter.en_name)
        BaseActions.verify_expected_result(entry_info[keys[2]], self.account_tcenter.city)
        BaseActions.verify_expected_result(entry_info[keys[3]], self.account_tcenter.contact_name)
        BaseActions.verify_expected_result(entry_info[keys[4]], 'Active')

    def verify_edit_owner_with_registered_email_and_duplicate_name(self, is_legislator=True):
        self.create_certain_number_of_test_centers(1)
        self.spa_test_centers.visit()
        self.spa_test_centers.select_edit_of_last_entry()
        self.fill_test_center_form(warning=True, is_legislator=is_legislator)
        self.spa_test_centers.click_edit_btn()
        self.spa_test_centers.verify_warning_duplicate_name()
        if is_legislator:
            self.spa_test_centers.verify_warning_duplicate_email()

    def verify_edit_empty_form_and_can_not_edit_country_field(self, is_legislator=True):
        self.spa_test_centers.visit()
        self.spa_test_centers.select_edit_of_last_entry()
        self.clear_all_fields(is_legislator)
        self.spa_test_centers.click_edit_btn()
        self.verify_empty_fields(is_legislator)
        self.spa_test_centers.verify_is_disabled_country_field()

    def verify_view_test_center_information(self):
        self.spa_test_centers.visit()
        self.spa_test_centers.select_view_of_last_entry()
        self.base_actions.wait_spinners_to_disappear()
        self.base_actions.verify_expected_title(Title.SPA_TEST_CENTER_INFORMATION)
        tcenter_account = vars(self.admin_api_actions.tcenter_account).values()
        for item in self.spa_test_centers.get_tc_info():
            BaseActions.verify_expected_result(item, tcenter_account, condition=True)

    def verify_removing_tcenter(self):
        self.spa_test_centers.visit()
        self.spa_test_centers.select_remove_of_last_entry()
        self.spa_test_centers.click_confirm_btn()
        self.base_actions.wait_spinners_to_disappear()
        # TODO: Need to debug verification alert message
        # self.base_actions.verify_message(SuccessMessage.TEST_CENTER_REMOVE)
        self.verify_no_data_available()
