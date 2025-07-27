import httpx
from urllib.parse import urlparse
from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_API_BASE = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json"
}

def extract_owner_repo(repo_url: str):
    parsed = urlparse(repo_url)
    path_parts = parsed.path.strip("/").split("/")
    if len(path_parts) < 2:
        raise ValueError("Invalid GitHub repo URL")
    return path_parts[0], path_parts[1]  # owner, repo


async def fetch_issue_and_comments(repo_url: str, issue_number: int):
    owner, repo = extract_owner_repo(repo_url)

    issue_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues/{issue_number}"
    comments_url = f"{issue_url}/comments"

    async with httpx.AsyncClient() as client:
        issue_response = await client.get(issue_url, headers=HEADERS)
        comments_response = await client.get(comments_url, headers=HEADERS)

    if issue_response.status_code == 404:
        raise Exception("Issue not found. It might be disabled or private.")
    if issue_response.status_code == 403:
        raise Exception("Access denied or rate limited. Try again later.")
    if issue_response.status_code == 500:
        raise Exception("GitHub server error. Try again later.")

    issue_data = issue_response.json()
    comments_data = comments_response.json()

    return {
        "title": issue_data.get("title", ""),
        "body": issue_data.get("body", ""),
        "comments": [comment.get("body", "") for comment in comments_data]
    }
