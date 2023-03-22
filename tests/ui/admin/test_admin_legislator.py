import allure
import pytest

from src.ui.actions.admin_actions import AdminActions


@allure.feature('Legislator tab as an Admin')
@pytest.mark.auth_suite
@pytest.mark.daily
@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.usefixtures("go_to_admin_auth_page")
class TestAdminLegislator:  # pylint: disable=attribute-defined-outside-init

    @pytest.fixture(autouse=True)
    def pre_test(self, api):
        self.admin_actions = AdminActions(api)

    @allure.title('Check register test center')
    def test_admin_register_legislator(self):
        self.admin_actions.register_legislator()
