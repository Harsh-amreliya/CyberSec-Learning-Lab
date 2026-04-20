import os
import json
import anthropic
from dotenv import load_dotenv
from .prompts import get_evaluation_prompt

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def evaluate_submission(challenge, stage_idx, student_answer):
    prompt = get_evaluation_prompt(challenge, stage_idx, student_answer)

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            temperature=0,
            system="You are a cybersecurity evaluator. Always respond in valid JSON format.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the text content from the response
        content = response.content[0].text
        # Try to parse the JSON
        result = json.loads(content)
        return result

    except Exception as e:
        print(f"AI Evaluation Error: {e}")
        # Fallback scoring logic
        return fallback_evaluation(challenge, stage_idx, student_answer)

def fallback_evaluation(challenge, stage_idx, student_answer):
    """
    A simple fallback mechanism if the API fails.
    Uses basic keyword matching against the target.
    """
    target = challenge['stages'][stage_idx]['target'].lower()
    student = student_answer.lower()

    # Very basic check: is the target in the student's answer or vice versa?
    if target in student or student in target:
        score = 0.8
        feedback = "The AI evaluator is currently unavailable, but your answer seems to match the key requirements (Fallback Mode)."
        hint = "Keep up the good work!"
    else:
        score = 0.3
        feedback = "The AI evaluator is currently unavailable, and your answer doesn't seem to contain the expected keywords (Fallback Mode)."
        hint = "Check your syntax or try to be more specific."

    return {
        "score": score,
        "feedback": feedback,
        "hint": hint
    }
