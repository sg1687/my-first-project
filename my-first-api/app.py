from flask import Flask, jsonify, request

# Create the Flask app
app = Flask(__name__)

# Our "database" (just a list for now)
tasks = []
task_id = 1

# Root endpoint - test if API is running
@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to your first API!",
        "endpoints": {
            "GET /tasks": "Get all tasks",
            "POST /tasks": "Create a task",
            "GET /tasks/<id>": "Get specific task",
            "DELETE /tasks/<id>": "Delete a task"
        }
    })

# GET all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({
        "tasks": tasks,
        "count": len(tasks)
    })

# CREATE a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id
    
    # Get data from request
    data = request.get_json()
    
    # Create new task
    new_task = {
        "id": task_id,
        "title": data.get("title"),
        "description": data.get("description", ""),
        "completed": False
    }
    
    tasks.append(new_task)
    task_id += 1
    
    return jsonify({
        "message": "Task created!",
        "task": new_task
    }), 201

# GET a specific task
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    # Find task by id
    task = next((t for t in tasks if t['id'] == id), None)
    
    if task:
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404

# DELETE a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    global tasks
    
    # Find and remove task
    task = next((t for t in tasks if t['id'] == id), None)
    
    if task:
        tasks = [t for t in tasks if t['id'] != id]
        return jsonify({
            "message": "Task deleted!",
            "task": task
        })
    else:
        return jsonify({"error": "Task not found"}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=8000)