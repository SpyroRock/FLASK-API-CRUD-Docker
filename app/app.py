from flask import Flask, render_template, request, redirect, url_for, flash
from flask.globals import session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.secret_key = "Secret Key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.getenv('DB_USER', 'root'),
    os.getenv('DB_PASSWORD', 'root'),
    os.getenv('DB_HOST', 'mysql'),
    os.getenv('DB_NAME', 'crud')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
 
#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    todos = db.relationship('Task', backref='employee_tasklist')

    def __init__(self, name, email, phone):
 
        self.name = name
        self.email = email
        self.phone = phone

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    completed = db.Column(db.String(50))
    employee_id = db.Column(db.Integer, db.ForeignKey('data.id'), nullable=False)

    def __init__(self, text, completed, employee_id):
 
        self.text = text
        self.completed = completed
        self.employee_id = employee_id
     
@app.route('/')
def front_layout():
    all_data_employees = Data.query.all()
    all_data_task = Task.query.all()
    return render_template('front_layout.html', employees = all_data_employees, tasks = all_data_task)

@app.route('/index')
def Index():
    all_data = Data.query.all()
    return render_template("index.html", employees = all_data)
 
@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == 'POST':
 
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
 
        my_data = Data(name, email, phone)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Employee Inserted Successfully")
 
        return redirect(url_for('Index'))
 
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Data.query.get(request.form.get('id'))
 
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
 
        db.session.commit()
        flash("Employee Updated Successfully")
 
        return redirect(url_for('Index'))
 
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
 
    return redirect(url_for('Index'))
 
@app.route('/index_task')
def Index_tasks():
    all_data = Task.query.all()
 
    return render_template("index_task.html", tasks = all_data)

@app.route('/insert_tasks', methods = ['POST'])
def insert_task():
    if request.method == 'POST':

        text = request.form['text']
        completed = request.form['completed']
        employee_id = request.form['employee_id']
        my_data = Data.query.get(request.form.get('id'))

        ids = [id[0] for id in Data.query.with_entities(Data.id).all()]

        for id_values in ids:
            if employee_id != id_values:
                flash("Employee ID not found. You are not able to insert this Task")
                return redirect(url_for('Index_tasks'))
        
        my_data = Task(text, completed, employee_id)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Task Inserted Successfully")
 
        return redirect(url_for('Index_tasks'))

@app.route('/update_task', methods = ['GET', 'POST'])
def update_task():
    if request.method == 'POST':
        my_data = Task.query.get(request.form.get('id'))
 
        my_data.text = request.form['name']
        my_data.completed = request.form['completed']
        my_data.employee_id = request.form['employee_id']
 
        db.session.commit()
        flash("Task Updated Successfully")
 
        return redirect(url_for('Index_tasks'))

@app.route('/delete_task/<id>/', methods = ['GET', 'POST'])
def delete_task(id):
    my_data = Task.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Task Deleted Successfully")
 
    return redirect(url_for('Index_tasks'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)