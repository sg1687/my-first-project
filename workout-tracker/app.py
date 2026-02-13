# Import the Flask class and helper functions from the flask library
from flask import Flask, request, jsonify, send_from_directory

# Import CORS to allow the frontend (HTML file) to talk to the API
from flask_cors import CORS

# Import date from datetime to auto-set the workout date
from datetime import date

# Import random to pick a random motivational image
import random

# Create an instance of the Flask app — this is the core of your API
app = Flask(__name__)

# Enable CORS so the browser doesn't block requests from the frontend
CORS(app)

# A list of motivational fitness image URLs (from Unsplash)
motivational_images = [
    {
        "url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800",
        "quote": "The only bad workout is the one that didn't happen.",
    },
    {
        "url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=800",
        "quote": "Push yourself, because no one else is going to do it for you.",
    },
    {
        "url": "https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=800",
        "quote": "Strength does not come from the body. It comes from the will.",
    },
    {
        "url": "https://images.unsplash.com/photo-1549060279-7e168fcee0c2?w=800",
        "quote": "Your body can stand almost anything. It's your mind you have to convince.",
    },
    {
        "url": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=800",
        "quote": "The pain you feel today will be the strength you feel tomorrow.",
    },
    {
        "url": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800",
        "quote": "Don't stop when you're tired. Stop when you're done.",
    },
]

# A list to store our workouts in memory (resets when the server restarts)
workouts = []

# A counter to give each workout a unique ID
next_id = 1


# Define a route for the landing page — serves index.html
@app.route("/")
def serve_landing():
    # Send the index.html file from the same directory as this script
    return send_from_directory(".", "index.html")


# Define a route for the workouts page — serves workouts.html
@app.route("/log")
def serve_workouts():
    # Send the workouts.html file from the same directory as this script
    return send_from_directory(".", "workouts.html")


# Define a route for GET /workouts — this returns all workouts
@app.route("/workouts", methods=["GET"])
def get_workouts():
    # Return the full list of workouts as JSON with a 200 OK status
    return jsonify(workouts), 200


# Define a route for GET /workouts/<id> — this returns a single workout by its ID
@app.route("/workouts/<int:workout_id>", methods=["GET"])
def get_workout(workout_id):
    # Loop through all workouts to find the one with the matching ID
    for workout in workouts:
        if workout["id"] == workout_id:
            # Found it — return it as JSON
            return jsonify(workout), 200
    # If no workout matched, return a 404 Not Found error
    return jsonify({"error": "Workout not found"}), 404


# Define a route for POST /workouts — this logs a new workout
@app.route("/workouts", methods=["POST"])
def create_workout():
    # We need access to the global next_id variable so we can update it
    global next_id

    # Get the JSON data sent in the request body
    data = request.get_json()

    # Check that the request includes an "exercise" field
    if not data or "exercise" not in data:
        # If not, return a 400 Bad Request error
        return jsonify({"error": "Exercise name is required"}), 400

    # Build a new workout dictionary with all the fields
    workout = {
        "id": next_id,                              # Assign the current ID counter
        "exercise": data["exercise"],                # Use the exercise name from the request
        "sets": data.get("sets", 0),                 # Number of sets, default to 0
        "reps": data.get("reps", 0),                 # Number of reps, default to 0
        "weight": data.get("weight", 0),             # Weight used, default to 0
        "duration": data.get("duration", 0),         # Duration in minutes, default to 0
        "notes": data.get("notes", ""),              # Optional notes, default to empty string
        "date": date.today().isoformat(),            # Auto-set to today's date (YYYY-MM-DD)
    }

    # Increment the ID counter so the next workout gets a unique ID
    next_id += 1

    # Add the new workout to our list
    workouts.append(workout)

    # Return the created workout as JSON with a 201 Created status
    return jsonify(workout), 201


# Define a route for PUT /workouts/<id> — this updates an existing workout
@app.route("/workouts/<int:workout_id>", methods=["PUT"])
def update_workout(workout_id):
    # Get the JSON data sent in the request body
    data = request.get_json()

    # Loop through all workouts to find the one with the matching ID
    for workout in workouts:
        if workout["id"] == workout_id:
            # Update each field if provided, otherwise keep the current value
            workout["exercise"] = data.get("exercise", workout["exercise"])
            workout["sets"] = data.get("sets", workout["sets"])
            workout["reps"] = data.get("reps", workout["reps"])
            workout["weight"] = data.get("weight", workout["weight"])
            workout["duration"] = data.get("duration", workout["duration"])
            workout["notes"] = data.get("notes", workout["notes"])
            # Return the updated workout as JSON
            return jsonify(workout), 200

    # If no workout matched, return a 404 Not Found error
    return jsonify({"error": "Workout not found"}), 404


# Define a route for DELETE /workouts/<id> — this deletes a workout
@app.route("/workouts/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    # Loop through all workouts to find the one with the matching ID
    for i, workout in enumerate(workouts):
        if workout["id"] == workout_id:
            # Remove the workout from the list using its index
            workouts.pop(i)
            # Return a success message
            return jsonify({"message": "Workout deleted"}), 200

    # If no workout matched, return a 404 Not Found error
    return jsonify({"error": "Workout not found"}), 404


# Define a route for GET /motivation — this returns a random motivational image and quote
@app.route("/motivation", methods=["GET"])
def get_motivation():
    # Pick a random image/quote pair from the list
    pick = random.choice(motivational_images)
    # Return the image URL and quote as JSON
    return jsonify(pick), 200


# This block runs only when you execute this file directly (not when imported)
if __name__ == "__main__":
    # Start the Flask development server on port 5001 with debug mode on
    # Using port 5001 to avoid conflict with the Todo API on port 5000
    # host="0.0.0.0" makes the server accessible from other devices on the network
    app.run(debug=True, port=5001, host="0.0.0.0")
