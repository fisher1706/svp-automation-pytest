from datetime import datetime

import allure
import pytest
from allure_commons.types import AttachmentType
from selene.support.shared import browser
from selenium import webdriver
from selenium.common import WebDriverException
from selenium.webdriver.remote.remote_connection import RemoteConnection
from urllib3.exceptions import MaxRetryError
from webdriver_manager.chrome import ChromeDriverManager

from helpers.logger import yaml_logger
from helpers.logger.yaml_logger import setup_logging
from src.ui.actions.driver_actions import DriverActions
from test_data.constants import SupportedBrowser, DirPath

logger = yaml_logger.setup_logging(__name__)


@pytest.fixture(autouse=True)
def setup_driver(request):
    webdriver_main = None
    setup_logging()
    browser.config.timeout = 30
    grid_url = request.config.getoption("grid_url")
    browser_name = request.config.getoption("browser_name")
    environment_url = request.config.getoption("environment_url")
    admin_environment_url = request.config.getoption("admin_environment_url")
    if 'localhost' in grid_url:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {'download.default_directory': f'{DirPath.TEMP_FOLDER}'})
        options.set_capability('goog:loggingPrefs', {"performance": "ALL"})
        options.headless = False
        if options.headless:
            options.add_argument("--window-size=2560x1600")
        webdriver_main = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    else:
        if browser_name not in SupportedBrowser.VERSION:
            raise NameError(f"Defined browser name '{browser_name}' is not supported")

        capabilities = {
            "browserName": browser_name,
            "browserVersion": SupportedBrowser.VERSION[browser_name],
            "applicationCacheEnabled": False,
            "javascriptEnabled": True,
            "acceptSslCerts": True,
            "sessionTimeout": "60m",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": False
            },
            "download.default_directory": f'{DirPath.TEMP_FOLDER}',
            "goog:loggingPrefs": {"performance": "ALL"}
        }
        try:
            webdriver_main = webdriver.Remote(command_executor=RemoteConnection(grid_url),
                                              desired_capabilities=capabilities)
        except MaxRetryError as ex:
            pytest.exit(f"Unable to connect to Remote Webdriver: {ex.reason}")
        except WebDriverException as ex:
            pytest.exit(f"Unable to connect to Remote Webdriver: {ex.msg}")

    webdriver_main.delete_all_cookies()
    webdriver_main.maximize_window()
    browser.set_driver(webdriver_main)
    DriverActions(browser, environment_url, admin_environment_url)
    yield browser
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.outcome == 'failed':
        timestamp = datetime.now()
        screenshot = browser.last_screenshot
        if screenshot:
            with open(screenshot, 'rb') as file:
                img = file.read()
            allure.attach(img, name=f"{timestamp}.png",
                          attachment_type=AttachmentType.PNG)
    setattr(item, "rep_" + rep.when, rep)
