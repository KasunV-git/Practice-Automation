import pytest
from app.database import db
from app.models import Task


@pytest.mark.database
class TestDatabase:
    """Tests for database operations."""
    
    def test_database_initialization(self, app):
        """Test that database initializes correctly."""
        with app.app_context():
            # Check that Task table exists
            assert db.engine.dialect.has_table(db.engine.connect(), 'tasks')
    
    def test_create_task_in_database(self, app):
        """Test creating a task in the database."""
        with app.app_context():
            task = Task(title='Test Task', description='Test Description')
            db.session.add(task)
            db.session.commit()
            
            # Verify task was created
            assert task.id is not None
            assert task.title == 'Test Task'
    
    def test_query_task_from_database(self, app, sample_task):
        """Test querying a task from the database."""
        with app.app_context():
            task = Task.query.get(sample_task)
            
            assert task is not None
            assert task.title == 'Sample Task'
    
    def test_update_task_in_database(self, app, sample_task):
        """Test updating a task in the database."""
        with app.app_context():
            task = Task.query.get(sample_task)
            task.completed = True
            db.session.commit()
            
            # Verify update
            updated_task = Task.query.get(sample_task)
            assert updated_task.completed is True
    
    def test_delete_task_from_database(self, app, sample_task):
        """Test deleting a task from the database."""
        with app.app_context():
            task = Task.query.get(sample_task)
            db.session.delete(task)
            db.session.commit()
            
            # Verify deletion
            deleted_task = Task.query.get(sample_task)
            assert deleted_task is None