from fastapi import FastAPI, HTTPException
from app.github_client import fetch_issue_and_comments
import asyncio
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "GitHub Issue Assistant API is running"}


@app.get("/test-fetch/")
async def test_fetch(repo_url: str, issue_number: int):
    try:
        data = await fetch_issue_and_comments(repo_url, issue_number)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
