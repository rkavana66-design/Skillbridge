from fastapi import APIRouter, Depends

from app.api.deps import get_current_user, require_role
from app.models.models import User, UserRole

router = APIRouter(prefix="/api", tags=["examples"])


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    """Any logged-in user, regardless of role."""
    return {"id": str(current_user.id), "email": current_user.email, "role": current_user.role.value}


@router.get("/recruiter-only")
def recruiter_only_route(current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin))):
    """Only recruiters and admins can reach this — e.g. the candidate search endpoint later."""
    return {"message": f"Welcome, recruiter {current_user.email}"}


@router.get("/admin-only")
def admin_only_route(current_user: User = Depends(require_role(UserRole.admin))):
    """Only admins — e.g. the Ministry analytics dashboard endpoint later."""
    return {"message": f"Welcome, admin {current_user.email}"}
