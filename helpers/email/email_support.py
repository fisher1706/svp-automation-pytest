import email
import imaplib
import socket

from helpers.logger import yaml_logger
from test_data.constants import EmailConst
from test_data.models.model_builder import ModelBuilder

logger = yaml_logger.setup_logging(__name__)

MAIL_LOGIN = 'qiwaqa@p2h.com'
MAIL_PASS = 'evevTSbfuZJ7B5'


class EmailSupport:

    def __init__(self):
        self.email_content = None
        self.imap_session = None
        self.email_id = None
        self.init_imap_session(EmailConst.IMAP_DOMAIN)

    def init_imap_session(self, imap_domain):
        """
        Init IMAP session for provided domain
        """
        try:
            self.imap_session = imaplib.IMAP4_SSL(imap_domain)
            typ, _ = self.imap_session.login(MAIL_LOGIN, MAIL_PASS)
            logger.debug("IMAP session successfully created")
            if typ != EmailConst.STATUS_OK:
                raise EnvironmentError("Not able to sign in to mailbox!")
        except socket.gaierror:
            logger.info(f"Socket error {socket.gaierror}")
            self.imap_session = None
        except Exception as ex:  # pylint: disable=broad-except
            logger.error("IMAP session creation failed")
            logger.error(ex)

    def get_unread_emails(self):
        id_list = None
        if self.imap_session:
            self.imap_session.select(EmailConst.INBOX_FOLDER, readonly=True)

            typ, data = self.imap_session.search(None, f"({EmailConst.UNSEEN_EMAILS})")
            if typ != EmailConst.STATUS_OK:
                raise FileNotFoundError("Requester Inbox folder was not found in the mailbox")

            unread_ids = data[0]
            id_list = unread_ids.split()

        return id_list

    def get_unread_email_by_recipient(self, recipient, ignore_not_found=False):
        self.email_id = None
        if not self.imap_session:
            raise AttributeError("IMAP session was not initiated")
        self.imap_session.select(EmailConst.INBOX_FOLDER, readonly=True)
        typ, data = self.imap_session.search(None, f'(TO "{recipient}" {EmailConst.UNSEEN_EMAILS})')
        if typ != EmailConst.STATUS_OK:
            raise FileNotFoundError("Requester Inbox folder was not found in the mailbox")
        self.email_id = data[0]
        if len(data[0]) == 0:
            self.email_id = None
            if not ignore_not_found:
                raise FileNotFoundError(f"No unread emails were found in the mailbox for {recipient}")
        return self

    def fetch_email_content(self):
        self.email_content = None
        _, data = self.imap_session.fetch(self.email_id, EmailConst.EMAIL_FORMAT)
        email_body = data[0][1]
        mail = email.message_from_bytes(email_body)
        self.email_content = ModelBuilder.build_email(mail)

    def mark_email_read(self):
        self.imap_session.select(EmailConst.INBOX_FOLDER, readonly=False)
        self.imap_session.store(self.email_id, EmailConst.ADD_FLAG, EmailConst.FLAG_SEEN)
        self.imap_session.select(EmailConst.INBOX_FOLDER, readonly=True)

    def logout_imap_session(self):
        if self.imap_session.state is EmailConst.IMAP_SESSION_ACTIVE:
            logger.debug("Complete session deactivation")
            self.imap_session.close()
            self.imap_session.logout()
        else:
            logger.debug("Reject session deactivation")
