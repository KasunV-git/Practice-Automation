from flask_sqlalchemy import SQLAlchemy

# Create database instance
db = SQLAlchemy()


def init_db():
    """
    Initialize the database.
    Creates all tables defined in models.
    """
    from app.models import Task
    db.create_all()


def reset_db():
    """
    Reset the database.
    Drops all tables and recreates them.
    Useful for testing.
    """
    db.drop_all()
    init_db()