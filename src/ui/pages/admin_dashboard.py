from selene import be
from selene.support.shared.jquery_style import s

from helpers.logger import yaml_logger
from src.ui.actions.driver_actions import DriverActions
from src.ui.pages.base import BasePage

logger = yaml_logger.setup_logging(__name__)


class DashboardPageLocators:  # pylint: disable=too-few-public-methods
    TAB_USERS = "//*[contains(text(),'Users')]"
    ROW_LEGISLATORS = "//a[text() = 'Legislators']"
    ROW_LABORS = "//*[contains(text(),'Labors')]"
    TAB_TEST_CENTERS = "//span[contains(@class, 'header-nav__link') and text() = 'Test Centers']"
    ROW_TEST_CENTERS = "//a[contains(@class, 'header-nav__link') and text() = 'Test Centers']"
    ROW_RESERVATIONS = "//a[text() = 'Reservations']"
    TAB_SETTINGS = "//*[contains(text(),'Settings')]"
    ROW_COUNTRY_SETTINGS = "//*[contains(text(),'Country settings')]"


class DashboardPage(BasePage, DashboardPageLocators):

    def __init__(self):
        super().__init__()
        self.page_url = ''
        self.driver_actions = DriverActions()

    def visit(self, url=None):  # pylint: disable=arguments-differ
        navigate_url = url if url else self.page_url
        self.driver_actions.visit(navigate_url)

    def click_user_tab(self, row=None):
        s(self.TAB_USERS).should(be.clickable).click()
        locator = self.ROW_LABORS if row else self.ROW_LEGISLATORS
        s(locator).should(be.clickable).click()

    def click_tcenter_tab(self, is_test_centers=False):
        s(self.TAB_TEST_CENTERS).should(be.clickable).click()
        locator = self.ROW_TEST_CENTERS if is_test_centers else self.ROW_RESERVATIONS
        s(locator).should(be.clickable).click()

    def click_settings_tab(self, row=None):
        s(self.TAB_SETTINGS).should(be.clickable).click()
        locator = self.ROW_COUNTRY_SETTINGS if row else f"//*[contains(text(), {row})]"
        s(locator).should(be.clickable).click()
