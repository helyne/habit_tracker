import questionary
from db import get_db, db_get_user_habits, db_get_habit_data
from habit import Habit
from user import User
from analyze import return_subset_habits
from print_helpers import print_habits, print_longest_streak_of_streaks, print_logs


def cli():
    # initialize database
    db = get_db()

    print("Hai. Welcome to Habitoro.")

    # get username and save
    user_name = questionary.text("What's your name?\n").ask()
    user = User(db, user_name)
    user.identify()
    user.save()
    print(f"Welcome, {user.name}.")

    # optionally print user habits
    confirm_showlist = questionary.confirm("Would you like to see your habits?\n").ask()
    if confirm_showlist:
        print(f"\nHere are all your current habits, {user.name}\n")
        print_habits(db_get_user_habits(db, user.id))

    else:
        print("Ok. Then let's track some habits.")

    confirm_start = questionary.confirm("Are you ready to track some habits?\n").ask()

    if confirm_start:
        go = True
        while go:

            choice = questionary.select(
                "What do you want to do with your habits?",
                choices=["Create", "Log", "Analyze", "List", "Modify", "Delete", "Exit"]
            ).ask()

            habits_data = db_get_user_habits(db, user.id)

            if choice == "Create":
                try_again = True
                while try_again:
                    name = questionary.text("What's the name of your habit?\n",
                                            validate=lambda text: True if len(text) > 0 else "Please enter a value"
                                            ).ask() # validate response is not null
                    reg = questionary.text("How often do you want to do this habit (in days)?"
                                           " e.g. daily = 1, weekly = 7, monthly = 30\n",
										   validate=lambda text: True if len( # validate response is an integer
											   text) > 0 and text.isnumeric() else "Please enter a value"
										   ).ask()
                    desc = questionary.text("What's the description of your habit? (optional)\n").ask()
                    habit = Habit(db=db, user_id=user.id, habit_name=name,
                                  regularity=int(reg), description=desc)
                    habit.identify()
                    if habit.id is None:
                        habit.save()
                        print("Thanks for the info. Your habit has been saved! \nNow...")
                        try_again = False
                    else:
                        print("Oops. You already have that habit saved.")

            elif choice == "Log":
                try_again = True
                while try_again:
                    print("\nHere are all your current habits\n")
                    print_habits(habits_data)
                    name = questionary.text("Which habit do you want to log?\n").ask()
                    habit = Habit(db, user.id, name)
                    habit.identify()
                    if habit.id is None:
                        print("I don't think that's a habit. Let's try again...")
                    else:
                        habit.log()
                        print("Your habit has been logged! \nNow...")
                        try_again = False

            elif choice == "Modify":
                try_again = True
                while try_again:
                    print("\nHere are all your current habits\n")
                    print_habits(habits_data)
                    name = questionary.text("Which habit do you want to modify?\n").ask()
                    habit = Habit(db, user.id, name)
                    habit.identify()
                    if habit.id is None:
                        print("I don't think that's a habit. Let's try again...")
                    else:
                        choice = questionary.select(
                            "What do you want to modify?",
                            choices=["Name", "Regularity", "Description"]
                        ).ask()
                        if choice == "Name":
                            try_again2 = True
                            while try_again2:
                                new_name = questionary.text("What do you want to change the name to?\n",
                                                            validate=lambda text: True if len(
                                                                text) > 0 else "Please enter a value").ask()
                                habit_new = Habit(db, user.id, new_name)
                                habit_new.identify()
                                if habit_new.id is not None:
                                    print("You already have a habit with the same name.\n")
                                else:
                                    habit.name = habit_new.name
                                    try_again2 = False
                        elif choice == "Regularity":
                            new_reg = questionary.text("What do you want to change the regularity to?\n",
													   validate=lambda text: True if len(
														   text) > 0 and text.isnumeric() else "Please enter a value"
													   ).ask()
                            habit.regularity = int(new_reg)
                        else:
                            new_desc = questionary.text("What do you want to change the description to?\n").ask()
                            habit.description = new_desc
                        habit.save()
                        print("Your habit has been modified! \nNow...")
                        try_again = False

            elif choice == "Delete":
                try_again = True
                while try_again:
                    print("\nHere are all your current habits \n")
                    print_habits(habits_data)
                    name = questionary.text("Which habit do you want to delete?\n").ask()
                    habit = Habit(db, user.id, name)
                    habit.identify()
                    if habit.id is None:
                        print("I don't think that's a habit. Let's try again...")
                    else:
                        choice = questionary.select(
                            "Are you sure? This will delete all habit logs as well. This can't be undone.",
                            choices=["Yes, delete the habit", "Nope, I changed my mind"]
                        ).ask()
                        if choice == "Yes, delete the habit":
                            habit.delete()
                            print("PUFF. Your habit and its logs have been deleted. \nNow...")
                        else:
                            print("Ok, I'll keep the habit and its logs for now...\nNow...")
                        try_again = False

            elif choice == "List":
                choice = questionary.select(
                    "Do you want to list habits or a habit's logs?\n",
                    choices=["Habits", "A habit's logs"]
                ).ask()
                if choice == "Habits":
                    choice = questionary.select(
                        "Which habits do you want to list?",
                        choices=["All", "With a specific regularity"]
                    ).ask()
                    if choice == "All":
                        print("\nHere are all your current habits:\n")
                        print_habits(habits_data)
                    else:
                        reg = questionary.text("What regularity? (in days, e.g. 1 for daily)\n",
											   validate=lambda text: True if len(
												   text) > 0 and text.isnumeric() else "Please enter a value"
											   ).ask()
                        print(f"\nHere are all your current habits with a regularity of {reg}\n")
                        print_habits(habits_data, int(reg))
                else:
                    try_again = True
                    while try_again:
                        print("\nHere are all your current habits:\n")
                        print_habits(habits_data)
                        name = questionary.text("Which habit's logs do you want to view?\n").ask()
                        habit = Habit(db, user.id, name)
                        habit.identify()
                        if habit.id is None:
                            print("I don't think that's a habit. Let's try again...")
                        else:
                            print(f"\nHere are all the times you logged {habit.name}:")
                            print_logs(habit.logs_data)
                            try_again = False

            elif choice == "Analyze":
                choice = questionary.select(
                    "From which habits do you want to analyze the longest streak?",
                    choices=["All", "With a specific regularity", "A specific habit"]
                ).ask()
                if choice == "All":
                    print("The habit with the longest streak is:")
                    print_longest_streak_of_streaks(
                        habits_data, db, "with a streak of:")
                elif choice == "With a specific regularity":
                    reg = questionary.text("What regularity? (in days, e.g. 1 for daily)\n",
										   validate=lambda text: True if len(
											   text) > 0 and text.isnumeric() else "Please enter a value"
										   ).ask()
                    subset_habits_data = return_subset_habits(habits_data, int(reg))
                    print(f"The habit with a regularity of {reg} with the longest streak is:")
                    print_longest_streak_of_streaks(subset_habits_data, db, "with a streak of:")
                else:
                    try_again = True
                    while try_again:
                        print("\nHere are all your current habits:")
                        print_habits(habits_data)
                        name = questionary.text("Which habit do you want to analyze?\n").ask()
                        habit = Habit(db, user.id, name)
                        habit.identify()
                        if habit.id is None:
                            print("I don't think that's a habit. Let's try again...")
                        else:
                            print(f"\nThe habit:")
                            single_habits_data = [db_get_habit_data(db, habit.user, habit.name)]
                            print_longest_streak_of_streaks(
                                single_habits_data, db, "has a longest streak of:")
                            try_again = False
                print("\nNow...")

            else:
                print("Goodbye!")
                go = False
    else:
        print("Ok. See you next time.")

if __name__ == '__main__':
    cli()
