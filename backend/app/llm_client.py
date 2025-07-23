import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from together import Together

load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY environment variable not set")

client = Together(api_key=TOGETHER_API_KEY)

SYSTEM_PROMPT = """
You are a GitHub Issue Assistant. Given an issue's title, body, and comments,
analyze it and return a JSON with the following fields:

- summary: a concise summary of the issue
- type: one of ["bug", "feature", "refactor", "documentation", "other"]
- priority_score: number between 1 (low) and 5 (critical)
- suggested_labels: array of relevant labels (strings) only have the standard github labels like [
  "bug",
  "feature",
  "enhancement",
  "refactor",
  "documentation",
  "test",
  "chore",
  "UI",
  "backend",
  "database",
  "API",
  "login-flow",
  "security",
  "performance",
  "good first issue",
  "help wanted",
  "in progress",
  "blocked",
  "ready for review",
  "wontfix",
  "duplicate",
  "question",
]

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

async def analyze_issue_with_llm(issue: dict):
    prompt = build_prompt(issue["title"], issue["body"], issue["comments"])

    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}, 
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        error_message = f"Together AI LLM error: {str(e)}"
        if hasattr(e, 'response') and e.response:
            error_message += f"\nResponse: {e.response.text}"
        raise Exception(error_message)
