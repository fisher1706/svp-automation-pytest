import os

from test_data.constants import UserInfo
from test_data.validation_message import ErrorMessage

DISCORD_HOOKS = {
    'demo': {
        'ui-daily': os.environ.get('DISCORD_URL'),
    }
}


class LoginDataset:
    INVALID_CREDENTIALS_UI = [
        [UserInfo.INVALID_LOGIN, UserInfo.DEFAULT_PASSWORD, ErrorMessage.INVALID_CREDENTIALS],
        [UserInfo.DEFAULT_LOGIN, UserInfo.INVALID_LOGIN, ErrorMessage.INVALID_CREDENTIALS],
    ]


class SetPasswordDataset:
    INVALID_PASSWORD = [
        ['1', '1'],
        ['12345678901234567', '12345678901234567'],
        ['Password1', 'Password1'],
        ['Password#', 'Password#'],
        ['password#', 'password#'],
        [UserInfo.DEFAULT_PASSWORD, UserInfo.DEFAULT_PASSWORD + '1']
    ]


class ChangePasswordDataset:
    INVALID_CURRENT_PASSWORD = 'invalid current password'
    CURRENT_PASSWORD = 'current password'
    MISMATCH_NEW_PASSWORD = 'mismatch new password'
    INVALID_CONFIRM_PASSWORD = 'invalid confirm password'
    LIST_INVALID_PASSWORDS = {
        INVALID_CURRENT_PASSWORD: [UserInfo.DEFAULT_PASSWORD + '1', UserInfo.DEFAULT_PASSWORD,
                                   UserInfo.DEFAULT_PASSWORD],
        CURRENT_PASSWORD: [UserInfo.DEFAULT_PASSWORD, UserInfo.DEFAULT_PASSWORD, UserInfo.DEFAULT_PASSWORD],
        MISMATCH_NEW_PASSWORD: [UserInfo.DEFAULT_PASSWORD, UserInfo.DEFAULT_PASSWORD + '1', UserInfo.DEFAULT_PASSWORD],
        INVALID_CONFIRM_PASSWORD: [UserInfo.DEFAULT_PASSWORD, UserInfo.DEFAULT_PASSWORD,
                                   UserInfo.DEFAULT_PASSWORD + '1']
    }
    WRONG_PASSWORDS = [
        [' ', ' ', ' '],
        ['1234567', '1234567', '1234567'],
        ['password', 'password', 'password'],
        ['PASSWORD', 'PASSWORD', 'PASSWORD'],
        ['Password1', 'Password1', 'Password1'],
        ['1234567890a1234567890', '1234567890a1234567890', '1234567890a1234567890']
    ]


class GetCreditsDataset:
    INVALID_CERTIFICATES = [0, -1, 'test']
    VALID_CARD_DETAILS = ['4111111111111111', '0130', 'Test', '000']
    INVALID_CARD_DETAILS = [
        ['1', '1', '1', '1'],
        ['1111111111111111', '1111', '1111', '1111']
    ]


class EditEmailDataset:
    INVALID_EMAIL = ['test', 'test123', 'test123@', 'test123@test', 'test123@test.test213', 'test!@#$%^&*()@test.test']


class WrongTestCenterDataset:
    OFFICIAL_CONTACT_NUMBER = ['Test', '####']
    CONTACT_INFORMATION = ['123456', '####']
    CITY = ['123456', '####']
    POSTAL_CODE = ['Test', '####']
    EMAIL = ['test', 'test@', 'test.test.com', 'test@test']


class WrongCertificateDataset:
    WRONG_CERTIFICATE = '1234567890'
    WRONG_PASSPORT_NUMBER = '123456789'
    INCORRECT_NUMBER = 'TEST'


class PageNumbersDataset:
    PAGE_VALUES = 11
