import allure
import pytest

from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.spa_actions import SPAActions
from test_data.constants import ExamResult


@allure.feature('Labors tab as Legislator')
@pytest.mark.legislator
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestLegislatorLabors:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.spa_actions = SPAActions(api)
        self.base_actions = BaseActions()
        self.backgrounds_actions = BackgroundsActions(api)
        self.backgrounds_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                            is_legislator_activate=True,
                                                            is_tcenter=True,
                                                            login_tcenter=False)

    @allure.title('Checking the ability to search entry by filters and clear filters on Labors table')
    def test_legislator_search_entry_by_filters_on_labors_table(self, pre_test):
        self.spa_actions.verify_filters_on_labors_table(tcenter=False)

    @allure.title('Checking counts on Labors tab')
    @pytest.mark.parametrize('exam_result', ExamResult.LIST_EXAM_RESULTS, ids=ExamResult.LIST_EXAM_RESULTS)
    def test_legislator_counts_on_labors_tab(self, pre_test, exam_result):
        self.spa_actions.add_group(status=exam_result)
        self.spa_actions.verify_counts_on_labors_tab(exam_result)

    @allure.title('Checking all count on Labors tab')
    @allure.issue(url='https://is-takamol.atlassian.net/browse/PVPE-1577',
                  name='[TC/Legislator] -uploaded labor(-s) displays on '
                       'a Uploaded Files Table only after reloading Page')
    @pytest.mark.skip
    def test_legislator_all_count_on_labors_tab(self, pre_test):
        self.spa_actions.verify_all_count_on_labors_tab()

    @allure.title('Checking pagination and search result value as Legislator on Labors tab')
    def test_legislator_pagination_and_search_result_value(self, pre_test):
        self.spa_actions.verify_pagination_and_search_result_value()

    @allure.title('Checking the ability to edit email on Labors tab')
    def test_legislator_edit_email_on_labors_tab(self, pre_test):
        self.spa_actions.edit_and_verify_email()

    @allure.title('Checking validation of edit email field on Labors tab')
    def test_legislator_validation_edit_email_on_labors_tab(self, pre_test):
        self.spa_actions.verify_validation_edit_email_on_labors_tab()
