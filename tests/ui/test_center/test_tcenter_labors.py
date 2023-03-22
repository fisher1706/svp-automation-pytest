import allure
import pytest

from helpers.csv_helper import CSVHelper
from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.spa_actions import SPAActions
from test_data.constants import ExamResult


@allure.feature('Labors tab as Test Center Owner')
@pytest.mark.tc
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestTCenterLabors:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.base_actions = BaseActions()
        self.spa_actions = SPAActions(api)
        self.csv_helper = CSVHelper()
        self.spa_actions = SPAActions(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_tcenter=True,
                                                           is_tcenter_activate=True)

    @allure.title('Checking the ability to search entry by filters and clear filters on Labors table')
    def test_tc_search_entry_by_filters_on_labors_table(self, pre_test):
        self.spa_actions.verify_filters_on_labors_table()

    @allure.title('Checking counts on Labors tab')
    @pytest.mark.parametrize('exam_result', ExamResult.LIST_EXAM_RESULTS, ids=ExamResult.LIST_EXAM_RESULTS)
    def test_tc_counts_on_labors_tab(self, pre_test, exam_result):
        self.spa_actions.add_group(status=exam_result)
        self.spa_actions.verify_counts_on_labors_tab(exam_result)

    @allure.title('Checking all count on Labors tab')
    def test_tc_all_count_on_labors_tab(self, pre_test):
        self.spa_actions.verify_all_count_on_labors_tab()

    @allure.title('Checking pagination and search result value as Test Center on Labors tab')
    def test_tc_pagination_and_search_result_value(self, pre_test):
        self.spa_actions.verify_pagination_and_search_result_value()

    @allure.title('Checking the ability to edit email on Labors tab')
    def test_tc_edit_email_on_labors_tab(self, pre_test):
        self.spa_actions.edit_and_verify_email()

    @allure.title('Checking validation of edit email field on Labors tab')
    def test_tc_validation_edit_email_on_labors_tab(self, pre_test):
        self.spa_actions.verify_validation_edit_email_on_labors_tab(ExamResult.PENDING)
