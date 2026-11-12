import sqlite3

conn = sqlite3.connect('school.db')

cursor = conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS STUDENTS (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME TEXT NOT NULL,
                AGE INTEGER ,
                COURSE TEXT NOT NULL
        )
''')

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('John ', 20, 'Computer Science'))

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('danni ', 25, 'ECE'))

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('nithi ', 29, 'Msw'))

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('athul ', 21, 'python'))

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('sree ', 26, 'Bca'))

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('viki ', 24, 'cyber'))

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('ammu', 27, ' Science'))

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('daniel ', 22, 'Computer Science'))

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('alex ', 24, 'mech'))

cursor.execute('''
         INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
''', ('malu ', 20, 'civil'))

conn.commit()

# cursor.execute('''
#         SELECT  * 
#         FROM STUDENTS
# ''')

# data = cursor.fetchall()
# print(data)

conn.close()