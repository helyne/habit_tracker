from habit import Habit
from user import User
from db import get_db
from analyze import return_subset_habits, longest_streak_of_streaks, longest_streak


class TestUser:

	def setup_method(self):
		self.db = get_db("new_test.db")
		self.user = User(self.db, "toto")

	def test_save_user(self):
		# check pre-save user object
		assert self.user.id is None
		assert self.user.name == "toto"

		# should save
		self.user.save()
		assert self.user.id == 1
		assert self.user.name == "toto"

	def test_identify_user(self):
		# should identify on new habit object
		self.user.identify()
		assert self.user.id is None

		# should identify on existing data in db using new object
		self.user.save()
		user2 = User(self. db, "toto")
		user2.identify()
		assert user2.id == 1

	def teardown_method(self):
		import os
		os.remove("new_test.db")

class TestHabit:

	def setup_method(self):
		# create dummy habit data in db and new habit object
		self.db = get_db("new_test.db")
		self.user = User(self.db, "totoro")
		self.user.save()
		# self.habit_existing = Habit(self.db, self.user.id, "existing habit", 1, "description", 1,
		# 							[(1, 1, 1111111111)])
		self.habit_existing = Habit(self.db, self.user.id, "existing habit", 1, "description")
		self.habit_existing.save()
		self.habit_existing.log()
		self.habit_new = Habit(self.db, self.user.id, "new")

	def test_save_habit(self):
		# check pre-save object
		assert self.habit_new.id is None
		assert self.habit_new.name == "new"
		assert self.habit_new.description == ""
		assert self.habit_new.logs_data == []

		# should save
		self.habit_new.save()
		assert self.habit_new.id == self.habit_existing.id + 1
		assert self.habit_new.name == "new"
		assert self.habit_new.description == ""

		# should save after modifying object
		self.habit_new.name = "updated"
		self.habit_new.description = "new description"
		self.habit_new.save()
		assert self.habit_new.id == 2
		assert self.habit_new.name == "updated"
		assert self.habit_new.description == "new description"

		# make sure the habit data was actually saved by running
		# identify on a new habit with the same name
		habit2 = Habit(self.db, self.user.id, "updated")
		habit2.identify()
		assert habit2.id == self.habit_new.id
		assert habit2.name == self.habit_new.name
		assert habit2.description == self.habit_new.description

	def test_identify_habit(self):
		# should identify on unsaved object
		self.habit_new.identify()
		assert self.habit_new.id is None

		# should identify on existing data in db using new object
		habit2 = Habit(self.db, self.user.id, "existing habit")
		habit2.identify()
		assert habit2.id == self.habit_existing.id
		assert habit2.description == self.habit_existing.description
		assert habit2.logs_data == self.habit_existing.logs_data

	def test_delete_habit(self):
		existing_habit_id = self.habit_existing.id
		existing_habit_name = self.habit_existing.name

		# should delete an existing habit
		self.habit_existing.delete()
		assert self.habit_existing.id is None
		assert self.habit_existing.name is None
		assert self.habit_existing.description is None
		assert self.habit_existing.user is None
		assert self.habit_existing.logs_data is None

		# ensure the existing habit was actually deleted in the db
		# by creating a new one with the deleted habit's name
		habit2 = Habit(self.db, self.user.id, existing_habit_name)
		habit2.identify()
		assert self.habit_existing.id is None
		assert self.habit_existing.logs_data is None

		# id should be auto-incremented, since it's a new habit
		habit2.save()
		assert habit2.id == existing_habit_id + 1
		assert habit2.name == existing_habit_name
		assert habit2.description is ''
		assert habit2.user == self.user.id
		assert habit2.logs_data == []

	def test_log_habit(self):
		# object should have no existing logs
		assert self.habit_new.logs_data == []

		# logging habit should add log to habit_logs data
		self.habit_new.save()
		self.habit_new.log()
		assert self.habit_new.logs_data[0] is not None

		# make sure log was saved to database
		habit2 = Habit(self.db, self.user.id, self.habit_new.name)
		habit2.identify()
		assert habit2.logs_data[0] == self.habit_new.logs_data[0]


	def teardown_method(self):
		import os
		os.remove("new_test.db")



class TestAnalyze:

	def setup_method(self):
		# create db-independent dummy data
		self.habit1 = (1, 1, 'habit1', 1, '', 1649439518) # habit1 regularity = 1
		self.habit2 = (2, 1, 'habit2', 1, '', 1649439518) # habit2 regularity = 1
		self.habit3 = (2, 1, 'habit3', 7, '', 1649439518) # habit3 regularity = 7
		self.habit1_logs_streak4 = [(1, 1, 1*86400), (2, 1, 2*86400), (3, 1, 3*86400), (4, 2, 4*86400)]
		self.habit2_logs_streak2 = [(1, 1, 1*86400), (2, 1, 2*86400), (3, 1, (3*86400+5)), (4, 2, 4*86400)]
		self.habit3_logs_streak1 = [(1, 1, 1*86400)]

	def test_return_subset(self):
		self.habits_data = [self.habit1, self.habit2, self.habit3]

		# should return subset of habit data based off regularity of 7
		subset = return_subset_habits(self.habits_data, 7)
		assert subset == [self.habit3]

		# should return subset of habit data based off regularity of 1
		subset = return_subset_habits(self.habits_data, 1)
		assert subset == [self.habit1, self.habit2]

	def test_longest_streak(self):
		# should return longest streak of habit2
		timestamps = [log[2] for log in self.habit2_logs_streak2]
		habit_longest_streak = longest_streak(timestamps, 1)
		assert habit_longest_streak == 2

	def test_longest_streak_of_streaks(self):
		self.habits_with_logs = [(self.habit1, self.habit1_logs_streak4), (
			self.habit2, self.habit2_logs_streak2), (self.habit3, self.habit3_logs_streak1)]

		# should return longest streak of all habits
		streak_of_streaks = longest_streak_of_streaks(self.habits_with_logs)
		assert streak_of_streaks == ('habit1', 4)

	def teardown_method(self):
		pass
