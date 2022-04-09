# Habitoro

Habitoro is a command-line habit tracker written in Python and SQLite.

## Summary

Habitoro is a command-line habit tracker where a user can create/login to an account and
track habits of their choice. Users can also choose how regularly they want to try to track 
their habit, give habits descriptions, and determine their longest streak of successfully 
logged habits.

### Languages & Technologies:

- Python 3.9.7
- SQLite3

### Libraries:

- questionary
- pytest

## What can I do with this app?

You can:

- Create & login to an account
- Create and add habits to a list of habits you want to track
- Modify the name, regularity, or description of your habits
- Log your habits when you complete them
- View your habits (all or with a specific regularity)
- View when you logged a habit
- Assess the success of your habit tracking by determining the longest streak of:
  - A single habit
  - Habits with the same regularity
  - All your habits


## Installation

```shell
pip install -r requirements.txt
```

## Usage

### To start Habitoro:
```shell
python main.py
```


### Here’s how a command line session looks like:
```
$ Hai. Welcome to Habitoro.
$ ? What's your name?
Helyne

$ Welcome, Helyne.
$ ? Would you like to see your habits? (Y/n)
No

$ ? Are you ready to track some habits? (Y/n)
Yes

$ ? What do you want to do with your habits? (Use arrow keys)
 » Create
   Log
   Analyse
   List
   Modify
   Delete
   Exit
```


### Creating a new habit :seedling:

To create a new habit, select "Create", then follow the instructions on the screen to 
give your habit a name, a regularity, and a description.

```
# ? What do you want to do with your habits? (Use arrow keys)
» Create
  Log
  Analyze
  List
  Modify
  Delete
  Exit
  
$ ? What's the name of your habit?
New Habit

$ ? How often do you want to do this habit (in days)? e.g. daily = 1, weekly = 7, monthly = 30
1

$ ? What's the description of your habit? (optional)
New daily habit

Thanks for the info. Your habit has been saved!
```

### Viewing a list of your habits :eyes:
Habitoro comes with some predefined habits to help you understand how to use the app. To show a list of 
all your daily habits:
```
# ? What do you want to do with your habits? (Use arrow keys)
  Create
  Log
  Analyze
» List
  Modify
  Delete
  Exit

# ? Do you want to list habits or a habit's logs?
(Use arrow keys)
» Habits
  A habit's logs

# ? Which habits do you want to list?
  All
» With a specific regularity

# ? What regularity? (in days, e.g. 1 for daily)
1

Here are all your current habits with a regularity of 1

Habit name (regularity in days): Description
-----------------------------------------------
New habit (1): New daily habit
jog (1): 15-30 minute jog
meditate (1): 5 minutes of mindful breathing
not smoke cigarette (1): quit smoking!
-----------------------------------------------
```
### Assessing your best habits :nail_care:
Habito can also help you monitor which habits you are most successful at. To determine your habit with the 
longest streak:
```
# ? What do you want to do with your habits? (Use arrow keys)
  Create
  Log
» Analyze
  List
  Modify
  Delete
  Exit

# ? From which habits do you want to analyze the longest streak? (Use arrow keys)
 » All
   With a specific regularity
   A specific habit

The habit with the longest streak is:
not smoke cigarette

with a streak of:
17
```


## Tests
To run the test suite:
```shell
pytest
```
