import pytest
from datetime import datetime
from app.models import Task


@pytest.mark.unit
class TestTaskModel:
    """Unit tests for Task model."""
    
    def test_task_creation(self, app):
        """Test creating a Task instance."""
        with app.app_context():
            task = Task(title='New Task', description='Task description', completed=False)
            
            assert task.title == 'New Task'
            assert task.description == 'Task description'
            assert task.completed is False
    
    def test_task_default_values(self, app):
        """Test default values for Task model."""
        with app.app_context():
            from app.database import db
            
            task = Task(title='Minimal Task')
            db.session.add(task)
            db.session.flush()  # This applies defaults
            
            assert task.description is None
            assert task.completed is False
    
    def test_task_to_dict(self, app):
        """Test converting Task to dictionary."""
        with app.app_context():
            from app.database import db
            
            task = Task(title='Dict Task', description='Test')
            db.session.add(task)
            db.session.flush()
            task.id = 1
            
            task_dict = task.to_dict()
            
            assert task_dict['id'] == 1
            assert task_dict['title'] == 'Dict Task'
            assert task_dict['description'] == 'Test'
            assert task_dict['completed'] is False
            assert 'created_at' in task_dict
            assert 'updated_at' in task_dict
    
    def test_task_repr(self, app):
        """Test Task string representation."""
        with app.app_context():
            task = Task(title='Repr Task')
            task.id = 5
            
            assert repr(task) == '<Task 5: Repr Task>'
    
    def test_task_timestamps(self, app):
        """Test that timestamps are set correctly."""
        with app.app_context():
            from app.database import db
            
            task = Task(title='Timestamp Task')
            db.session.add(task)
            db.session.commit()
            
            assert task.created_at is not None
            assert task.updated_at is not None
            assert isinstance(task.created_at, datetime)
            assert isinstance(task.updated_at, datetime)