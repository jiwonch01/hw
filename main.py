from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from services.tone_analyzer import get_dominant_colors

app = FastAPI(title="OOTD Color & Tone Analyzer")

# 템플릿 설정 (경로를 templates로 지정)
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    메인 페이지를 렌더링하여 반환합니다.
    """
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    업로드된 이미지를 받아 주요 색상(Top 3)과 퍼스널 컬러 톤을 분석해 반환합니다.
    """
    try:
        contents = await file.read()
        # AI 분석 서비스 호출
        result = get_dominant_colors(contents)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
