from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.spam import check_spam

# FastAPI 기반 웹 앱 생성
app = FastAPI(title="SpamCheck Web")

# 정적 HTML 서빙: static 폴더 안의 파일들을 브라우저에서 읽을 수 있게 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

# 메인 페이지 (/) 접속 시 index.html을 보여줌
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

# /classify 주소로 데이터가 들어왔을 때 스팸 여부를 판별하여 돌려줌
@app.post("/classify")
async def classify(request: Request):
    payload = await request.json()
    text = payload["text"]
    
    label, score = check_spam(text)
    
    return {
        "label": label, "score": score
    }