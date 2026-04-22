from pydantic import BaseModel, HttpUrl

class AnalyzeRequest(BaseModel):
    url: HttpUrl

class WordWeightSchema(BaseModel):
    word: str
    weight: float

class AnalyzeResponse(BaseModel):
    words: list[WordWeightSchema]