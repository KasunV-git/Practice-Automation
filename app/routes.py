from flask import request, jsonify
from app.database import db
from app.models import Task


def register_routes(app):
    """
    Register all API routes.
    
    Args:
        app: Flask application instance
    """
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({'status': 'healthy'}), 200
    
    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        """
        Get all tasks.
        Supports filtering by completed status.
        
        Query Parameters:
            completed: Filter by completion status (true/false)
        
        Returns:
            JSON list of tasks
        """
        completed = request.args.get('completed')
        
        if completed is not None:
            completed_bool = completed.lower() == 'true'
            tasks = Task.query.filter_by(completed=completed_bool).all()
        else:
            tasks = Task.query.all()
        
        return jsonify([task.to_dict() for task in tasks]), 200
    
    @app.route('/tasks/<int:task_id>', methods=['GET'])
    def get_task(task_id):
        """
        Get a specific task by ID.
        
        Args:
            task_id: Task identifier
        
        Returns:
            JSON task object or 404 error
        """
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(task.to_dict()), 200
    
    @app.route('/tasks', methods=['POST'])
    def create_task():
        """
        Create a new task.
        
        Request Body:
            title (required): Task title
            description (optional): Task description
            completed (optional): Completion status
        
        Returns:
            JSON task object with 201 status
        """
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            completed=data.get('completed', False)
        )
        
        db.session.add(task)
        db.session.commit()
        
        return jsonify(task.to_dict()), 201
    
    @app.route('/tasks/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        """
        Update an existing task.
        
        Args:
            task_id: Task identifier
        
        Request Body:
            title (optional): Updated title
            description (optional): Updated description
            completed (optional): Updated completion status
        
        Returns:
            JSON task object or 404 error
        """
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        data = request.get_json()
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']
        
        db.session.commit()
        
        return jsonify(task.to_dict()), 200
    
    @app.route('/tasks/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        """
        Delete a task.
        
        Args:
            task_id: Task identifier
        
        Returns:
            Success message or 404 error
        """
        task = Task.query.get(task_id)
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'}), 200