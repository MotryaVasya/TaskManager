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
    user_id = db.Column(db.String(50), nullable=False) # Уникальный идентификатор пользователя
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Integer, CheckConstraint('priority BETWEEN 1 AND 9'), default=5)
    start_date = db.Column(DateTime, default=datetime.now)
    finish_date = db.Column(DateTime, default=lambda: datetime.now() + timedelta(days=1))


@app.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': task.id, 'name': task.name, 'description': task.description,
                     'priority': task.priority, 'start_date': task.start_date,
                     'finish_date': task.finish_date} for task in tasks])

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if task:
        return jsonify({'id': task.id, 'name': task.name, 'description': task.description,
                        'priority': task.priority, 'start_date': task.start_date,
                        'finish_date': task.finish_date})
    else:
        return jsonify({'error': 'Task not found or does not belong to the user'}), 404

@app.route('/tasks', methods=['POST'])
def add_task():
    if not request.json or 'user_id' not in request.json or 'name' not in request.json:
        return jsonify({"error": "Необходимо передать поля user_id, name, description и priority"}), 400

    task = Task(
        user_id=request.json['user_id'],
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
    user_id = request.json.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task not found or does not belong to the user"}), 404

    if not request.json or 'name' not in request.json or 'description' not in request.json or 'priority' not in request.json:
        return jsonify({"error": "Fields name, description, and priority are required"}), 400

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
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task not found or does not belong to the user"}), 404

    try:
        db.session.delete(task)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": "Task successfully deleted"}), 204


if __name__ == '__main__':
    app.run(debug=True)