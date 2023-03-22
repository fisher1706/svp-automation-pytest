import time

import allure
import pytest
from selene.core import query
from selene.support.conditions import be
from selene.support.shared.jquery_style import s, ss

from helpers.decorators import for_all_methods
from test_data.constants import Labels


class SPALocators:
    BTN_CLEAR_FILTER = '.link'
    LAST_ENTRY = 'tr:nth-child(1) td'
    BTN_NEXT = '.next a'
    NO_DATA_AVAILABLE = '.modal-box--empty-text'
    USER_INFO = '.user-info__icon'
    CHANGE_PASSWORD = "//*[contains(text(),'Change Password')]"
    ACCOUNT_INFORMATION = "//*[contains(text(),'Account Information')]"
    LOGOUT = "//*[contains(text(),'Logout')]"


@for_all_methods(allure.step)
class SPA(SPALocators):
    def click_clear_filter_btn(self):
        s(self.BTN_CLEAR_FILTER).should(be.clickable).click()

    def get_info_of_last_entry(self, date=False):
        entry = None
        entry_info = {}
        for _ in range(5):
            entry = ss(self.LAST_ENTRY)
            if len(entry) > 1:
                break
            time.sleep(1)
        if not entry:
            pytest.fail('No data found')
        for item in entry:
            entry_info[item.get_attribute('data-label')] = item.get(query.text)
        if date:
            for key in entry_info.copy():
                if Labels.DATE in key:
                    entry_info[key] = entry_info[key].split('\n')[0]
        return entry_info

    def verify_active_next_btn(self):
        s(self.BTN_NEXT).should(be.clickable)

    def wait_until_no_data_available_disappear(self):
        s(self.NO_DATA_AVAILABLE).wait_until(be.not_.present)

    def click_on_profile_menu(self):
        s(self.USER_INFO).should(be.clickable).click()
        return self

    def click_change_password(self):
        s(self.CHANGE_PASSWORD).should(be.clickable).click()
        return self

    def click_account_info(self):
        s(self.ACCOUNT_INFORMATION).should(be.clickable).click()
        return self

    def click_logout_btn(self):
        s(self.LOGOUT).should(be.clickable).click()
        return self
