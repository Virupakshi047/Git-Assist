import os
import json
import requests
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

SYSTEM_PROMPT = """
You are a GitHub Issue Assistant. Given an issue's title, body, and comments,
analyze it and return a JSON with the following fields:

- summary: a concise summary of the issue
- type: one of ["bug", "feature", "refactor", "documentation", "other"]
- priority_score: number between 1 (low) and 5 (critical)
- suggested_labels: array of relevant labels (strings)
- potential_impact: brief description of what this issue could affect

Respond ONLY with a valid JSON object, nothing else.
"""

class IssueRequest(BaseModel):
    repo_url: str
    issue_number: int

def build_prompt(title, body, comments):
    comment_str = "\n".join([f"- {c}" for c in comments]) if comments else "No comments"
    return f"""
    Title: {title}
    Body: {body}
    Comments:
    {comment_str}
    """

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

PAYLOAD = {
    "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
    "messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": ""}
    ]
}

async def analyze_issue_with_llm(issue: dict):
    prompt = build_prompt(issue["title"], issue["body"], issue["comments"])

    payload = PAYLOAD
    payload["messages"][1]["content"] = prompt

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=HEADERS,
                                 data=json.dumps(payload))
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return json.loads(content)  # assumes model returns valid JSON
    except Exception as e:
        raise Exception(f"OpenRouter LLM error: {str(e)}\nResponse: {response.text if 'response' in locals() else 'No response'}")
