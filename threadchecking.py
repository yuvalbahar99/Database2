"""
author: Yuval Bahar
date: 6/12/2022
description: checks the synchronization while mode is threading
"""

#  ----------------- IMPORTS -----------------

from filedatabase import FileDatabase
from syncdatabase import SyncDatabase
import win32process
import win32event
import logging

# ----------------- CONSTANTS - ----------------

FILENAME = "new_file"
MODE = "threading"
READER_NUM = 50
WRITER_NUM = 10
FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(message)s'
FILENAMELOG = 'logging_thread.text'
SIZE = 1000

# ----------------- FUNCTIONS - ----------------


def reader(database):
    """
    reader is trying to get an access to read the value from the dictionary
    :param database: an object that one of his feature is a dictionary
    :return: None
    """
    logging.debug("reader started")
    for i in range(100):
        flag = database.get_value(i) == i or database.get_value(i) is None
        assert flag
    logging.debug("reader left")


def writer(database):
    """
    writer is trying to get an access to write the value from the dictionary
    :param database: an object that one of his feature is a dictionary
    :return: None
    """
    logging.debug("writer started")
    for i in range(100):
        assert database.set_value(i, i)
    for i in range(100):
        flag = database.delete_value(i) == i or database.delete_value(i) is None
        assert flag
    logging.debug("writer left")


def main():
    """
    combine the running of the writers and the readers by threading
    :return: None
    """
    #  checks the access of writing and reading without competition
    # צריך להדפיס כל פעם שלקוח מקבל גישה לכתוב או לקרוא, וכל פעם שהוא משחרר את הגישה
    logging.basicConfig(filename=FILENAMELOG, level=logging.DEBUG, format=FORMAT)
    database = SyncDatabase(FileDatabase(FILENAME))
    # הרשאת כתיבה כאשר יש תחרות
    counter = 0
    for i in range(0, READER_NUM):
        thread = win32process.beginthreadex(None, SIZE, writer, (database, ), 0)[0]
        if win32event.WaitForSingleObject(thread, win32event.INFINITE) == 0:
            counter += 1
    for i in range(0, WRITER_NUM):
        thread = win32process.beginthreadex(None, SIZE, reader, (database, ), 0)[0]
        if win32event.WaitForSingleObject(thread, win32event.INFINITE) == 0:
            counter += 1
    assert counter == READER_NUM + WRITER_NUM


if __name__ == "__main__":
    main()
