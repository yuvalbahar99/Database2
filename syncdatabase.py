"""
author: Yuval Bahar
date: 6/12/2022
description: synchronize between few writers and readers,
so the access to the file will be according the rules.
"""

#  ----------------- IMPORTS -----------------

from filedatabase import FileDatabase
import logging
import win32event

# ----------------- CONSTANTS - ----------------

SEMAPHORE_NAME = 'semaphore'
MUTEX_NAME = 'lock'

# ----------------- FUNCTIONS - ----------------


class SyncDatabase:
    def __init__(self, database: FileDatabase):
        """
        initialize class that synchronize between readers and writers
        :param mode: threading/ processing
        :param database: an object that one of his feature is a dictionary
        """
        self.database = database
        self.semaphore = win32event.CreateSemaphore(None, 10, 10, SEMAPHORE_NAME)
        self.lock = win32event.CreateMutex(None, False, MUTEX_NAME)

    def write_access(self):
        """
        get access to change details in the dictionary
        :return: None
        """
        win32event.WaitForSingleObject(self.lock, win32event.INFINITE)
        for i in range(10):  # אם לכותב הרשאת כתיבה לכל האחרים אין גם לקריאה
            win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
        logging.debug("writer has an access")

    def write_release(self):
        """
        release access to change details in the dictionary
        :return: None
        """
        win32event.ReleaseSemaphore(self.semaphore, 10)
        win32event.ReleaseMutex(self.lock)
        logging.debug("writer released an access")

    def read_access(self):
        """
        get access to read details in the dictionary
        :return: None
        """
        win32event.WaitForSingleObject(self.semaphore, win32event.INFINITE)
        logging.debug("reader has an access")

    def read_release(self):
        """
        release access to read details in the dictionary
        :return: None
        """
        win32event.ReleaseSemaphore(self.semaphore, 1)
        logging.debug("reader released an access")

    def get_value(self, key):
        """
        returns the value of the value of the key in the dictionary
        :param key: key of the dictionary
        :return: flag - the value of the value of the key's dictionary
        """
        self.read_access()
        flag = self.database.get_value(key)
        self.read_release()
        return flag

    def set_value(self, key, val):
        """
        changes the value of the value of the key in the dictionary
        :param key: key of the dictionary
        :param val: value to put in the dictionary
        :return: flag - True/ False (if it was successful)
        """
        self.write_access()
        flag = self.database.set_value(key, val)
        self.write_release()
        return flag

    def delete_value(self, key):
        """
        deletes the value of the value of the key in the dictionary
        :param key: key of the dictionary
        :return: flag - the value that was deleted
        """
        self.write_access()
        flag = self.database.delete_value(key)
        self.write_release()
        return flag
