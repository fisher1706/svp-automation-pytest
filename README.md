# svp-automation

Automation testing for SVP project

Preconditions (local)
---
Make sure you have `git`, `python3` and `pip3` installed. If not, please do so by googling and following the
instructions on the official resources.

Prepare local environment
---

* Clone the project to your local machine and navigate to the project directory:

```shell
git clone git@gitlab.qiwa.tech:takamol/qiwa/integration-testing/svp-automation.git
cd svp-automation
```

* Install and setup virtualenv for the project:

```shell
pip install virtualenv
virtualenv --python python3 venv
source venv/bin/activate
```

* Install all packages required for the tests run:

```shell
pip install -r requirements.txt
```

----
Same actions you can do with PyCharm IDE via UI with hints

Run tests locally
---
Once the environment is ready the tests can be executed. Run the following command to do so:

```shell
pytest
```

All tests are grouped by features using tag name `@pytest.mark.user_suite`. So to run specific tests by tag name use cli
argument `-m` + tag value:

```shell
pytest -m sign_in
```

To run tests with Allure reporting add the argument `--alluredir=allure-results` to the command.

```shell
pytest --alluredir=allure-results
```

View Allure report locally
---
If the tests were executed with `--alluredir` argument, allure results will be stored in the defined directory. To view
allure results run the following command:

```shell
allure serve allure-results
```
