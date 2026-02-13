"""
Job Scraper Web App
A Flask app that scrapes job listings and displays them in a web interface.
Run with: python3 app.py
Then open: http://localhost:5002
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from scraper import scrape_jobs, scrape_hackernews  # Import both scrapers

# Create the Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Serve the frontend HTML page
@app.route("/")
def home():
    return send_file("index.html")

# API endpoint that returns scraped jobs as JSON
@app.route("/api/jobs")
def get_jobs():
    # Get the optional search query from the URL: /api/jobs?q=python
    search_term = request.args.get("q", None)

    # Run the scraper
    jobs = scrape_jobs(search_term=search_term)

    # Return the results as JSON
    return jsonify({
        "count": len(jobs),
        "search": search_term,
        "jobs": jobs,
    })


# API endpoint that returns Hacker News stories as JSON
@app.route("/api/hackernews")
def get_hackernews():
    # Get the optional search query and sort: /api/hackernews?q=python&sort=newest
    search_term = request.args.get("q", None)
    sort_by = request.args.get("sort", "default")

    # Run the HN scraper with sort option
    stories = scrape_hackernews(search_term=search_term, sort_by=sort_by)

    # Return the results as JSON
    return jsonify({
        "count": len(stories),
        "search": search_term,
        "stories": stories,
    })


if __name__ == "__main__":
    print("Job Scraper running at http://localhost:5002")
    app.run(port=5002, debug=True)
