from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.assessment import LanguageScoreSchema


# ---------- Candidate search ----------
class CandidateSummary(BaseModel):
    id: UUID
    name: str
    discipline: Optional[str] = None
    top_skills: list[LanguageScoreSchema] = []
    verified_documents_count: int = 0


# ---------- Interview booking ----------
class InterviewCreate(BaseModel):
    student_id: UUID
    scheduled_at: datetime
    duration_minutes: int = Field(default=30, gt=0, le=240)
    mode: str = "online"  # "online" | "offline"
    location_or_link: Optional[str] = None
    notes: Optional[str] = None


class InterviewResponse(BaseModel):
    id: UUID
    student_id: UUID
    student_name: str
    scheduled_at: datetime
    duration_minutes: int
    mode: str
    location_or_link: Optional[str] = None
    notes: Optional[str] = None
    status: str

    class Config:
        from_attributes = True