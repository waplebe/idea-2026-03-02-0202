import unittest
from app import app, db
from models import Task

class TestTasks(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
        with app.test_request_context():
            db.create_all()

    def test_task_creation(self):
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()

    def test_task_retrieval(self):
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()
        retrieved_task = Task.query.get(task.id)
        self.assertEqual(retrieved_task.title, 'Test Task')
        self.assertEqual(retrieved_task.description, 'Test Description')

    def test_task_update(self):
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()
        task.completed = True
        db.session.commit()
        retrieved_task = Task.query.get(task.id)
        self.assertTrue(retrieved_task.completed)

    def test_task_deletion(self):
        task = Task(title='Test Task', description='Test Description')
        db.session.add(task)
        db.session.commit()
        db.session.delete(task)
        db.session.commit()
        self.assertFalse(Task.query.get(task.id))

if __name__ == '__main__':
    unittest.main()