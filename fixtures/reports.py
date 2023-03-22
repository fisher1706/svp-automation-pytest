import pytest
from _pytest.config import Config
from requests import Session

from helpers.discord_report import TestReportManager


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_report_teststatus(report, config: Config) -> None:
    yield
    if report.when == 'setup' and report.passed is True:
        config.setup_duration = report.duration
    if report.when == 'call' or report.passed is False:
        test_report = TestReportManager()
        if test_report.define_webhook_url():
            test_report.create_message_add_to_report(report, config)


def pytest_sessionfinish(session: Session, exitstatus):  # pylint: disable=unused-argument
    test_report = TestReportManager()
    if test_report.define_webhook_url():
        test_report.send_report()
        test_report.send_duration_report()
        test_report.send_count_report()
