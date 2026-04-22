from fastapi import APIRouter, HTTPException
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse, WordWeight
from app.services.scraper import fetch_article_text
from app.services.nlp import extract_topics

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    try:
        text = fetch_article_text(str(request.url))
        if not text:
            raise HTTPException(status_code=422, detail="Could not extract text from the provided URL")
        
        words = extract_topics(text)
        return AnalyzeResponse(words=[WordWeight(**w) for w in words])
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze article: {str(e)}")