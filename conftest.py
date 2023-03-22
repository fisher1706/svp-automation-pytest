import os
from typing import Tuple

from dotenv import load_dotenv

from helpers.pytest_init_support import get_suite_name_from_params

load_dotenv()


def pytest_addhooks(pluginmanager):
    params: Tuple[str] = pluginmanager.rewrite_hook.config.invocation_params.args
    if '-m' in params:
        suite_name = get_suite_name_from_params(params)
        if suite_name is None:
            raise AssertionError('Failed to get suite name')
        is_api_dir = bool('api' in suite_name)
        os.environ["SUITE_NAME"] = "-".join(suite_name.split(" and "))
    elif '-k' in params:
        is_api_dir = True
    else:
        path = str(pluginmanager.rewrite_hook.config.invocation_dir)
        api = '/api' if os.name == 'posix' else '\\api'
        is_api_dir = bool(api in path)

    if not is_api_dir:
        pluginmanager.import_plugin('fixtures.navigation')
        pluginmanager.import_plugin('fixtures.prepare_ui')


pytest_plugins = [
    'fixtures.prepare_api',
    'fixtures.actions',
    'fixtures.reports'
]


def pytest_addoption(parser):
    parser.addoption("--admin_environment_url", action="store", default=os.environ.get('ENV_ADMIN_URL'))
    parser.addoption("--environment_url", action="store", default=os.environ.get('ENV_URL'))
    parser.addoption("--api_url", action="store", default=os.environ.get('API_URL'))
    parser.addoption("--allure_url", action="store", default=os.environ.get('ALLURE_URL'))
    parser.addoption("--grid_url", action="store", default=os.environ.get('GRID_URL'))
    parser.addoption("--browser_name", action="store", default="chrome", help="chrome, firefox, opera")
