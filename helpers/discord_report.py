import os
from time import gmtime
from time import strftime
from typing import List

from _pytest.config import Config
from discord import Webhook, RequestsWebhookAdapter

from helpers.decorators import singleton
from test_data.dataset import DISCORD_HOOKS


@singleton
class TestReportManager:
    GREEN_CIRCLE = ':green_circle:'
    SCROLL = ':scroll:'
    RED_CIRCLE = ':red_circle:'
    BLUE_CIRCLE = ':blue_circle:'
    YELLOW_CIRCLE = ':yellow_circle:'
    WHITE_CHECK_MARK = ':white_check_mark:'
    BANGBANG = ':bangbang:'
    RERUN = ':infinity:'
    MARK = ':bangbang:'
    MESSAGE_SIZE = 2000

    def __init__(self):
        self.__report: List = []
        self.__suite_name = os.getenv('SUITE_NAME')
        self.__project_env = os.getenv("PROJECT_ENV")
        self.__webhook_url = None
        self.__total_duration: int = 0
        self.__failed_tests: int = 0
        self.__skipped_tests: int = 0
        self.__passed_tests: int = 0
        self.__rerun_tests: int = 0
        self.__with_stacktrace = False
        self.__failed_only = True

    def define_webhook_url(self):
        try:
            self.__webhook_url = DISCORD_HOOKS[self.__project_env][self.__suite_name]
        except KeyError:
            self.__webhook_url = None
        return self.__webhook_url

    @staticmethod
    def get_webhook(webhook: str) -> Webhook:
        return Webhook.from_url(webhook, adapter=RequestsWebhookAdapter())

    @staticmethod
    def get_suite_name(config: Config) -> str:
        return config.option.markexpr

    @staticmethod
    def get_skipped_reason(report) -> str:
        return report.longrepr[2].split('Skipped:')[1]

    @staticmethod
    def get_setup_duration(config: Config) -> int:
        try:
            return config.setup_duration
        except AttributeError:
            return 0

    @staticmethod
    def format_duration(duration: float) -> str:
        return strftime("%H:%M:%S", gmtime(round(duration, 2)))

    @staticmethod
    def get_call_duration(report):
        try:
            return report.duration
        except AttributeError:
            return 0

    def get_test_duration(self, config: Config, report) -> float:
        setup_duration = self.get_setup_duration(config)
        test_duration = self.get_call_duration(report)
        total_duration = setup_duration + test_duration
        return total_duration

    @staticmethod
    def get_test_name(report) -> str:
        return f"{report.head_line.split('.')[0]} :: {report.head_line.split('.')[1]}"

    @staticmethod
    def get_error_trace(report) -> str:
        try:
            trace = report.longrepr.reprtraceback.reprentries[0].lines
            normalized_trace = '```diff\n'
            for trace_line in trace:
                normalized_trace += f'-{trace_line}\n'
            message = report.longrepr.reprcrash.message
        except AttributeError:
            return 'Failed to get trace'
        return normalized_trace + message + '```'

    def force_message_split(self, report_text: str) -> List[str]:
        chunks, chunk_size = len(report_text), self.MESSAGE_SIZE
        return [report_text[i:i + chunk_size] for i in range(0, chunks, chunk_size)]

    def send_message(self, report_text: str):
        reports = self.force_message_split(report_text)
        webhook = self.get_webhook(self.__webhook_url)
        for report in reports:
            webhook.send(report, username=self.__suite_name)

    def check_is_not_empty_report(self) -> bool:
        if self.__report:
            return True
        self.send_message(f'{self.BLUE_CIRCLE} There is no report for tests')
        return False

    def send_duration_report(self):
        message = f'Total suite duration: `{self.format_duration(self.__total_duration)}`'
        self.send_message(message)

    def build_title(self):
        if self.__failed_tests > 0:
            title_text = "FAILED RUN"
            title_side = (("-" * 40), self.BANGBANG)
        else:
            title_text = "SUCCESS RUN"
            title_side = (("-" * 40), self.WHITE_CHECK_MARK)
        return f'{"".join(title_side)} {title_text} {"".join(title_side[::-1])}\n'

    # pylint: disable=broad-except
    def send_report(self):
        if self.check_is_not_empty_report():
            try:
                messages_to_send = self.build_title()
                total_message_amount = len(self.__report)
                for i in range(total_message_amount):
                    current_message = self.__report[i]
                    current_length = len(messages_to_send + current_message)
                    if current_length < self.MESSAGE_SIZE:
                        messages_to_send += current_message
                    if current_length > self.MESSAGE_SIZE:
                        self.send_message(messages_to_send)
                        messages_to_send = current_message

                self.send_message(messages_to_send)
            except Exception as exception:
                self.send_message(f'{self.MARK} Failed to send test report due to {exception}')

    def add_message(self, outcome: str):
        self.__report.append(outcome)

    def get_failed_message(self, report, str_duration: str, test_name: str, is_rerun: bool = True) -> str:
        marker = self.RERUN if is_rerun else self.RED_CIRCLE
        test_trace = ""
        if self.__with_stacktrace:
            test_trace = f"{self.SCROLL} {self.get_error_trace(report)}\n"
        return f"{marker} :: `{str_duration}` :: {test_name}\n{test_trace}"

    def send_count_report(self):
        message = f'{self.BLUE_CIRCLE} Environment: {self.__project_env} \n' \
                  f'{self.GREEN_CIRCLE} Passed: {self.__passed_tests} \n' \
                  f'{self.RED_CIRCLE} Failed: {self.__failed_tests} \n' \
                  f'{self.YELLOW_CIRCLE} Skipped: {self.__skipped_tests} \n' \
                  f'{self.RERUN} Rerun: {self.__rerun_tests}'
        self.send_message(message)

    def create_message_add_to_report(self, report, config: Config):
        test_name = self.get_test_name(report)
        test_duration = self.get_test_duration(config, report)
        str_duration = self.format_duration(test_duration)

        self.__total_duration += test_duration
        message = ""
        if report.outcome == 'failed':
            message = self.get_failed_message(report, str_duration, test_name, False)
            self.__failed_tests += 1
        elif report.outcome == 'skipped':
            if not self.__failed_only:
                message = f"{self.YELLOW_CIRCLE} :: f`00:00:00` :: {test_name} {self.SCROLL} " \
                          f"{self.get_skipped_reason(report)}\n"
            self.__skipped_tests += 1
        elif report.outcome == 'rerun':
            message = self.get_failed_message(report, str_duration, test_name)
            self.__rerun_tests += 1
        elif report.outcome == 'passed':
            if not self.__failed_only:
                message = f"{self.GREEN_CIRCLE} :: `{str_duration}` :: {test_name}\n"
            self.__passed_tests += 1
        else:
            raise KeyError('Unexpected pytest report status')

        self.add_message(message)
