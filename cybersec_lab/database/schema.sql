CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    total_points INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS challenges (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    difficulty TEXT NOT NULL,
    base_points INTEGER NOT NULL,
    description TEXT,
    vuln_code TEXT
);

CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    challenge_id TEXT NOT NULL,
    stage INTEGER NOT NULL,
    answer TEXT NOT NULL,
    ai_score REAL,
    ai_feedback TEXT,
    ai_hint TEXT,
    points_awarded INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (challenge_id) REFERENCES challenges (id)
);

CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    challenge_id TEXT NOT NULL,
    current_stage INTEGER DEFAULT 1,
    attempts INTEGER DEFAULT 0,
    hints_used INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (challenge_id) REFERENCES challenges (id),
    UNIQUE(user_id, challenge_id)
);

CREATE TABLE IF NOT EXISTS badges (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_badges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    badge_id TEXT NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (badge_id) REFERENCES badges (id),
    UNIQUE(user_id, badge_id)
);

-- Initial Badges
INSERT OR IGNORE INTO badges (id, name, description) VALUES
('first_blood', 'First Blood', 'Complete your first challenge'),
('sql_slayer', 'SQL Slayer', 'Complete all SQL Injection challenges'),
('no_hints', 'No Hints Needed', 'Complete a challenge without using any hints'),
('speed_hacker', 'Speed Hacker', 'Complete a challenge in record time'),
('perfectionist', 'Perfectionist', 'Get a 1.0 AI score on all stages of a challenge'),
('explorer', 'Explorer', 'Complete challenges in 3 different categories'),
('top_10', 'Top 10', 'Reach the top 10 on the leaderboard'),
('mentor', 'Mentor', 'Explain 5 vulnerabilities with high clarity'),
('elite_hacker', 'Elite Hacker', 'Complete all advanced challenges');
