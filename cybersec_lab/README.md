# CyberSec Learning Lab — Ethical Hacking Practice Environment

This is a Master's-level educational platform designed to teach cybersecurity through Problem-Based Learning (PBL) and Scaffolded Instruction.

## Architecture
- **Frontend:** Streamlit
- **Database:** SQLite
- **AI Evaluator:** Anthropic Claude API (Claude 3 Haiku)
- **Authentication:** Streamlit Authenticator (with password hashing)

## Features
- **4-Stage Learning Model:** Find, Exploit, Patch, and Explain.
- **AI Evaluation:** Real-time feedback and hints from Claude API.
- **15 Challenges:** SQLi, XSS, IDOR, CSRF, SSRF, JWT, Command Injection, Path Traversal, Race Conditions.
- **Gamification:** Points, Leaderboard, and 9 different Badges.
- **Adaptive Learning:** Personalized challenge recommendations.
- **Learning Analytics:** Progress tracking and skill visualization.

## Setup Instructions

1. **Clone the repository.**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment Variables:**
   - Copy `.env.example` to `.env`.
   - Add your `ANTHROPIC_API_KEY`.
4. **Initialize Database and Load Challenges:**
   ```bash
   python cybersec_lab/challenges/challenge_loader.py
   ```
5. **Run the Application:**
   ```bash
   streamlit run cybersec_lab/app.py
   ```

## Suggested Improvements
- **Dockerization:** Containerize the app and its dependencies.
- **Real-time Sandboxing:** Use Docker to provide real, isolated environments for students to exploit and patch.
- **Social Features:** Add a forum or comments for peer-to-peer learning.
- **Multi-tenant Support:** Allow instructors to manage multiple classes and students.
