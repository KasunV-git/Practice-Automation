from flask import Flask
from app.database import db, init_db


def create_app(config=None):
    """
    Application factory pattern.
    Creates and configures the Flask application.
    
    Args:
        config: Dictionary with configuration values
        
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    
    # Default configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = False
    
    # Override with custom config if provided
    if config:
        app.config.update(config)
    
    # Initialize database
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        init_db()
    
    # Register routes
    from app.routes import register_routes
    register_routes(app)
    
    return app