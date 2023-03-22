import csv
import datetime
from random import randint

import allure

from test_data.constants import DirPath


class CSVHelper:

    def __init__(self):
        self.name = []
        self.passport_numbers = []

    @property
    def get_passport_number(self):
        return self.passport_numbers[0]

    @property
    def get_name(self):
        return self.name

    @classmethod
    def _open_file(cls, file_path=None, list_csv=None, mode: str = 'r'):
        if mode == 'r':
            with open(file_path, mode=mode, encoding="utf-8") as file:
                data = csv.reader(file)
                for row in data:
                    list_csv.append(row)
        else:
            with open(file_path, mode=mode, encoding="utf-8") as file:
                file = csv.writer(file, quotechar="'", quoting=csv.QUOTE_MINIMAL)
                for row in list_csv:
                    file.writerow(row)

    @classmethod
    def _verify_timestamp(cls, timestamp: str):
        if not timestamp:
            date = datetime.date.today().strftime('%d.%m.%Y')
        elif timestamp == 'previous':
            date = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d.%m.%Y')
        else:
            date = '01.01.2000'
        return date

    def change_timestamp_to_previous_day(self):
        timestamp = self._verify_timestamp('previous')
        list_csv = []
        self._open_file(DirPath.CSV, list_csv, mode='r')
        for item in list_csv[1:]:
            item[5] = timestamp
        self._open_file(DirPath.CSV, list_csv, mode='w')

    @allure.step
    def prepare_csv_file(self, amount: int = 1, wrong_timestamp: str = False, exam_score: int = 99):
        timestamp = self._verify_timestamp(wrong_timestamp)
        random_number = str(randint(1, 10 ** randint(7, 8)))
        self.passport_numbers = [random_number + str(_) for _ in range(amount)]
        emails = [f'test{number}@gmail.com' for number in self.passport_numbers]
        file_path = DirPath.CSV if amount == 1 else DirPath.CSV_5
        list_csv = []
        self._open_file(file_path, list_csv, mode='r')
        for item in list_csv[1:]:
            item[2] = self.passport_numbers[list_csv.index(item) - 1]
            item[3] = emails[list_csv.index(item) - 1]
            item[4] = exam_score
            item[5] = timestamp
        self._open_file(file_path, list_csv, mode='w')
