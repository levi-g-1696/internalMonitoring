# This is a sample Python script.
import codecs
import os
from ftplib import FTP

import psutil as psutil

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.





# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for proc in psutil.process_iter():
        # check whether the process name matches
        print(proc)
        if "2Erm" in proc.name():
            print(proc)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
