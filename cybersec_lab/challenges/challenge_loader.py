import json
import os
import sys

# Add the parent directory to sys.path so we can import from database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db import add_challenge, init_db

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def load_challenges():
    # Ensure DB is initialized
    init_db()

    count = 0
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(DATA_DIR, filename), 'r') as f:
                try:
                    data = json.load(f)
                    # We store the whole JSON or parts of it?
                    # The requirement says 'Load challenges from JSON files'.
                    # Let's store the metadata in DB and the full content can be loaded when needed,
                    # or we can store the whole JSON in a column.
                    # Given the schema, let's store the main fields.
                    add_challenge(
                        id=data['id'],
                        title=data['title'],
                        category=data['category'],
                        difficulty=data['difficulty'],
                        base_points=data['base_points'],
                        description=data['description'],
                        vuln_code=data['vuln_code']
                    )
                    count += 1
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    print(f"Loaded {count} challenges into the database.")

def get_challenge_details(challenge_id):
    filename = f"{challenge_id}.json"
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

if __name__ == "__main__":
    load_challenges()
