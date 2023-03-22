from helpers.logger import yaml_logger
from src.api.actions.auth_api_actions import AuthApiActions
from src.api.features.admin_api import AdminApi
from src.ui.actions.base_actions import BaseActions
from src.ui.actions.login_actions import LoginActions
from src.ui.actions.password_actions import PasswordActions
from test_data.constants import Title
from test_data.models.model_builder import ModelBuilder

logger = yaml_logger.setup_logging(__name__)


class AdminApiActions(AdminApi):

    def __init__(self, api):
        super().__init__(api)
        self.legislator_account = None
        self.tcenter_account = None
        self.auth_api_actions = AuthApiActions(api)
        self.login_action = LoginActions()
        self.password = PasswordActions()
        self.base_actions = BaseActions()

    def create_legislator(self, token):
        logger.info('LEGISLATOR INFO')
        self.legislator_account = ModelBuilder.build_random_account()
        self.post_create_legislator(token=token,
                                    en_name=self.legislator_account.en_name,
                                    arabic_name=self.legislator_account.ar_name,
                                    country_id=self.legislator_account.country_id,
                                    city=self.legislator_account.city,
                                    address=self.legislator_account.address,
                                    phone_number=self.legislator_account.sub_number,
                                    country_code=self.legislator_account.country_code,
                                    full_name=self.legislator_account.contact_name,
                                    email=self.legislator_account.email,
                                    postal_code=self.legislator_account.postal_code,
                                    show_logo=self.legislator_account.show_logo)
        return self

    def create_tcenter(self, token):
        logger.info('TEST CENTER INFO')
        self.tcenter_account = ModelBuilder.build_random_account()
        self.post_create_tcenter(token=token,
                                 name=self.tcenter_account.en_name,
                                 country_id=self.tcenter_account.country_id,
                                 city=self.tcenter_account.city,
                                 address=self.tcenter_account.address,
                                 phone_number=self.tcenter_account.sub_number,
                                 country_code=self.tcenter_account.country_code,
                                 full_name=self.tcenter_account.contact_name,
                                 email=self.tcenter_account.email,
                                 legislator_id=self.legislator_id,
                                 postal_code=self.legislator_account.postal_code)
        return self

    def activate_account(self, email):
        self.base_actions.activate_account(email)
        self.base_actions.verify_expected_title(expected_title=Title.SPA_SET_PASSWORD)

    def activate_permission(self, tcenter, multiple_categories=None):
        self.auth_api_actions.get_token()
        self.put_permissions(token=self.auth_api_actions.token,
                             tcenter=tcenter,
                             multiple_categories=multiple_categories)
