import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'cybersec_lab.db')
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), 'schema.sql')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def query_db(query, args=(), one=False):
    conn = get_connection()
    cur = conn.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
    conn = get_connection()
    cur = conn.execute(query, args)
    conn.commit()
    lastrowid = cur.lastrowid
    conn.close()
    return lastrowid

# User functions
def create_user(username, email, password_hash):
    return execute_db("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", (username, email, password_hash))

def get_user_by_username(username):
    return query_db("SELECT * FROM users WHERE username = ?", (username,), one=True)

# Challenge functions
def add_challenge(id, title, category, difficulty, base_points, description, vuln_code):
    execute_db("INSERT OR REPLACE INTO challenges (id, title, category, difficulty, base_points, description, vuln_code) VALUES (?, ?, ?, ?, ?, ?, ?)",
               (id, title, category, difficulty, base_points, description, vuln_code))

def get_all_challenges():
    return query_db("SELECT * FROM challenges")

def get_challenge_by_id(challenge_id):
    return query_db("SELECT * FROM challenges WHERE id = ?", (challenge_id,), one=True)

# Progress functions
def get_user_progress(user_id, challenge_id):
    return query_db("SELECT * FROM progress WHERE user_id = ? AND challenge_id = ?", (user_id, challenge_id), one=True)

def update_user_progress(user_id, challenge_id, stage, completed=False, hints_used=0):
    progress = get_user_progress(user_id, challenge_id)
    if progress:
        execute_db("UPDATE progress SET current_stage = ?, completed = ?, hints_used = hints_used + ?, last_updated = CURRENT_TIMESTAMP, attempts = attempts + 1 WHERE user_id = ? AND challenge_id = ?",
                   (stage, completed, hints_used, user_id, challenge_id))
    else:
        execute_db("INSERT INTO progress (user_id, challenge_id, current_stage, completed, hints_used, attempts) VALUES (?, ?, ?, ?, ?, 1)",
                   (user_id, challenge_id, stage, completed, hints_used))

# Submission functions
def add_submission(user_id, challenge_id, stage, answer, ai_score, ai_feedback, ai_hint, points_awarded):
    execute_db("INSERT INTO submissions (user_id, challenge_id, stage, answer, ai_score, ai_feedback, ai_hint, points_awarded) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               (user_id, challenge_id, stage, answer, ai_score, ai_feedback, ai_hint, points_awarded))
    if points_awarded > 0:
        execute_db("UPDATE users SET total_points = total_points + ? WHERE id = ?", (points_awarded, user_id))

# Badge functions
def award_badge(user_id, badge_id):
    try:
        execute_db("INSERT INTO user_badges (user_id, badge_id) VALUES (?, ?)", (user_id, badge_id))
        return True
    except sqlite3.IntegrityError:
        return False # Already has badge

def get_user_badges(user_id):
    return query_db("SELECT b.* FROM badges b JOIN user_badges ub ON b.id = ub.badge_id WHERE ub.user_id = ?", (user_id,))

def get_leaderboard():
    return query_db("""
        SELECT u.username, u.total_points,
        (SELECT COUNT(*) FROM progress p WHERE p.user_id = u.id AND p.completed = 1) as completed_count,
        (SELECT COUNT(*) FROM user_badges ub WHERE ub.user_id = u.id) as badge_count
        FROM users u
        ORDER BY u.total_points DESC
        LIMIT 10
    """)
