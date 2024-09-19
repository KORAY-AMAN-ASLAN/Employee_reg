# create_db.py
from app import db, Employee, app

# Create the database and add five employees
with app.app_context():
    db.create_all()  # Create tables if they don't exist

    # Add five employees
    employees = [
        Employee(name='John Doe', unique_code='E001'),
        Employee(name='Jane Smith', unique_code='E002'),
        Employee(name='Alice Johnson', unique_code='E003'),
        Employee(name='Bob Brown', unique_code='E004'),
        Employee(name='Charlie Green', unique_code='E005'),
    ]

    # Add and commit the employees
    db.session.bulk_save_objects(employees)
    db.session.commit()

    print("Database created and 5 employees added.")
