import sqlite3

def get_db(name="habits_main.db"):
    db = sqlite3.connect(name)
    create_tables(db)
    return db

def create_tables(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
	    	id INTEGER PRIMARY KEY AUTOINCREMENT,
	    	name TEXT)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS habits (
    		id INTEGER PRIMARY KEY AUTOINCREMENT,
    		user_id INTEGER,
    		name TEXT,
    		regularity INTEGER,
    		description TEXT,
    		created INTEGER,
    		FOREIGN KEY (user_id) REFERENCES users(id),
    		UNIQUE(user_id, name))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS habit_logs (
	    	id INTEGER PRIMARY KEY AUTOINCREMENT,
		    habit_id INTEGER,
		    log INTEGER,
		    FOREIGN KEY (habit_id) REFERENCES habits(id))""")

    db.commit()

def db_get_user_data(db, user_name):
    cur = db.cursor()
    cur.execute("SELECT * FROM users WHERE name=?", [user_name])
    return cur.fetchone()

def add_user(db, user_name):
    cur = db.cursor()
    cur.execute("INSERT INTO users VALUES (NULL,?)", [user_name])
    db.commit()

def db_get_user_habits(db, user_id):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE user_id=?", [user_id])
    return cur.fetchall()

def update_habit(db, habit_id, habit_name, regularity, description):
    cur = db.cursor()
    cur.execute("UPDATE habits SET name=?, regularity=?, description=? WHERE id=?",
                (habit_name, regularity, description, habit_id))
    db.commit()

def add_habit(db, user_id, habit_name, regularity, description):
    cur = db.cursor()
    cur.execute("INSERT INTO habits VALUES (NULL, ?, ?, ?, ?, strftime('%s', 'now'))",
                (user_id, habit_name, regularity, description))
    db.commit()

def db_get_habit_data(db, user_id, habit_name):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE user_id=? AND name=?",
                (user_id, habit_name))
    return cur.fetchone()

def delete_habit(db, habit_id):
    cur = db.cursor()
    cur.execute("DELETE FROM habits WHERE id=?", [habit_id])
    db.commit()

def delete_habit_logs(db, habit_id):
    cur = db.cursor()
    cur.execute("DELETE FROM habit_logs WHERE habit_id=?", [habit_id])
    db.commit()

def add_log(db, habit_id):
    cur = db.cursor()
    cur.execute("INSERT INTO habit_logs VALUES (NULL, ?, strftime('%s', 'now'))", [habit_id])
    db.commit()

def db_get_habit_log_data(db, habit_id):
    cur = db.cursor()
    cur.execute("SELECT * FROM habit_logs WHERE habit_id=?", [habit_id])
    return cur.fetchall()

def add_manual_log(db, habit_id, timestamp):
    cur = db.cursor()
    cur.execute("INSERT INTO habit_logs VALUES (NULL, ?, ?)", (habit_id, timestamp))
    db.commit()

# def add_timestamp(db, habit_id):
#     for x in range(1,5):
#         add_manual_log(db, habit_id, (1649439226+(x*604800)))

