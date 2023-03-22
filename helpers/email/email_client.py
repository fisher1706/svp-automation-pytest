import base64
import json
import re
import time
from urllib.parse import parse_qs, urlparse

from helpers.email.email_support import EmailSupport
from helpers.logger import yaml_logger

logger = yaml_logger.setup_logging(__name__)


class EmailClient(EmailSupport):

    def __init__(self):
        super().__init__()
        self._confirmation_url = None
        self._confirmation_code = None

    @property
    def confirmation_url(self):
        return self._confirmation_url

    @property
    def confirmation_code(self):
        return self._confirmation_code

    def find_email_by_recipient(self, recipient_email, attempts=30, raise_exception=True, mark_read=True):
        sleep_time = 2
        for attempt in range(attempts):
            time.sleep(sleep_time)
            logger.debug(f"Check mailbox {attempt} time(s)")
            self.get_unread_email_by_recipient(recipient=recipient_email, ignore_not_found=True)
            if self.email_id and mark_read:
                self.fetch_email_content()
                self.mark_email_read()
                break
        if not self.email_content:
            logger.debug(f"No unread emails in {attempts * sleep_time} sec. for: {recipient_email}")
            if raise_exception:
                raise Exception(f"No unread emails in {attempts * sleep_time} sec. for: {recipient_email}")

    def parse_confirmation_url(self):
        msg = str(self.email_content.body[1])
        link_pattern = re.compile(r'serif;"><a href=3D"(?P<url>https([^"]*))')
        found_url = link_pattern.search(msg)
        if found_url:
            found_url = found_url.group("url")
            self._confirmation_url = found_url.replace("=\n", "").replace("3D", "")
            logger.debug(f"Email confirmation URL: {self._confirmation_url}")
        else:
            raise Exception("Verification URL was not found in Confirmation email")

    def parse_confirmation_code(self):
        msg = str(self.email_content.body[1])
        code_pattern = re.compile(r'\D (\d{6})\D')
        found_code = code_pattern.search(msg)
        if found_code:
            self._confirmation_code = found_code.group(1)
            logger.debug(f"Confirmation code: {self._confirmation_code}")
        else:
            raise Exception("Verification URL was not found in Confirmation email")

    def is_confirmation_email_received(self, pass_no_email=False):
        if pass_no_email:
            assert not self.email_content, "Confirmation email was found in the mailbox"
        else:
            assert self.email_content, "Confirmation email was not found in the mailbox"

    def receive_confirmation_url(self, email_address):
        self.find_email_by_recipient(email_address)
        self.parse_confirmation_url()

    def get_confirmation_code(self, email_address):
        self.find_email_by_recipient(email_address)
        self.parse_confirmation_code()

    def get_confirmation_token(self):
        result = urlparse(self.confirmation_url)
        if "token=" in self.confirmation_url:
            token = parse_qs(result.query)['token'][0]
        else:
            base_string = parse_qs(result.query)['p'][0]
            first_url = json.loads(json.loads(base64.b64decode(base_string + '=='))["p"])["url"]
            second = parse_qs(urlparse(first_url).query)
            token = second['token'][0]
        return token
