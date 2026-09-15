
"""
Lightweight proctoring logic — intentionally simple for a hackathon-grade
build. Tracks tab-switch events per attempt and auto-disqualifies past a
threshold. Camera snapshots are just stored as files (see
TestAttemptSnapshot); this module doesn't attempt real image analysis on
them, matching the "keep it simple, hackathon-ready" scope.
"""
 
from sqlalchemy.orm import Session
 
from app.models.models import TestAttempt, TestAttemptEvent
 
TAB_SWITCH_DISQUALIFY_THRESHOLD = 3
 
 
def record_event_and_check_disqualification(
    db: Session, attempt: TestAttempt, event_type: str, event_data: dict | None
) -> tuple[bool, int]:
    """
    Logs a proctoring event, and — for tab_switch events specifically —
    checks whether this attempt has now crossed the disqualification
    threshold. Returns (disqualified, tab_switch_count).
    """
    event = TestAttemptEvent(attempt_id=attempt.id, event_type=event_type, event_data=event_data)
    db.add(event)
    db.commit()
 
    tab_switch_count = (
        db.query(TestAttemptEvent)
        .filter(TestAttemptEvent.attempt_id == attempt.id)
        .filter(TestAttemptEvent.event_type == "tab_switch")
        .count()
    )
 
    disqualified = False
    if (
        event_type == "tab_switch"
        and tab_switch_count >= TAB_SWITCH_DISQUALIFY_THRESHOLD
        and attempt.status == "in_progress"
    ):
        attempt.status = "disqualified"
        attempt.disqualification_reason = (
            f"Exceeded tab-switch limit ({tab_switch_count}/{TAB_SWITCH_DISQUALIFY_THRESHOLD})."
        )
        db.commit()
        disqualified = True
 
    return disqualified, tab_switch_count
 
