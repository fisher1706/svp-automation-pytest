import filecmp
import glob
import os
import time
import zipfile

import pytest
from PyPDF2 import PdfReader

from test_data.constants import DirPath


class FileHelper:

    def __init__(self):
        self.temp_folder_path = DirPath.TEMP_FOLDER

    @staticmethod
    def check_compatibility_files(file1, file2):
        filecmp.cmp(file1, file2)

    def get_temp_files(self, csv=False, pdf=False, check=True):
        for _ in range(10):
            time.sleep(1)
            tmp_files = glob.glob(os.path.join(self.temp_folder_path, '*'))
            if tmp_files:
                if csv:  # pylint: disable=no-else-return
                    return next(file for file in tmp_files if '.csv' in file)
                elif pdf:
                    return next(file for file in tmp_files if '.pdf' in file)
                return tmp_files
        if check:
            pytest.fail('File not found in temp directory')
        return None

    def clear_temp_folder(self, check=True):
        tmp_files = self.get_temp_files(check=check)
        if tmp_files:
            for file in tmp_files:
                os.remove(os.path.join(self.temp_folder_path, file))

    def unzip_temp_file(self):
        tmp_files = self.get_temp_files()
        if tmp_files:
            with zipfile.ZipFile(os.path.join(self.temp_folder_path, tmp_files[0]), 'r') as zip_ref:
                zip_ref.extractall(self.temp_folder_path)

    def read_pdf_file(self):
        tmp_file = self.get_temp_files(pdf=True)
        if tmp_file:
            return set(PdfReader(os.path.join(self.temp_folder_path, tmp_file)).getPage(0).extractText().split('\n'))
        return pytest.fail('File not found in temp directory')
