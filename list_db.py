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

students = [("Amith",22,"eee"), ("Abhi",22,"Mechanical"), ("Philip",32,"Mechanical"), ("Catherine",22,"civil"), ("Gopal",22,"EC")]



# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('John ', 20, 'Computer Science'))

# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('danni ', 25, 'ECE'))

# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('nithi ', 29, 'Msw'))

# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('athul ', 21, 'python'))

# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('sree ', 26, 'Bca'))

# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('viki ', 24, 'cyber'))

# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('ammu', 27, ' Science'))

# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('daniel ', 22, 'Computer Science'))

# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('alex ', 24, 'mech'))

# cursor.execute('''
#          INSERT INTO STUDENTS (NAME, AGE, COURSE) VALUES (?, ?, ?)
# ''', ('malu ', 20, 'civil'))

# conn.commit()

# cursor.execute('''
#         SELECT  * 
#         FROM STUDENTS
# ''')

# data = cursor.fetchall()
# print(data)

# conn.close()

course = 'Computer Science'
id = 6
cursor.execute('''
    UPDATE students
    SET course = ?
    WHERE id = ?
''',(course,id))
# cursor.execute('''
#     DELETE
#     FROM students
#     WHERE id = ?
# ''',(4,))
# conn.commit()
# cursor.execute('''
#     SELECT *
#     FROM students
# ''')

# cursor.execute('''
#     SELECT name
#     FROM students
# ''')

# cursor.execute('''
#     SELECT name,course
#     FROM students
# ''')
# cursor.execute('''
#     SELECT *
#     FROM students
#     WHERE course = ?
# ''',('Computer Science',))
# cursor.execute('''
#     SELECT *
#     FROM students
#     WHERE age > ? AND name LIKE ?
# ''',(19,'A%'))
# cursor.execute('''
#     SELECT
#     COUNT(*) FROM students
#     WHERE age > ? AND name LIKE ?
# ''',(19,'S%'))
# cursor.execute('''
#     SELECT *
#     FROM students
#     WHERE age > ? AND name LIKE ?
# ''',(19,'AM%'))
# cursor.execute('''
#     SELECT COUNT(*)
#     FROM students
#     WHERE age > ?
# ''',(21,))
# data = cursor.fetchall()
# # data = cursor.fetchmany(5)
# # data = cursor.fetchone()
# print(data)

# print(cursor.fetchone())
# cursor.execute('alter table students add column register_no integer')
# cursor.execute('alter table students rename column course to department')
# # cursor.execute('alter table synnefo rename to students')
# cursor.execute('drop table if exists students')

cursor.Execute('''
     SELECT *
     FROM students
     ORDER BY name DESC
''')
print(cursor.fetchall())
conn.close()