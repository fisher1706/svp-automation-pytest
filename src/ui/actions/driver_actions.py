import json
import re
import time

import allure
from selene.support.shared import browser
from selenium.webdriver.common.action_chains import ActionChains

from helpers.decorators import for_all_methods
from helpers.singleton import SingletonMeta


@for_all_methods(allure.step)
class DriverActions(metaclass=SingletonMeta):
    def __init__(self, driver: browser = None, environment_url: str = None, admin_environment_url: str = None):
        super().__init__()
        self.shared_driver = driver
        self.shared_driver.driver.implicitly_wait(1)
        self.admin_environment_url = admin_environment_url
        self.environment_url = environment_url
        self.action_chains = ActionChains(self.shared_driver.driver)

    def visit(self, url: str, admin: bool = None):
        env_url = self.environment_url if not admin else self.admin_environment_url
        navigate_url = url if url.startswith("https") else env_url + url
        self.shared_driver.open(navigate_url)
        return self

    def get_url(self):
        return self.shared_driver.driver.current_url

    def refresh_page(self):
        self.shared_driver.driver.refresh()
        return self

    def set_cookie(self, cookie: dict):
        normalized_cookie = None
        for cookie_name, cookie_value in cookie.items():
            normalized_cookie = {
                'name': cookie_name,
                'value': cookie_value,
            }
        self.shared_driver.driver.add_cookie(normalized_cookie)
        return self

    def clear_all_cookies(self):
        self.shared_driver.driver.delete_all_cookies()
        return self

    def switch_to_tab(self, tab_id):
        self.shared_driver.driver.switch_to.window(self.shared_driver.driver.window_handles[tab_id])
        return self

    def switch_to_second_tab_with_timeout(self):
        attempts = 5
        for _ in range(attempts):
            available_tabs = len(self.shared_driver.driver.window_handles)
            if available_tabs > 1:
                self.switch_to_tab(1)
            else:
                time.sleep(1)
        return self

    def close_tab(self):
        available_tabs = len(self.shared_driver.driver.window_handles)
        if available_tabs > 1:
            self.shared_driver.close_current_tab()
        return self

    def switch_to_iframe(self, frame_locator):
        # TODO: Find possibility for wait load iframe
        time.sleep(2)
        self.shared_driver.driver.switch_to.frame(frame_locator)

    def exit_iframe(self):
        self.shared_driver.switch_to.default_content()

    def remove_item_from_local_storage(self, key):
        self.shared_driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def get_item_from_local_storage(self, key):
        return self.shared_driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def clear_local_storage(self):
        self.shared_driver.execute_script("window.localStorage.clear();")

    def get_otp_code_from_network(self):
        logs_raw = self.shared_driver.driver.get_log("performance")
        logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

        def log_filter(log_):
            return (
                    log_["method"] == "Network.responseReceived" and "json" in log_["params"]["response"]["mimeType"]
            )

        for log in filter(log_filter, logs):
            request_id = log["params"]["requestId"]
            if 'login?locale=en' in log["params"]["response"]["url"]:
                response = self.shared_driver.driver.execute_cdp_cmd("Network.getResponseBody",
                                                                     {"requestId": request_id})['body']
                return re.findall(r'\d{6}', response)[0]
