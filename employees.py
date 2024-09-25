from app import db, Employee, app

# DB
with app.app_context():
    db.create_all()

    employees = [
        Employee(name='John Doe', unique_code='E001'),
        Employee(name='Jane Smith', unique_code='E002'),
        Employee(name='Alice Johnson', unique_code='E003'),
        Employee(name='Bob Brown', unique_code='E004'),
        Employee(name='Charlie Green', unique_code='E005'),
    ]

    db.session.bulk_save_objects(employees)
    db.session.commit()

    print("Database created and 5 employees added.")
