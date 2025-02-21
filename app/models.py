from pydantic import BaseModel

class WebsiteRequest(BaseModel):
    url: str
    expected_description: str

class WebsiteResponse(BaseModel):
    url: str
    title: str
    match_score: int
    analysis: str 