from fastapi import FastAPI, HTTPException
from sqlmodel import select
from app.github_client import fetch_issue_and_comments
from app.llm_client import analyze_issue_with_llm, IssueRequest
from app.database import create_db_and_tables, get_session
from app.models import IssueAnalysis
import json
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from typing import List

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on startup
    create_db_and_tables()
    yield
    # on shutdown

app = FastAPI(lifespan=lifespan)

@app.post("/analyze-issue")
async def analyze_issue(req: IssueRequest):
    try:
        session = get_session()

        # Check if already exists
        statement = select(IssueAnalysis).where(
            IssueAnalysis.repo_url == req.repo_url,
            IssueAnalysis.issue_number == req.issue_number
        )
        existing = session.exec(statement).first()
        if existing:
            return json.loads(existing.full_json)

        # Fetch and analyze
        issue_data = await fetch_issue_and_comments(req.repo_url, req.issue_number)
        analysis = await analyze_issue_with_llm(issue_data)

        # Save to DB
        analysis_model = IssueAnalysis(
            repo_url=req.repo_url,
            issue_number=req.issue_number,
            summary=analysis.get("summary"),
            type=analysis.get("type"),
            priority_score=analysis.get("priority_score"),
            suggested_labels=",".join(analysis.get("suggested_labels", [])),
            potential_impact=analysis.get("potential_impact"),
            full_json=json.dumps(analysis, indent=2)
        )

        session.add(analysis_model)
        session.commit()

        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/history")
def get_history():
    try:
        session = get_session()
        statement = select(IssueAnalysis).order_by(IssueAnalysis.created_at.desc())
        results = session.exec(statement).all()

        history = []
        for row in results:
            history.append({
                "id": row.id,
                "repo_url": row.repo_url,
                "issue_number": row.issue_number,
                "summary": row.summary,
                "type": row.type,
                "priority_score": row.priority_score,
                "suggested_labels": row.suggested_labels.split(","),
                "potential_impact": row.potential_impact,
                "full_json": row.full_json,
                "created_at": row.created_at.isoformat()
            })

        return JSONResponse(content=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @app.get("/test-fetch/")
# async def test_fetch(repo_url: str, issue_number: int):
#     try:
#         data = await fetch_issue_and_comments(repo_url, issue_number)
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/analyze-issue")
# async def analyze_issue(req: IssueRequest):
#     print("inside openrouter\n")
#     headers = {
#         "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
#         "Content-Type": "application/json",
#         "HTTP-Referer": os.getenv("OPENROUTER_REFERER", ""),
#         "X-Title": os.getenv("OPENROUTER_TITLE", "Issue Assistant")
#     }

#     payload = {
#         "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
#         "messages": [
#             {
#                 "role": "user",
#                 "content": req
#             }
#         ]
#     }
#     try:
#         print("inside try\n")
#         response = requests.post("https://openrouter.ai/api/v1/chat/completions",
#                                  headers=headers,
#                                  data=json.dumps(payload))
#         response.raise_for_status()
#         return {
#             "response": response.json()["choices"][0]["message"]["content"]
#         }
#     except Exception as e:
#         print("inside except\n")
#         return {
#             "error": str(e),
#             "response_text": response.text if 'response' in locals() else "No response"
#         }


