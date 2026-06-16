# src/database/db_setup.py
# Idhula naama oru sample company database create panrom
# 3 tables irukum: employees, departments, projects
# Idhu test panna ovvoru company-layum irukura common data structure

import sqlite3
import os

# Database file path
DB_PATH = "data/company.db"


def create_database():
    """
    # Idhu function database file create pannum
    # Already irundha, athai delete panni puthusa create pannum
    """

    # data folder illana create pannu
    os.makedirs("data", exist_ok=True)

    # Already db file irundha delete pannu - fresh start ku
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    # Database connection create pannu
    # connection = database file open pannurathu maathiri
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ---------- TABLE 1: departments ----------
    # Company-la irukura departments details
    cursor.execute("""
        CREATE TABLE departments (
            dept_id INTEGER PRIMARY KEY,
            dept_name TEXT NOT NULL,
            location TEXT,
            budget REAL
        )
    """)

    # ---------- TABLE 2: employees ----------
    # Employee details - department oda link irukum
    cursor.execute("""
        CREATE TABLE employees (
            emp_id INTEGER PRIMARY KEY,
            emp_name TEXT NOT NULL,
            dept_id INTEGER,
            salary REAL,
            hire_date TEXT,
            job_title TEXT,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        )
    """)

    # ---------- TABLE 3: projects ----------
    # Projects details - department oda link irukum
    cursor.execute("""
        CREATE TABLE projects (
            project_id INTEGER PRIMARY KEY,
            project_name TEXT NOT NULL,
            dept_id INTEGER,
            status TEXT,
            budget REAL,
            start_date TEXT,
            FOREIGN KEY (dept_id) REFERENCES departments(dept_id)
        )
    """)

    print("Tables created successfully!")

    # ---------- SAMPLE DATA INSERT PANNUROM ----------

    # Departments data
    departments_data = [
        (1, "Engineering", "Chennai", 5000000),
        (2, "Sales", "Bangalore", 3000000),
        (3, "Marketing", "Mumbai", 2000000),
        (4, "HR", "Chennai", 1000000),
        (5, "Finance", "Delhi", 1500000)
    ]

    cursor.executemany("""
        INSERT INTO departments (dept_id, dept_name, location, budget)
        VALUES (?, ?, ?, ?)
    """, departments_data)

    # Employees data
    employees_data = [
        (1, "Arun Kumar", 1, 75000, "2022-01-15", "Senior Developer"),
        (2, "Priya Sharma", 1, 65000, "2022-03-10", "Developer"),
        (3, "Vikram Singh", 1, 85000, "2021-06-20", "Tech Lead"),
        (4, "Sneha Patel", 2, 55000, "2023-02-01", "Sales Executive"),
        (5, "Karthik Raja", 2, 60000, "2022-08-15", "Sales Manager"),
        (6, "Divya Menon", 3, 50000, "2023-01-10", "Marketing Specialist"),
        (7, "Rahul Verma", 3, 58000, "2022-11-05", "Marketing Manager"),
        (8, "Ananya Reddy", 4, 45000, "2023-04-12", "HR Executive"),
        (9, "Suresh Babu", 4, 62000, "2021-09-01", "HR Manager"),
        (10, "Meera Iyer", 5, 70000, "2022-05-18", "Finance Analyst"),
        (11, "Karan Malhotra", 1, 95000, "2020-01-01", "Engineering Manager"),
        (12, "Lakshmi Narayan", 5, 80000, "2021-12-01", "Finance Manager"),
        (13, "Rohit Sharma", 2, 48000, "2023-06-01", "Sales Executive"),
        (14, "Pooja Desai", 3, 52000, "2023-03-20", "Content Writer"),
        (15, "Arjun Nair", 1, 70000, "2022-07-15", "Developer")
    ]

    cursor.executemany("""
        INSERT INTO employees (emp_id, emp_name, dept_id, salary, hire_date, job_title)
        VALUES (?, ?, ?, ?, ?, ?)
    """, employees_data)

    # Projects data
    projects_data = [
        (1, "Website Redesign", 1, "In Progress", 500000, "2024-01-01"),
        (2, "Mobile App Development", 1, "In Progress", 800000, "2024-02-15"),
        (3, "Q1 Sales Campaign", 2, "Completed", 200000, "2024-01-01"),
        (4, "Brand Awareness Drive", 3, "In Progress", 300000, "2024-03-01"),
        (5, "Employee Onboarding System", 4, "Planning", 150000, "2024-04-01"),
        (6, "Annual Audit", 5, "Completed", 100000, "2024-01-15"),
        (7, "Cloud Migration", 1, "Planning", 600000, "2024-05-01"),
        (8, "Customer Retention Program", 2, "In Progress", 250000, "2024-02-01")
    ]

    cursor.executemany("""
        INSERT INTO projects (project_id, project_name, dept_id, status, budget, start_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, projects_data)

    # Changes save pannurathu - commit panna mattum dhan database-la save aagum
    conn.commit()
    conn.close()

    print("Sample data inserted successfully!")
    print(f"Database created at: {DB_PATH}")


if __name__ == "__main__":
    # Idhu file directly run panna - database create aagum
    create_database()