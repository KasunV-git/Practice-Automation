import pytest
from app import create_app
from app.database import db, reset_db


@pytest.fixture
def app():
    """
    Create and configure a test application instance.
    Uses an in-memory SQLite database for testing.
    """
    config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    
    app = create_app(config)
    
    with app.app_context():
        reset_db()
    
    yield app


@pytest.fixture
def client(app):
    """
    Create a test client for the application.
    Used to make HTTP requests in tests.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a CLI runner for the application.
    """
    return app.test_cli_runner()


@pytest.fixture
def sample_task(app):
    """
    Create a sample task in the database.
    Useful for tests that need existing data.
    """
    from app.models import Task
    
    with app.app_context():
        task = Task(
            title='Sample Task',
            description='This is a sample task',
            completed=False
        )
        db.session.add(task)
        db.session.commit()
        
        # Refresh to get the ID
        db.session.refresh(task)
        task_id = task.id
    
    return task_id