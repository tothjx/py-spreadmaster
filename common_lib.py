# common_lib.py

import os
import sys
import time


# common library
class CommonLib:
    def __init__(self):
        self.version = 1.0
        self.title = 'common library'
        self.errors = []

    # e.g. for pyinstaller
    # add absolute path to resource
    @staticmethod
    def get_resource_path(relative_path):
        try:
            # pyinstaller creates a temp folder
            # and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            # absolute path for base dir
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    @staticmethod
    def get_format_current_date_hu():
        return time.strftime("%Y-%M-%d %H:%I:%S")

    @staticmethod
    def get_month_name(index, lang='hu'):
        if lang == 'hu':
            months = ('január', 'február', 'március', 'április', 'május', 'június',
                'július', 'augusztus', 'szeptember', 'október', 'november', 'december')
        else:
            months = ('January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December')
        return months[index]

    @staticmethod
    def get_day_name(index, lang='hu'):
        if lang == 'hu':
            days = ('hétfő', 'kedd', 'szerda', 'csütörtök', 'péntek', 'szombat', 'vasárnap')
        else:
            days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
        return days[index]

    @staticmethod
    def list_files(path):
        files = []
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                files.append(name)
        return files

# end
