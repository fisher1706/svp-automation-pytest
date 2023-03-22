import allure
import pytest

from src.api.features.spa_api import SPAApi
from src.ui.actions.backgrounds import BackgroundsActions
from src.ui.actions.spa_actions import SPAActions


@allure.feature('Reports tab as Test Center Owner')
@pytest.mark.tc
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.usefixtures('logout_after_test')
class TestTCenterReports:  # pylint: disable=unused-argument, attribute-defined-outside-init

    @pytest.fixture()
    def pre_test(self, api):
        self.spa_actions = SPAActions(api)
        self.spa_api = SPAApi(api)
        self.background_actions = BackgroundsActions(api)
        self.background_actions.create_entities_and_log_in(self.spa_actions.auth_api_actions,
                                                           is_legislator_activate=True,
                                                           is_tcenter=True,
                                                           login_tcenter=False)

    @allure.title('Check the ability to download certificate as a Test Center')
    def test_tc_download_certificate(self, pre_test, clear_temp_folder):
        self.spa_actions.verify_download_certificate_report(is_reports_tab=True)

    @allure.title('Check the ability to download report as a Test Center')
    def test_tc_download_report(self, pre_test, clear_temp_folder):
        self.spa_actions.verify_download_certificate_report(is_certificate=False, is_reports_tab=True)

    @allure.title('Check the ability to download report on view payment details as a Test Center')
    def test_tc_download_report_on_view_payment_details(self, pre_test, clear_temp_folder):
        self.spa_actions.verify_download_certificate_report(is_certificate=False,
                                                            is_reports_tab=True,
                                                            is_view_payment=True)
