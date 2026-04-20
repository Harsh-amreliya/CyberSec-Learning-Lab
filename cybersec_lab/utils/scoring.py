from database.db import award_badge, get_user_badges, query_db, get_user_progress

def calculate_points(base_points, stage_idx, ai_score, hints_used, attempts, time_taken=0):
    """
    Base points: Beginner=100, Intermediate=200, Advanced=350
    Stage share: base_points / 4 (since 4 stages)
    Adjustments:
    - Hint penalty: -10 per hint
    - Attempt penalty: -5 per extra attempt (after 1st)
    - Speed bonus: +20 (if time_taken < 60s, for example)
    - Perfect bonus: +50 (if score == 1.0)
    """
    stage_base = base_points / 4

    # Only award points if score >= 0.7
    if ai_score < 0.7:
        return 0

    points = stage_base * ai_score
    points -= (hints_used * 10)
    points -= (max(0, attempts - 1) * 5)

    if ai_score == 1.0:
        points += 50

    if time_taken > 0 and time_taken < 60:
        points += 20

    return int(max(0, points))

def check_badges(user_id, challenge_id, stage_idx, ai_score, hints_used):
    new_badges = []

    # First Blood
    if award_badge(user_id, 'first_blood'):
        new_badges.append('First Blood')

    # No Hints Needed
    if hints_used == 0 and ai_score >= 0.7:
        if award_badge(user_id, 'no_hints'):
            new_badges.append('No Hints Needed')

    # SQL Slayer
    sql_challenges = query_db("SELECT id FROM challenges WHERE category = 'SQL Injection'")
    sql_ids = [c['id'] for c in sql_challenges]
    completed_sql = query_db(f"SELECT COUNT(*) as count FROM progress WHERE user_id = ? AND completed = 1 AND challenge_id IN ({','.join(['?']*len(sql_ids))})", (user_id, *sql_ids), one=True)
    if completed_sql['count'] == len(sql_ids):
        if award_badge(user_id, 'sql_slayer'):
            new_badges.append('SQL Slayer')

    # Explorer (3 different categories)
    categories = query_db("SELECT DISTINCT category FROM challenges JOIN progress ON challenges.id = progress.challenge_id WHERE progress.user_id = ? AND progress.completed = 1", (user_id,))
    if len(categories) >= 3:
        if award_badge(user_id, 'explorer'):
            new_badges.append('Explorer')

    # Perfectionist (1.0 on all stages of a challenge)
    # This check is more complex, might need a helper

    return new_badges

def get_recommendations(user_id):
    """
    Adaptive Learning: Suggest next challenge based on weak areas.
    Find categories with lowest completion rate or lowest average score.
    """
    stats = query_db("""
        SELECT c.category, AVG(s.ai_score) as avg_score, COUNT(DISTINCT c.id) as total_cat,
        (SELECT COUNT(*) FROM progress p JOIN challenges c2 ON p.challenge_id = c2.id WHERE p.user_id = ? AND p.completed = 1 AND c2.category = c.category) as completed_count
        FROM challenges c
        LEFT JOIN submissions s ON c.id = s.challenge_id AND s.user_id = ?
        GROUP BY c.category
    """, (user_id, user_id))

    if not stats:
        return query_db("SELECT * FROM challenges LIMIT 3")

    # Find category with lowest completion rate or avg_score < 0.8
    weak_categories = [s['category'] for s in stats if s['completed_count'] < s['total_cat']]

    if weak_categories:
        cat = weak_categories[0]
        return query_db("SELECT * FROM challenges WHERE category = ? AND id NOT IN (SELECT challenge_id FROM progress WHERE user_id = ? AND completed = 1) LIMIT 3", (cat, user_id))

    return query_db("SELECT * FROM challenges LIMIT 3")
