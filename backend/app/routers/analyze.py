from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.analyze import AnalyzedArticle, WordWeight
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse, WordWeightSchema
from app.services.scraper import fetch_article_text
from app.services.nlp import extract_topics
from app.db.session import get_db
from app.dependencies.auth import verify_token

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest, db: AsyncSession = Depends(get_db), payload: dict = Depends(verify_token)):
    try:
        text = fetch_article_text(str(request.url))
        if not text:
            raise HTTPException(status_code=422, detail="Could not extract text from the provided URL")
        
        records = extract_topics(text)

        article = AnalyzedArticle(
            user_id = payload["sub"],
            url = str(request.url)
        )
        db.add(article)
        await db.commit(article)
        await db.refresh(article)

        word_weights = [WordWeight(article_id = article.id, word=records["word"], weight=records["weight"])]
        db.add_all(word_weights)
        await db.commit()

        return AnalyzeResponse(words=[WordWeightSchema(**w) for w in records])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")