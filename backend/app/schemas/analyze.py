from pydantic import BaseModel, HttpUrl, field_validator

class AnalyzeRequest(BaseModel):
    url: HttpUrl

    @field_validator("url")
    @classmethod
    def block_private_urls(cls, v):
        host = v.host
        blocked = ["localhost", "127.0.0.1", "0.0.0.0", "::1"]
        if host in blocked:
            raise ValueError("Private URLs are not allowed")
        if host.startswith("192.168.") or host.startswith("10.") or host.startswith("172."):
            raise ValueError("Private URLs are not allowed")
        return v

class WordWeightSchema(BaseModel):
    word: str
    weight: float

class AnalyzeResponse(BaseModel):
    words: list[WordWeightSchema]