

def return_subset_habits(habits_data, regularity):
	"""
	Subset and return subset of habits data by designated regularity

	:param habits_data: list of habit entries in format: (id, user id, name, regularity, description, date created)
	:param regularity: regularity in days (int)
	:return: subsetted list of habit entries
	"""
	subset_habits_data = []
	for index, item in enumerate(habits_data):
		if item[3] == regularity:
			subset_habits_data.append(item)
	return subset_habits_data

def longest_streak(timestamps, regularity):
	"""
	Determine the longest streak from a set of timestamps given the regularity

	:param timestamps: list of timestamps
	:param regularity: regularity in days (int)
	:return: the longest streak as integer
	"""
	reg = (regularity * 86400) + 1
	longest = 0
	current = 1
	for index, item in enumerate(timestamps):
		if index == (len(timestamps) - 1):
			longest = max(longest, current)
			break
		elif item > (timestamps[index + 1] - reg):
			current += 1
		else:
			longest = max(longest, current)
			current = 1
	return longest

def longest_streak_of_streaks(habits_with_logs):
	"""
	Determine the habit with the longest streak given a set of habits with their associated logs

	:param habits_with_logs: list of tuples in which the first element is a habit's data in format:
							(id, user id, name, regularity, description, date created)
							and the second element is a list of the habit's log data in the format:
							(id, habit id, timestamp)
	:return: tuple where the first element is name of habit with the longest streak
			and the second element is the longest streak of that habit as integer
	"""
	longest_streak_seen = 0
	longest_streak_habit = None
	for habit_with_logs in habits_with_logs:
		habit_entry = habit_with_logs[0] # get entry of habit data
		habit_regularity = habit_entry[3] # get habit regularity from entry
		log_data = habit_with_logs[1] # get entries of habit log data
		timestamps = [log[2] for log in log_data]
		current_streak = longest_streak(timestamps, habit_regularity)
		if current_streak >= longest_streak_seen:
			longest_streak_seen = current_streak
			longest_streak_habit = habit_entry[2] # set habit name to current habit
	return (longest_streak_habit, longest_streak_seen)

