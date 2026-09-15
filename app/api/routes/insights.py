from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.insights import SkillDemandResponse
from app.services.skill_demand import compute_skill_demand

router = APIRouter(prefix="/api/insights", tags=["insights"])


# Intentionally public (no auth) for this demo — this is meant to represent
# a government/institutional dashboard, not a recruiter or student account.
# For a production deployment, gate this behind an admin/government role
# the same way require_role() protects student/recruiter routes elsewhere.
@router.get("/skill-demand", response_model=SkillDemandResponse)
def get_skill_demand(
    discipline: str | None = None,
    db: Session = Depends(get_db),
):
    return compute_skill_demand(db, discipline=discipline)