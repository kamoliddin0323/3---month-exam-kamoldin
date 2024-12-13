import sqlite3

connection = sqlite3.connect('course.db')

cursor = connection.cursor()


def create_table_course_data():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS course_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name VARCHAR(200) NOT NULL,
        course_price INTEGER,
        complete_information VARCHAR,
        teacher VARCHAR
        )
    ''')
    connection.commit()

def get_all_course_data():
    data = cursor.execute('SELECT course_name,id FROM course_data')
    return data.fetchall()

def get_count_course():
    data = cursor.execute('SELECT * FROM course_data')
    return cursor.fetchall()


def inset_row_course_data(course_name,course_price,complete_information,teacher):
    cursor.execute('''
    INSERT INTO course_data(course_name,course_price,complete_information,teacher)
    VALUES (?, ?, ?, ?) ''',(course_name,course_price,complete_information,teacher))
    connection.commit()