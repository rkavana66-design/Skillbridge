from pydantic import BaseModel


class RecommendationSchema(BaseModel):
    language: str
    percent: float
    level: str  # "low" | "average" | "strong"
    message: str
    suggested_actions: list[str]


class RecommendationsResponse(BaseModel):
    recommendations: list[RecommendationSchema]