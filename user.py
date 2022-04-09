import sqlite3

from db import db_get_user_data, add_user

class User:
    """Provides an interface for a user,
    keeping the state of the user in sync with the db

    :param db: sqlite3 database object
    :param user_name: the name of the user
    :param user_id: the id number of current user (optional)
    """
    def __init__(self, db: sqlite3.Connection, user_name: str, user_id=None):
        self.db = db
        self.name = user_name
        self.id = user_id

    def identify(self):
        """syncs user object with database if the user exists"""
        user_data = db_get_user_data(self.db, self.name)
        if user_data is not None:
            self.id = user_data[0]

    def save(self):
        """saves the user to the database if the user does not exist"""
        if self.id is None:
            add_user(self.db, self.name)
            user_entry = db_get_user_data(self.db, self.name)
            self.id = user_entry[0]

