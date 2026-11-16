import sqlite3
conn = sqlite3.connect('school2.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        age INTEGER,
        grade TEXT
    )
''')

def add_student(name,email,age,grade):
    try:
        cursor.execute('''
            INSERT INTO students (name,email,age,grade)
            VALUES (?, ?, ?, ?)
        ''',(name,email,age,grade))
        conn.commit()
        print("Student added.")
    except sqlite3.IntegrityError as e:
        print(f"Email already exist: {e}")

def view_students():
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    if not students:
        print("No students found.")
    else:
        for student in students:
            print(student)

def search_student(keyword):
    cursor.execute('''
        SELECT *
        FROM students
        WHERE name LIKE ?
    ''',(f'%{keyword}%',))
    students = cursor.fetchall()
    if not students:
        print("No students found.")
    else:
        for student in students:
            print(student)

def update_grade(student_id, new_grade):
    cursor.execute('''
        UPDATE students
        SET grade = ?
        WHERE id = ?
    ''',(new_grade, student_id))
    conn.commit()
    if cursor.rowcount == 0:
        print("No student found.")
    else:
        print("Grade updated")

def delete_student(student_id):
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    if cursor.rowcount == 0:
        print("No student found.")
    else:
        print("Grade updated")

while True:
    print('1. Add 2. View all 3. Search 4. Update grade 5. Delete 6. Exit')
    choice = input("Enter your choice: ")
    match choice:
        case '1':
            name = input("Name: ")
            email = input("Email: ")
            age = int(input("Age: "))
            grade = input("Grade: ")
            add_student(name,email,age,grade)
        case '2':
            view_students()
        case '3':
            search_student(input("Search student: "))
        case '4':
            view_students()
            id = int(input("Enter ID: "))
            grade = input("New Grade: ")
            update_grade(id, grade)
        case '5':
            view_students()
            id = int(input("Enter Id: "))
            delete_student(id)
        case '6':
            print("Exiting...")
            break
        case _:
            print("Invalid choice...")

conn.close()