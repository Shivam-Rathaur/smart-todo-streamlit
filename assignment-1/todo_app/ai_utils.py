# ai_utils.py
import os
from google import genai

def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    return genai.Client(api_key=api_key)

def _safe_generate(client, prompt):
    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        return response.text
    except Exception:
        return (
            "Don't worry about getting it perfect.\n"
            "Just identify the immediate next step and do it to break the inertia."
        )

def rewrite_and_breakdown(task_text):
    client = get_client()
    if not client:
        return "Break this task into smaller steps and start with the simplest one."

    prompt = f"""
Rewrite the task below clearly and break it into 3–5 small actionable steps.

Task:
{task_text}
"""
    return _safe_generate(client, prompt)

def stuck_task_analysis(task_text):
    client = get_client()
    if not client:
        return (
            "This task might feel hard because it’s vague or mentally heavy. "
            "Try defining a clear first step."
        )

    prompt = f"""
Explain briefly why the following task might feel hard to start
and suggest one small action to begin.

Task:
{task_text}
"""
    return _safe_generate(client, prompt)
