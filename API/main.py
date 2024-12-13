from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pyodbc
from sqlalchemy import DateTime, CheckConstraint
from datetime import datetime, timedelta

app = Flask(__name__)

# Строка подключения к базе данных
server = 'DESKTOP-1IT6A1H'
database = 'TaskManager'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://' + server + '/' + database + '?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    priority = db.Column(db.Integer, CheckConstraint('priority BETWEEN 1 AND 9'), default=5)
    start_date = db.Column(DateTime, default=datetime.now())
    finish_date = db.Column(DateTime, default=datetime.now() + timedelta(days=1))


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'name': task.name, 'description': task.description, 'priority': task.priority,
                     'start_date': task.start_date, 'finish_date': task.finish_date} for task in tasks])


@app.route('/tasks', methods=['POST'])
def add_task():
    if not request.json or 'name' not in request.json or 'description' not in request.json or 'priority' not in request.json:
        return jsonify({"error": "Необходимо передать поля name, description и priority"}), 400

    task_name = request.json['name']
    task_description = request.json['description']
    task_priority = request.json['priority']
    task_start_date = request.json.get('start_date', datetime.now())
    task_finish_date = request.json.get('finish_date', datetime.now() + timedelta(days=1))

    task = Task()
    task.name = task_name
    task.description = task_description
    task.start_date = task_start_date
    task.finish_date = task_finish_date
    task.priority = task_priority

    try:
        db.session.add(task)
        db.session.commit()
    except Exception as e:
        print(str(e))
        return jsonify({"error": str(e)}), 500

    return jsonify({'id': task.id, 'name': task.name, 'description': task.description, 'priority': task.priority,
                    'start_date': task.start_date, 'finish_date': task.finish_date}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({"error": "Задача не найдена"}), 404

    if not request.json or 'name' not in request.json or 'description' not in request.json or 'priority' not in request.json:
        return jsonify({"error": "Необходимо передать поля name, description и priority"}), 400

    task.name = request.json['name']
    task.description = request.json['description']
    task.priority = request.json['priority']
    task.start_date = request.json.get('start_date', task.start_date)
    task.finish_date = request.json.get('finish_date', task.finish_date)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({'id': task.id, 'name': task.name, 'description': task.description, 'priority': task.priority,
                    'start_date': task.start_date, 'finish_date': task.finish_date})

if __name__ == '__main__':
    app.run(debug=True)
