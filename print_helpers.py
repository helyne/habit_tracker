from db import db_get_habit_log_data
from analyze import longest_streak_of_streaks
from datetime import datetime

def print_habits(habits_data, regularity=None):
	print("Habit name (regularity in days): Description\n"
		  "-----------------------------------------------")
	if regularity is None:
		[print(f"{str(item[2])} ({str(item[3])}): {str(item[4])}") for
		 item in habits_data]
	else:
		[print(f"{str(item[2])} ({str(item[3])}): {str(item[4])}") for
		 item in habits_data if item[3] == regularity]
	print("-----------------------------------------------\n")

def print_logs(logs_data):
	print("-----------------------------------------------")
	[print(datetime.fromtimestamp(item[2])) for item in logs_data]
	print("-----------------------------------------------\n")

def print_longest_streak_of_streaks(habits_data, db, message):
	habits_with_logs = [(habit, db_get_habit_log_data(db, habit[0])) for habit in habits_data]
	print(f'\n\n{message}\n'.join(map(str, longest_streak_of_streaks(habits_with_logs))))