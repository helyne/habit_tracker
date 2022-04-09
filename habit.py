import sqlite3

from db import add_habit, db_get_habit_data, update_habit,\
    delete_habit, delete_habit_logs, add_log, db_get_habit_log_data

class Habit:
    """Provides an interface to a user's habit,
    keeping the state of the habit in sync with the db & vice versa

    :param db: an initialized sqlite3 database connection object
    :param user_id: the id number of current user
    :param habit_name: the name of the habit
    :param regularity: the regularity (or periodicity) of the habit
    :param description: the description of the habit (optional)
    :param habit_id: the id number of the habit (optional)
    """
    def __init__(self,
                 db: sqlite3.Connection, user_id: int, habit_name: str,
                 regularity=None, description="", habit_id=None, habit_logs=[]):
        self.db = db
        self.user = user_id
        self.name = habit_name
        self.regularity = regularity
        self.description = description
        self.id = habit_id
        self.logs_data = habit_logs

    def identify(self):
        """syncs habit object with database if the user already has a habit by that name"""
        habit_data = db_get_habit_data(self.db, self.user, self.name)
        if habit_data is not None:
            self.id = habit_data[0]
            self.regularity = habit_data[3]
            self.description = habit_data[4]
            habit_logs_data = db_get_habit_log_data(self.db, self.id)
            self.logs_data = habit_logs_data

    def save(self):
        """saves the user's habit to the database if the habit does not exist,
        otherwise syncs the database with the current habit object's attributes"""
        if self.id is not None:
            update_habit(self.db, self.id, self.name, self.regularity, self.description)
        else:
            add_habit(self.db, self.user, self.name, self.regularity, self.description)
            habit_entry = db_get_habit_data(self.db, self.user, self.name)
            self.id = habit_entry[0]

    def delete(self):
        """deletes the user's habit and habit logs from the db,
        and clears habit object's attributes"""
        delete_habit_logs(self.db, self.id)
        delete_habit(self.db, self.id)
        self.id = None
        self.user = None
        self.name = None
        self.regularity = None
        self.description = None
        self.logs_data = None

    def log(self):
        """adds log with current timestamp to habit's logs in db,
        then syncs habit object's logs data with db"""
        add_log(self.db, self.id)
        habit_logs_data = db_get_habit_log_data(self.db, self.id)
        self.logs_data = habit_logs_data

