from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import unittest

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tasks.db')
app.config['DEBUG'] = True  # Enable debug mode
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = [task.to_dict() for task in tasks]
    return jsonify(task_list)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    task = Task.query.get_or_404(id)
    return jsonify(task.to_dict())

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        abort(400, description="Title is required")

    new_task = Task(title=title, description=description)
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400

class TestTasks(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        db.init_app(app)
        with app.test_request_context():
            db.drop_all()
            db.create_all()

    def test_get_tasks(self):
        task1 = Task(title='Task 1', description='Description 1', completed=False)
        task2 = Task(title='Task 2', description='Description 2', completed=True)
        db.session.add(task1)
        db.session.add(task2)
        db.session.commit()
        tasks = Task.query.all()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].title, 'Task 1')
        self.assertEqual(tasks[1].title, 'Task 2')

    def test_get_task(self):
        task1 = Task(title='Task 1', description='Description 1', completed=False)
        db.session.add(task1)
        db.session.commit()
        task = Task.query.get(task1.id)
        self.assertEqual(task.title, 'Task 1')

    def test_create_task(self):
        data = {'title': 'New Task', 'description': 'New Description'}
        response = app.post('/tasks', json=data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['title'], 'New Task')

    def test_update_task(self):
        task1 = Task(title='Task 1', description='Description 1', completed=False)
        db.session.add(task1)
        db.session.commit()
        data = {'title': 'Updated Task', 'completed': True}
        response = app.put('/tasks/1', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], 'Updated Task')
        self.assertEqual(response.json()['completed'], True)

    def test_delete_task(self):
        task1 = Task(title='Task 1', description='Description 1', completed=False)
        db.session.add(task1)
        db.session.commit()
        response = app.delete('/tasks/1')
        self.assertEqual(response.status_code, 204)

if __name__ == '__main__':
    unittest.main()