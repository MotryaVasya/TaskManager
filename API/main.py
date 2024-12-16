from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, CheckConstraint
from datetime import datetime, timedelta

app = Flask(__name__)

# PostgreSQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:MNB1787mnb@localhost:5432/TaskManager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create the Tasks table if it doesn't exist
with app.app_context():
    db.create_all()

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, CheckConstraint('priority BETWEEN 1 AND 9'), default=5)
    start_date = db.Column(DateTime, default=datetime.now)
    finish_date = db.Column(DateTime, default=lambda: datetime.now() + timedelta(days=1))

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'name': task.name, 'description': task.description,
                     'priority': task.priority, 'start_date': task.start_date,
                     'finish_date': task.finish_date} for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    if not request.json or 'name' not in request.json or 'description' not in request.json or 'priority' not in request.json:
        return jsonify({"error": "Необходимо передать поля name, description и priority"}), 400

    task = Task(
        name=request.json['name'],
        description=request.json['description'],
        priority=request.json['priority'],
        start_date=request.json.get('start_date', datetime.now()),
        finish_date=request.json.get('finish_date', datetime.now() + timedelta(days=1))
    )

    try:
        db.session.add(task)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

    return jsonify({'id': task.id, 'name': task.name, 'description': task.description,
                    'priority': task.priority, 'start_date': task.start_date,
                    'finish_date': task.finish_date}), 201

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

    return jsonify({'id': task.id, 'name': task.name, 'description': task.description,
                    'priority': task.priority, 'start_date': task.start_date,
                    'finish_date': task.finish_date})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({"error": "Задача не найдена"}), 404

    try:
        db.session.delete(task)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Задача успешно удалена"}), 204

if __name__ == '__main__':
    app.run(debug=True)