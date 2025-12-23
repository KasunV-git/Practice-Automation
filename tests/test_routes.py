import pytest
import json


@pytest.mark.integration
class TestRoutes:
    """Integration tests for API routes."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        
        assert response.status_code == 200
        assert response.json == {'status': 'healthy'}
    
    def test_get_all_tasks_empty(self, client):
        """Test getting all tasks when database is empty."""
        response = client.get('/tasks')
        
        assert response.status_code == 200
        assert response.json == []
    
    def test_create_task(self, client):
        """Test creating a new task."""
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description'
        }
        
        response = client.post(
            '/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        assert response.json['title'] == 'Test Task'
        assert response.json['description'] == 'Test Description'
        assert response.json['completed'] is False
        assert 'id' in response.json
    
    def test_create_task_without_title(self, client):
        """Test creating a task without required title field."""
        task_data = {'description': 'No title'}
        
        response = client.post(
            '/tasks',
            data=json.dumps(task_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        assert 'error' in response.json
    
    def test_get_specific_task(self, client, sample_task):
        """Test getting a specific task by ID."""
        response = client.get(f'/tasks/{sample_task}')
        
        assert response.status_code == 200
        assert response.json['id'] == sample_task
        assert response.json['title'] == 'Sample Task'
    
    def test_get_nonexistent_task(self, client):
        """Test getting a task that doesn't exist."""
        response = client.get('/tasks/9999')
        
        assert response.status_code == 404
        assert 'error' in response.json
    
    def test_update_task(self, client, sample_task):
        """Test updating an existing task."""
        update_data = {
            'title': 'Updated Task',
            'completed': True
        }
        
        response = client.put(
            f'/tasks/{sample_task}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        assert response.json['title'] == 'Updated Task'
        assert response.json['completed'] is True
    
    def test_update_nonexistent_task(self, client):
        """Test updating a task that doesn't exist."""
        update_data = {'title': 'Updated'}
        
        response = client.put(
            '/tasks/9999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_delete_task(self, client, sample_task):
        """Test deleting a task."""
        response = client.delete(f'/tasks/{sample_task}')
        
        assert response.status_code == 200
        assert 'message' in response.json
        
        # Verify task is deleted
        get_response = client.get(f'/tasks/{sample_task}')
        assert get_response.status_code == 404
    
    def test_delete_nonexistent_task(self, client):
        """Test deleting a task that doesn't exist."""
        response = client.delete('/tasks/9999')
        
        assert response.status_code == 404
    
    def test_filter_tasks_by_completion(self, client):
        """Test filtering tasks by completion status."""
        # Create completed and incomplete tasks
        client.post('/tasks', json={'title': 'Complete', 'completed': True})
        client.post('/tasks', json={'title': 'Incomplete', 'completed': False})
        
        # Filter for completed tasks
        response = client.get('/tasks?completed=true')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['completed'] is True
        
        # Filter for incomplete tasks
        response = client.get('/tasks?completed=false')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['completed'] is False