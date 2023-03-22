import os.path


class UserInfo:
    DEFAULT_LOGIN = 'admin@gmail.com'
    INVALID_LOGIN = 'test@gmail.com'
    DEFAULT_PASSWORD = 'Password#1'
    CHANGED_PASSWORD = 'Password#1!#'
    INVALID_PASSWORD = 'Invalid#1'
    TC_LOGIN = 'auto-ppuliw9p@qa.qiwa.tech'
    TC_NAME = 'Autotest nkmvrorv'
    LEGISLATOR_LOGIN = 'auto-unmlm1d2@qa.qiwa.tech'


class UserType:
    LEGISLATOR = {'type': 'spa user type', 'text': 'Legislator'}
    TEST_CENTER_OWNER = {'type': 'spa user type', 'text': 'Test Center Owner'}


class SupportedBrowser:
    VERSION = {
        "chrome": "107.0",
        "firefox": "93.0",
        "opera": "80.0"
    }


class Title:
    SIGN_IN = {'type': 'header', 'text': 'Sign in'}
    LEGISLATORS = {'type': 'header', 'text': 'Legislators'}
    NEW_LEGISLATOR = {'type': 'header', 'text': 'New Legislator'}
    NEW_TEST_CENTER = {'type': 'header', 'text': 'New Test Center'}
    TEST_CENTER = {'type': 'header', 'text': 'Test Centers'}
    SPA_SIGN_IN = {'type': 'spa login', 'text': 'Welcome to International SVP!'}
    SPA_SET_PASSWORD = {'type': 'spa login', 'text': 'Set Password'}
    CARD_DETAILS = {'type': 'header payment', 'text': 'PLEASE ENTER YOUR CARD DETAILS TO A PURCHASE'}
    UPLOADED_FILES = {'type': 'spa', 'text': 'Uploaded Files'}
    ADD_GROUP = {'type': 'modal', 'text': 'Add Group'}
    TRANSACTION_HISTORY = {'type': 'spa', 'text': 'Transaction History'}
    REPORTS = {'type': 'spa', 'text': 'Reports'}
    CHECK_VALIDITY = {'type': 'spa', 'text': 'Check Validity'}
    GROUP = {'type': 'spa', 'text': 'GROUP {}'}
    PAYMENT_CONFIRMATION = {'type': 'spa', 'text': 'Payment Confirmation'}
    PAYMENT = {'type': 'spa', 'text': 'Payment'}
    ADD_INDIVIDUAL = {'type': 'modal', 'text': 'Add Individual'}
    SPA_NEW_TEST_CENTER = {'type': 'spa', 'text': 'New Test Center'}
    SPA_TEST_CENTER_INFORMATION = {'type': 'spa', 'text': 'Test Center Information'}
    SPA_EDIT_TEST_CENTER = {'type': 'spa', 'text': 'EDIT TEST CENTER'}
    SPA_ACCOUNT_INFORMATION = {'type': 'spa', 'text': 'Account Information'}
    SPA_CHANGE_PASSWORD = {'type': 'spa login', 'text': 'Change Password'}
    SPA_PROFESSIONAL_ACCREDITATION_PROGRAM = {'type': 'home', 'text': 'Professional Accreditation Program'}


class DirPath:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEST_FILES = os.path.join(BASE_DIR, 'test_files')
    PNG_FILE = os.path.join(TEST_FILES, 'valid_3.png')
    CSV = os.path.join(TEST_FILES, 'sample_attributes.csv')
    CSV_5 = os.path.join(TEST_FILES, 'sample_attributes_5.csv')
    TEMP_FOLDER = os.path.join(TEST_FILES, 'temp')


class EmailConst:
    INBOX_FOLDER = '"Inbox"'
    UNSEEN_EMAILS = 'UNSEEN'
    IMAP_SESSION_ACTIVE = 'SELECTED'
    EMAIL_FORMAT = "(RFC822)"
    IMAP_DOMAIN = 'imap.gmail.com'
    STATUS_OK = 'OK'
    FLAG_SEEN = r'\Seen'
    ADD_FLAG = '+FLAGS'


class TransactionState:
    SUCCESS = 'Success'
    USER_CANCELED = 'User canceled'
    PENDING = 'Pending'
    LIMIT_EXCEEDED = 'Error, limit exceeded'
    MANY_TRIES = 'Error, too many tries'
    PREPARED_CHECKOUT = 'prepared checkout'
    TRANSACTION_STATE_LIST = [SUCCESS, USER_CANCELED, PENDING, LIMIT_EXCEEDED, MANY_TRIES, PREPARED_CHECKOUT]


class TransactionStatuses:
    SUCCESS = 'Success'
    PREPARED_CHECKOUT = 'Statuses.Prepared_Checkout'
    FAILED = 'Failed'
    TRANSACTION_STATUSES_LIST = {
        'success': SUCCESS,
        'prepared checkout': PREPARED_CHECKOUT,
        'failed': FAILED
    }


class ExamResult:
    ALL = 'All'
    PASSED = 'Passed'
    FAILED = 'Failed'
    PENDING = 'Pending'
    REJECTED = 'Rejected'
    LIST_EXAM_RESULTS = [PASSED, FAILED, PENDING, REJECTED]
    LIST_ALL_EXAM_RESULTS = [ALL, PASSED, FAILED, PENDING, REJECTED]


class Labels:
    FILE_ID = 'File ID'
    STATUS = 'Status'
    DATE = 'Date'
    EMAIL = 'Email'


class DateType:
    DATE_SEP_DASH = '%Y-%m-%d'
    DATE_SEP_SLASH = '%d/%m/%Y'
    DATE_SEP_SPACE = '%d %B %Y'


class Authentication:
    EMAIL = 'email'
    API = 'api'
    OTP_FROM_NETWORK = 'otp_from_network'


class Credits:
    AMOUNT = 25


class Filters:
    CONTAINS = 'Contains'
    BEGINS_WITH = 'Begins with'
    ENDS_WITH = 'Ends with'


class Status:
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    DELETED = 'Deleted'


class Countries:
    MONTENEGRO = 'MONTENEGRO'
