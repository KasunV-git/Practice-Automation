# TaskMaster API

A simple REST API for managing tasks, built with Flask and SQLite. This project is designed for learning CI/CD automation and test-driven development.

## Features

- Create, Read, Update, Delete (CRUD) tasks
- Filter tasks by completion status
- SQLite database for persistence
- Comprehensive test coverage
- CI/CD pipeline with GitHub Actions

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd taskmaster
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Run the Application
```bash
python run.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

- `GET /health` - Health check
- `GET /tasks` - Get all tasks
- `GET /tasks/<id>` - Get specific task
- `POST /tasks` - Create new task
- `PUT /tasks/<id>` - Update task
- `DELETE /tasks/<id>` - Delete task

## Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_routes.py

# Run tests with specific marker
pytest -m unit
pytest -m integration
```

## Test Coverage

View coverage report after running tests:
```bash
open htmlcov/index.html  # Mac
start htmlcov/index.html  # Windows
```

## CI/CD Pipeline

The GitHub Actions workflow automatically:
- Runs tests on multiple Python versions
- Generates coverage reports
- Validates code on every push and pull request

## Project Structure

See the main documentation for detailed file structure explanation.