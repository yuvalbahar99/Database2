"""
author: Yuval Bahar
date: 6/12/2022
description: get, set and deletes values from the dictionary
using the file
"""

#  ----------------- IMPORTS -----------------

from database import Database
import pickle
import win32file

# ----------------- CONSTANTS - ----------------

BUFFERSIZE = 100000000


# ----------------- FUNCTIONS - ----------------


class FileDatabase(Database):

    def __init__(self, file):
        """
        initialize new class that has a dictionary in a file
        :param file: name of the file that the dictionary will be written in
        """
        super().__init__()
        self.file = file

    def dump_file(self):
        """
        write in the file
        :return: None
        """
        data = pickle.dumps(self.dict)
        file = win32file.CreateFile(self.file, win32file.GENERIC_WRITE, 0, None, win32file.CREATE_ALWAYS, 0, None)
        win32file.WriteFile(file, data)
        win32file.CloseHandle(file)

    def load_file(self):
        """
        read from the file
        :return: None
        """
        try:
            file = win32file.CreateFile(self.file, win32file.GENERIC_READ, win32file.FILE_SHARE_READ, None,
                                        win32file.OPEN_ALWAYS, 0, None)
            self.dict = pickle.loads(win32file.ReadFile(file, BUFFERSIZE)[1])
            win32file.CloseHandle(file)
        except:
            pass

    def get_value(self, key):
        """
        returns the value of the value of the key in the dictionary
        :param key: key of the dictionary
        :return: the value of the value of the key's dictionary
        """
        self.load_file()
        return super().get_value(key)

    def set_value(self, key, val):
        """
        changes the value of the value of the key in the dictionary
        :param key: key of the dictionary
        :param val: value to put in the dictionary
        :return: True/ False (if it was successful)
        """
        self.load_file()
        flag = super().set_value(key, val)
        self.dump_file()
        return flag

    def delete_value(self, key):
        """
        deletes the value of the value of the key in the dictionary
        :param key: key of the dictionary
        :return: the value that was deleted
        """
        self.load_file()
        flag = super().delete_value(key)
        self.dump_file()
        return flag
