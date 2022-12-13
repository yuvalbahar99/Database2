"""
author: Yuval Bahar
date: 6/12/2022
description: get, set and deletes values from the dictionary
"""

# ----------------- FUNCTIONS - ----------------


class Database:

    def __init__(self):
        """
        initialize new class that has a dictionary
        """
        self.dict = {None: None}

    def set_value(self, key, val):
        """
        changes the value of the value of the key in the dictionary
        :param key: key of the dictionary
        :param val: value to put in the dictionary
        :return: True/ False (if it was successful)
        """
        self.dict.update({key: val})
        return True

    def get_value(self, key):
        """
        returns the value of the value of the key in the dictionary
        :param key: key of the dictionary
        :return: the value of the value of the key's dictionary
        """
        if key in self.dict.keys():
            return self.dict[key]
        return None

    def delete_value(self, key):
        """
        deletes the value of the value of the key in the dictionary
        :param key: key of the dictionary
        :return: the value that was deleted
        """
        if key in self.dict.keys():
            return self.dict.pop(key)
        return None
