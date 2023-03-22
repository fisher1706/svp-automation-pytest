from datetime import date

from helpers.logger import yaml_logger
from helpers.random_manager import RandomManager
from test_data.constants import DirPath
from test_data.models.account import Account
from test_data.models.email import Email
from test_data.models.labor import Labor

logger = yaml_logger.setup_logging(__name__)


class ModelBuilder:
    LOGO = DirPath.PNG_FILE
    COUNTRY = 'Ukraine'
    COUNTRY_ID = '5'
    COUNTRY_CODE = '+380'
    CITY = 'Kiev'
    ADDRESS = 'Address'
    CONTACT_NAME = 'Contact Name'
    CATEGORY = 'Engine Mechanics'
    POSTAL_CODE = 111111

    @staticmethod
    def build_random_account(en_name=None,
                             ar_name='',
                             logo=LOGO,
                             country=COUNTRY,
                             country_id=COUNTRY_ID,
                             country_code=COUNTRY_CODE,
                             category=CATEGORY,
                             city=CITY,
                             address=ADDRESS,
                             postal_code=POSTAL_CODE,
                             contact_name=CONTACT_NAME,
                             sub_number=None,
                             phone_number=None,
                             email=None,
                             show_logo=False):
        random_manager = RandomManager()
        en_name = en_name if en_name else random_manager.random_name()
        email = email if email else random_manager.random_email()
        sub_number = sub_number if sub_number else random_manager.random_number()
        phone_number = phone_number if phone_number else country_code + sub_number
        logger.info(f"USER EMAIL: {email}, USER NAME: {en_name}")
        return Account(en_name=en_name,
                       ar_name=ar_name,
                       logo=logo,
                       country=country,
                       country_id=country_id,
                       country_code=country_code,
                       category=category,
                       city=city,
                       address=address,
                       postal_code=postal_code,
                       contact_name=contact_name,
                       sub_number=sub_number,
                       phone_number=phone_number,
                       email=email,
                       show_logo=show_logo)

    @staticmethod
    def build_email(mail):
        return Email(_from=mail['from'],
                     _to=mail['to'],
                     date=mail['date'],
                     subject=mail['subject'],
                     body=mail.get_payload()
                     )

    @staticmethod
    def build_random_labor(national_id=None, labor_name=None, passport=None, occupation=CATEGORY, exam_date=None,
                           scope=33):
        random_manager = RandomManager()
        national_id = national_id if national_id else random_manager.random_name()
        labor_name = labor_name if labor_name else random_manager.random_name()
        passport = passport if passport else random_manager.random_number()
        exam_date = exam_date if exam_date else date.today()
        return Labor(national_id=national_id,
                     labor_name=labor_name,
                     passport=passport,
                     occupation=occupation,
                     exam_date=exam_date,
                     scope=scope)
