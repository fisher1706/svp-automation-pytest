import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.spa_actions import SPAActions


@allure.feature('Upload Files tab as Legislator')
@pytest.mark.legislator
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestLegislatorUploadFiles:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           is_tcenter=True,
                                                           login_tcenter=False)

    @allure.title('C6488 Check the ability to add individual labor with valid data')
    def test_legislator_adding_individual_labor(self, pre_test):
        self.spa_actions.add_individual_labor(tcenter=False)

    @allure.title('C6090 Checking the ability to upload csv file with selected Test Center and Categories')
    @pytest.mark.parametrize('amount', [1, 5])
    def test_legislator_upload_csv_file_with_selected_category_and_tcenter(self, pre_test, amount):
        self.spa_actions.upload_group_of_labors(amount)

    @allure.title('C6087 C6088 C6089 Checking the ability to upload csv file without selected Category and Test Center')
    def test_legislator_upload_csv_file_without_selected_category_and_tcenter(self, pre_test):
        self.spa_actions.verify_upload_csv_file_without_selected_category_and_tcenter(tcenter=False)

    @allure.title('C9121 C9126 Checking the ability to search entry by filters and clear filters on Upload Files table')
    def test_legislator_search_entry_by_filters_on_upload_files_table(self, pre_test):
        self.spa_actions.verify_filters_on_uploads_tab()

    @allure.title('Checking pagination and search result value as Legislator on Upload tab')
    def test_legislator_upload_tab_pagination_and_search_result_value(self, pre_test):
        self.spa_actions.verify_total_amount_value()

    @allure.title('C9372 Checking the ability to search entry by filters and clear filters on Group table')
    def test_legislator_entry_search_entry_by_filters_on_upload_files_table(self, pre_test):
        self.spa_actions.verify_filters_on_upload_files(tcenter=False)

    @allure.title('Checking the ability to download csv sample')
    def test_legislator_download_csv_sample(self, pre_test, clear_temp_folder):
        self.spa_actions.verify_download_csv_sample()
