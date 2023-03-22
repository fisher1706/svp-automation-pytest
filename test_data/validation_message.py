class SuccessMessage:
    LOGIN = {'type': 'success', 'text': 'Welcome to the Professional Accreditation Program Control Panel.'}
    ADMIN_CONFIRM_CODE = {'type': 'otp code', 'text': 'Two-Factor Verification'}
    CONFIRM_CODE = {'type': 'email code', 'text': 'Two-Factor Verification'}
    LEGISLATOR_CREATION = {'type': 'legislator creation', 'text': 'The legislator has been created successfully'}
    TEST_CENTER_CREATION = {'type': 'test center creation', 'text': 'Test center has been created successfully'}
    TEST_CENTER_REMOVE = {'type': 'test center creation', 'text': 'Test Center has been deleted successfully'}
    MSG_VALID_CERTIFICATE = 'The certificate is valid'
    CERTIFICATE = {'type': 'certificate', 'text': 'You can download list of certificates now'}


class ErrorMessage:
    INVALID_CREDENTIALS = {'type': 'invalid credentials error', 'text': 'Invalid Email or Password.'}
    PASS_WARNING = {'type': 'pass warning', 'text': 'Complexity requirement not met. Length should be 8-20 characters '
                                                    'and include at least: 1 uppercase, 1 lowercase, 1 digit and 1 '
                                                    'special character'}
    CONFIRMED_PASS_WARNING = {'type': 'pass warning', 'text': 'doesn\'t match Password'}
    VERIFICATION_CODE_WARNING = {'type': 'pass warning', 'text': 'The code you have entered is incorrect'}
    TOKEN_INVALID = {'type': 'token warning', 'text': 'Password token is invalid'}

    CARD_NUMBER = {'type': 'card number', 'text': 'Invalid card number or brand'}
    CARD_EXPIRY_DATE = {'type': 'card expiry date', 'text': 'Invalid expiry date'}
    CARD_CVV = {'type': 'card cvv', 'text': 'Invalid CVV'}
    CARD_HOLDER = {'type': 'card holder', 'text': 'Invalid card holder'}

    POPUP_EMAIL_FIELD = {'type': 'popup edit email', 'text': 'Please enter a valid email'}
    MSG_WRONG_CERTIFICATE = 'The passport number does not match for this certificate serial number'
    MSG_CERTIFICATE_NOT_EXIST = 'The certificate does not exist'
    MSG_EXPIRED_CERTIFICATE = 'The certificate is expired'


class WarningMessage:
    ACTIVE_CERTIFICATE = {'type': 'active certificate',
                          'text': 'Labor with below info have an active certificate within the same category, '
                                  'are you sure you want to proceed with issuing another certificate knowing that the '
                                  'amount is not refundable'}
    CHOOSE_FILE_BTN = 'Choose file button is {} disabled'
    OTP_CODE = 'Confirmation verification code is not correct'
    EMAIL_IS_EXIST = 'has already been taken'
    TC_NAME = 'The Test center is already registered'
    TC_EMPTY_NAME = "Name can't be empty"
    TC_CONTACT_NUMBER = "Contact number can't be empty"
    TC_EMPTY_CATEGORY_LIST = 'At least one occupation must be selected'
    TC_EMPTY_OWNER_NAME = "Name can't be empty"
    TC_EMPTY_EMAIL = "Email can't be empty"
    TC_EMPTY_CITY = "City can't be empty"
    TC_EMPTY_STREET = "Street can't be empty"
    TC_ONLY_DIGITS_CONTACT_NUMBER = 'Should contain digits only'
    TC_VALID_EMAIL = 'Please enter a valid email'
    ONLY_EN_CHARS = 'Only english characters'
    TC_ONLY_DIGITS_POSTAL_CODE = 'Should contain digits only'
    INVALID_CURRENT_PASSWORD = 'Current password is invalid'
    SAME_NEW_PASSWORD = 'new password shouldn’t be same as old Password'
    MISMATCH_PASSWORD = "doesn't match Password"
    MSG_WRONG_CERTIFICATE = "The passport number is valid but its not for the certificate entered serial number"


class InfoMessages:
    NO_DATA_AVAILABLE = 'There are no data'
