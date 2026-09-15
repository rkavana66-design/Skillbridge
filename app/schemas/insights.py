from pydantic import BaseModel


class SkillDemandItem(BaseModel):
    skill: str
    search_count: int


class SkillDemandResponse(BaseModel):
    total_searches: int
    top_skills: list[SkillDemandItem]