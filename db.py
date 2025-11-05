import sqlite3

# Step 1: Create the table (if it doesn't exist)
def create_table():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            department TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Step 2: Add a new employee
def add_employee(name, department, role):
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('INSERT INTO employees (name, department, role) VALUES (?, ?, ?)', (name, department, role))
    conn.commit()
    conn.close()

# Step 3: View all employees
def view_employees():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('SELECT * FROM employees')
    data = c.fetchall()
    conn.close()
    return data

# Optional: Delete employee
def delete_employee(emp_id):
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('DELETE FROM employees WHERE id=?', (emp_id,))
    conn.commit()
    conn.close()

# Update existing employee
def update_employee(emp_id, name, department, role):
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('''
        UPDATE employees
        SET name = ?, department = ?, role = ?
        WHERE id = ?
    ''', (name, department, role, emp_id))
    conn.commit()
    conn.close()
