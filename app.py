# app.py
from flask import Flask, render_template, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unique_code = db.Column(db.String(50), unique=True, nullable=False)
    # Relationship to time logs
    time_logs = db.relationship('TimeLog', backref='employee', lazy=True)

# Time log model
class TimeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    clock_in = db.Column(db.DateTime, nullable=True)
    clock_out = db.Column(db.DateTime, nullable=True)

@app.route('/')
def home():
    return render_template('index.html')

# Route to handle employee registration
@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    unique_code = request.form['unique_code']

    # Check if the unique code already exists
    existing_employee = Employee.query.filter_by(unique_code=unique_code).first()
    if existing_employee:
        return render_template('message.html', title="Registration Failed", message="Unique code already exists!", delay=20), 400

    # Create a new employee and save to the database
    new_employee = Employee(name=name, unique_code=unique_code)
    db.session.add(new_employee)
    db.session.commit()

    return render_template('message.html', title="Registration Successful", message=f"Employee {name} registered successfully with unique code {unique_code}.", delay=20), 200

# Clock-in route
@app.route('/clock-in', methods=['POST'])
def clock_in():
    code = request.form['unique_code']
    employee = Employee.query.filter_by(unique_code=code).first()

    if employee:
        existing_log = TimeLog.query.filter_by(employee_id=employee.id, clock_out=None).first()
        if existing_log:
            return render_template('message.html', title="Clock In Failed", message="You are already clocked in!", delay=20), 400

        log = TimeLog(employee_id=employee.id, clock_in=datetime.now())
        db.session.add(log)
        db.session.commit()
        return render_template('message.html', title="Clock In Successful", message=f"Clocked in at {log.clock_in.strftime('%Y-%m-%d %H:%M:%S')}.", delay=20), 200

    return render_template('message.html', title="Clock In Failed", message="Invalid unique code!", delay=20), 400


# Clock-out route
@app.route('/clock-out', methods=['POST'])
def clock_out():
    code = request.form['unique_code']
    employee = Employee.query.filter_by(unique_code=code).first()

    if employee:
        existing_log = TimeLog.query.filter_by(employee_id=employee.id, clock_out=None).first()
        if existing_log:
            existing_log.clock_out = datetime.now()
            db.session.commit()
            worked_hours = (existing_log.clock_out - existing_log.clock_in).total_seconds() / 3600
            return render_template('message.html', title="Clock Out Successful", message=f"Clocked out at {existing_log.clock_out.strftime('%Y-%m-%d %H:%M:%S')}. You worked {worked_hours:.2f} hours.", delay=20), 200
        return render_template('message.html', title="Clock Out Failed", message="You have not clocked in yet!", delay=20), 400

    return render_template('message.html', title="Clock Out Failed", message="Invalid unique code!", delay=20), 400


# View logs
@app.route('/logs/<string:code>', methods=['GET'])
def view_logs(code):
    employee = Employee.query.filter_by(unique_code=code).first()
    if employee:
        logs = TimeLog.query.filter_by(employee_id=employee.id).order_by(TimeLog.clock_in.desc()).all()
        return render_template('logs.html', logs=logs, employee=employee)
    return jsonify({'error': 'Invalid code!'}), 400

if __name__ == '__main__':
    app.run(debug=True)
