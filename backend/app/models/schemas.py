from pydantic import BaseModel, HttpUrl

class AnalyzeRequest(BaseModel):
    url: HttpUrl

class WordWeight(BaseModel):
    word: str
    weight: float

class AnalyzeResponse(BaseModel):
    words: list[WordWeight]