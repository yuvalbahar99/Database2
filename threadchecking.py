"""
author: Yuval Bahar
date: 6/12/2022
description: checks the synchronization while mode is threading
"""

#  ----------------- IMPORTS -----------------

from filedatabase import FileDatabase
from syncdatabase import SyncDatabase
from threading import Thread
import logging

# ----------------- CONSTANTS - ----------------

FILENAME = "new_file"
READER_NUM = 50
WRITER_NUM = 10
FORMAT = '%(asctime)s %(levelname)s %(threadName)s %(message)s'
FILENAMELOG = 'logging_thread.text'

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
        val = database.delete_value(i)
        flag = val == i or val is None
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
    all_threads = []
    for i in range(1000, 1100):
        database.set_value(i, i)
    for i in range(0, READER_NUM):
        thread = Thread(target=reader, args=(database, ))
        all_threads.append(thread)
    for i in range(0, WRITER_NUM):
        thread = Thread(target=writer, args=(database, ))
        all_threads.append(thread)
    for i in all_threads:
        i.start()
    for i in all_threads:
        i.join()
    for i in range(1000, 1100):
        assert database.get_value(i) == i


if __name__ == "__main__":
    main()
