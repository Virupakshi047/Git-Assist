from fastapi import FastAPI, HTTPException
from app.github_client import fetch_issue_and_comments
from app.llm_client import analyze_issue_with_llm
from app.llm_client import IssueRequest

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "GitHub Issue Assistant API is running"}


@app.post("/analyze-issue")
async def analyze_issue(req: IssueRequest):
    try:
        issue_data = await fetch_issue_and_comments(req.repo_url, req.issue_number)
        result = await analyze_issue_with_llm(issue_data)
        return result
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


