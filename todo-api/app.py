# Import the Flask class and helper functions from the flask library
from flask import Flask, request, jsonify

# Create an instance of the Flask app — this is the core of your API
app = Flask(__name__)

# A list to store our todos in memory (resets when the server restarts)
todos = []

# A counter to give each todo a unique ID
next_id = 1


# Define a route for GET /todos — this returns all todos
@app.route("/todos", methods=["GET"])
def get_todos():
    # Return the full list of todos as JSON with a 200 OK status
    return jsonify(todos), 200


# Define a route for GET /todos/<id> — this returns a single todo by its ID
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    # Loop through all todos to find the one with the matching ID
    for todo in todos:
        if todo["id"] == todo_id:
            # Found it — return it as JSON
            return jsonify(todo), 200
    # If no todo matched, return a 404 Not Found error
    return jsonify({"error": "Todo not found"}), 404


# Define a route for POST /todos — this creates a new todo
@app.route("/todos", methods=["POST"])
def create_todo():
    # We need access to the global next_id variable so we can update it
    global next_id

    # Get the JSON data sent in the request body
    data = request.get_json()

    # Check that the request includes a "title" field
    if not data or "title" not in data:
        # If not, return a 400 Bad Request error
        return jsonify({"error": "Title is required"}), 400

    # Build a new todo dictionary with an ID, title, and done status
    todo = {
        "id": next_id,                       # Assign the current ID counter
        "title": data["title"],              # Use the title from the request
        "done": data.get("done", False),     # Default "done" to False if not provided
    }

    # Increment the ID counter so the next todo gets a unique ID
    next_id += 1

    # Add the new todo to our list
    todos.append(todo)

    # Return the created todo as JSON with a 201 Created status
    return jsonify(todo), 201


# Define a route for PUT /todos/<id> — this updates an existing todo
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    # Get the JSON data sent in the request body
    data = request.get_json()

    # Loop through all todos to find the one with the matching ID
    for todo in todos:
        if todo["id"] == todo_id:
            # Update the title if provided, otherwise keep the current title
            todo["title"] = data.get("title", todo["title"])
            # Update the done status if provided, otherwise keep the current value
            todo["done"] = data.get("done", todo["done"])
            # Return the updated todo as JSON
            return jsonify(todo), 200

    # If no todo matched, return a 404 Not Found error
    return jsonify({"error": "Todo not found"}), 404


# Define a route for DELETE /todos/<id> — this deletes a todo
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    # Loop through all todos to find the one with the matching ID
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            # Remove the todo from the list using its index
            todos.pop(i)
            # Return a success message
            return jsonify({"message": "Todo deleted"}), 200

    # If no todo matched, return a 404 Not Found error
    return jsonify({"error": "Todo not found"}), 404


# This block runs only when you execute this file directly (not when imported)
if __name__ == "__main__":
    # Start the Flask development server on port 5000 with debug mode on
    # debug=True auto-reloads the server when you change the code
    app.run(debug=True, port=5000)
