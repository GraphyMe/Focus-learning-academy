import sqlite3

def print_table_schema():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(students);")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

print_table_schema()
