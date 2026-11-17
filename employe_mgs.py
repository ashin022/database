import sqlite3
conn = sqlite3.connect("employe.db")
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT,
        salary REAL CHECK (salary > 0),
        join_date TEXT DEFAULT CURRENT_DATE,
        is_active INTEGER DEFAULT 1
    )
""")
conn.commit()

COLUMNS = ("id", "name", "email", "department", "salary", "join_date", "is_active")


def _valid_salary(value):
    try:
        salary = float(value)
    except (TypeError, ValueError):
        print("Salary must be a number greater than 0.")
        return None
    if salary <= 0:
        print("Salary must be greater than 0.")
        return None
    return salary


def _print_rows(rows):
    if not rows:
        print("No employees found.")
        return
    widths = [max(len(COLUMNS[i]), *(len(str(row[i])) for row in rows)) for i in range(len(COLUMNS))]
    print(" | ".join(COLUMNS[i].ljust(widths[i]) for i in range(len(COLUMNS))))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(str(row[i]).ljust(widths[i]) for i in range(len(COLUMNS))))


def add_employee(name, email, department, salary):
    salary = _valid_salary(salary)
    if salary is None:
        return
    if not isinstance(email, str) or "@" not in email:
        print("Please enter a valid email address containing @.")
        return
    try:
        cursor.execute(
            "INSERT INTO employees (name, email, department, salary) VALUES (?, ?, ?, ?)",
            (name, email, department, salary),
        )
        conn.commit()
        print("Employee added successfully.")
    except sqlite3.IntegrityError:
        conn.rollback()
        print("An employee with that email already exists.")


def view_employees():
    cursor.execute("SELECT * FROM employees WHERE is_active = ? ORDER BY id", (1,))
    _print_rows(cursor.fetchall())


def get_employee(employee_id):
    cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    row = cursor.fetchone()
    if row is None:
        print("Not found.")
    else:
        _print_rows([row])


def search_employee(keyword):
    cursor.execute(
        "SELECT * FROM employees WHERE is_active = ? AND LOWER(name) LIKE LOWER(?) ORDER BY id",
        (1, "%" + str(keyword) + "%"),
    )
    _print_rows(cursor.fetchall())


def filter_by_department(dept):
    cursor.execute(
        "SELECT * FROM employees WHERE is_active = ? AND LOWER(department) = LOWER(?) ORDER BY id",
        (1, dept),
    )
    _print_rows(cursor.fetchall())


def filter_by_salary(min_salary, max_salary):
    minimum = _valid_salary(min_salary)
    try:
        maximum = float(max_salary)
    except (TypeError, ValueError):
        print("Salary range must contain numbers.")
        return
    if minimum is None:
        return
    if maximum < minimum:
        print("Maximum salary must be at least the minimum salary.")
        return
    cursor.execute(
        "SELECT * FROM employees WHERE is_active = ? AND salary BETWEEN ? AND ? ORDER BY salary",
        (1, minimum, maximum),
    )
    _print_rows(cursor.fetchall())


def sort_employees(column, order):
    allowed_columns = {"name": "name", "salary": "salary", "join_date": "join_date"}
    column = str(column).lower()
    order = str(order).upper()
    if column not in allowed_columns or order not in ("ASC", "DESC"):
        print("Choose name, salary, or join_date and ascending or descending order.")
        return
    cursor.execute(
        "SELECT * FROM employees WHERE is_active = ? ORDER BY " + allowed_columns[column] + " " + order,
        (1,),
    )
    _print_rows(cursor.fetchall())


def update_salary(employee_id, new_salary):
    salary = _valid_salary(new_salary)
    if salary is None:
        return
    cursor.execute("UPDATE employees SET salary = ? WHERE id = ? AND is_active = ?", (salary, employee_id, 1))
    if cursor.rowcount == 0:
        print("No employee found.")
    else:
        conn.commit()
        print("Salary updated.")


def update_department(employee_id, new_dept):
    cursor.execute(
        "UPDATE employees SET department = ? WHERE id = ? AND is_active = ?",
        (new_dept, employee_id, 1),
    )
    if cursor.rowcount == 0:
        print("No employee found.")
    else:
        conn.commit()
        print("Department updated.")


def give_raise(department, percent):
    try:
        percentage = float(percent)
    except (TypeError, ValueError):
        print("Percent must be a number.")
        return
    if percentage < 0:
        print("Percent cannot be negative.")
        return
    cursor.execute(
        "UPDATE employees SET salary = salary * ? WHERE LOWER(department) = LOWER(?) AND is_active = ?",
        (1 + percentage / 100, department, 1),
    )
    updated = cursor.rowcount
    conn.commit()
    print("Employees updated: " + str(updated))


def remove_employee(employee_id):
    confirmation = input("Remove this employee? (y/n): ").strip().lower()
    if confirmation != "y":
        print("Removal cancelled.")
        return
    cursor.execute("UPDATE employees SET is_active = ? WHERE id = ? AND is_active = ?", (0, employee_id, 1))
    if cursor.rowcount == 0:
        print("No employee found.")
    else:
        conn.commit()
        print("Employee removed.")


def restore_employee(employee_id):
    cursor.execute("UPDATE employees SET is_active = ? WHERE id = ? AND is_active = ?", (1, employee_id, 0))
    if cursor.rowcount == 0:
        print("No employee found.")
    else:
        conn.commit()
        print("Employee restored.")


def view_removed():
    cursor.execute("SELECT * FROM employees WHERE is_active = ? ORDER BY id", (0,))
    _print_rows(cursor.fetchall())


def show_summary():
    cursor.execute(
        "SELECT COUNT(*), AVG(salary), MAX(salary), MIN(salary) FROM employees WHERE is_active = ?",
        (1,),
    )
    total, average, highest, lowest = cursor.fetchone()
    print("Active employees: " + str(total))
    print("Average salary: " + ("N/A" if average is None else format(average, ".2f")))
    print("Highest salary: " + ("N/A" if highest is None else format(highest, ".2f")))
    print("Lowest salary: " + ("N/A" if lowest is None else format(lowest, ".2f")))
    cursor.execute(
        "SELECT department, COUNT(*), AVG(salary) FROM employees WHERE is_active = ? GROUP BY department ORDER BY department",
        (1,),
    )
    print("\nDepartment | Employees | Average salary")
    for department, count, dept_average in cursor.fetchall():
        print(str(department) + " | " + str(count) + " | " + format(dept_average, ".2f"))


def top_earners(n):
    try:
        limit = int(n)
    except (TypeError, ValueError):
        print("Enter a whole number for the number of employees.")
        return
    if limit < 0:
        print("Number of employees cannot be negative.")
        return
    cursor.execute(
        "SELECT * FROM employees WHERE is_active = ? ORDER BY salary DESC LIMIT ?",
        (1, limit),
    )
    _print_rows(cursor.fetchall())


def export_to_csv(filename):
    cursor.execute("SELECT * FROM employees WHERE is_active = ? ORDER BY id", (1,))
    rows = cursor.fetchall()
    try:
        with open(filename, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(COLUMNS)
            writer.writerows(rows)
        print("Exported " + str(len(rows)) + " active employees.")
    except OSError as error:
        print("Could not export CSV: " + str(error))


def _read_number(prompt, whole=False):
    try:
        value = input(prompt).strip()
        return int(value) if whole else float(value)
    except ValueError:
        print("Please enter a valid number.")
        return None


def main():
    menu = (
        "\n1. Add employee\n2. View all\n3. Search\n4. Filter by dept\n"
        "5. Filter by salary\n6. Sort\n7. Update salary\n8. Give raise\n"
        "9. Remove employee\n10. Restore employee\n11. Summary report\n"
        "12. Top earners\n13. Export to CSV\n14. Exit"
    )
    while True:
        print(menu)
        choice = input("Choice: ").strip()
        if choice == "1":
            name = input("Name: ").strip()
            email = input("Email: ").strip()
            department = input("Department: ").strip()
            salary = _read_number("Salary: ")
            if salary is not None:
                add_employee(name, email, department, salary)
        elif choice == "2":
            view_employees()
        elif choice == "3":
            search_employee(input("Name keyword: ").strip())
        elif choice == "4":
            filter_by_department(input("Department: ").strip())
        elif choice == "5":
            minimum = _read_number("Minimum salary: ")
            maximum = _read_number("Maximum salary: ")
            if minimum is not None and maximum is not None:
                filter_by_salary(minimum, maximum)
        elif choice == "6":
            sort_employees(input("Sort by (name/salary/join_date): ").strip(), input("Order (asc/desc): ").strip())
        elif choice == "7":
            employee_id = _read_number("Employee ID: ", whole=True)
            salary = _read_number("New salary: ")
            if employee_id is not None and salary is not None:
                update_salary(employee_id, salary)
        elif choice == "8":
            department = input("Department: ").strip()
            percentage = _read_number("Raise percent: ")
            if percentage is not None:
                give_raise(department, percentage)
        elif choice == "9":
            employee_id = _read_number("Employee ID: ", whole=True)
            if employee_id is not None:
                remove_employee(employee_id)
        elif choice == "10":
            employee_id = _read_number("Employee ID: ", whole=True)
            if employee_id is not None:
                restore_employee(employee_id)
        elif choice == "11":
            show_summary()
        elif choice == "12":
            count = _read_number("Number of employees: ", whole=True)
            if count is not None:
                top_earners(count)
        elif choice == "13":
            export_to_csv(input("CSV filename: ").strip())
        elif choice == "14":
            break
        else:
            print("Invalid menu choice. Enter a number from 1 to 14.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
    finally:
        conn.close()

