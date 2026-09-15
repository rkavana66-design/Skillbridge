"""
Aggregates real recruiter search queries (see SearchLog, logged from
GET /api/recruiter/candidates) into a ranked "what skills are companies
actually searching for" list — the data behind the government/institution
feedback dashboard (Step 6).

Every number here comes directly from logged search text. Nothing is
invented: if no one has searched for "blockchain" yet, it simply won't
appear. This is intentionally simple word-frequency counting, not NLP —
good enough to show real signal in a demo, and fully explainable.
"""

import re
from collections import Counter
from sqlalchemy.orm import Session

from app.models.models import SearchLog
from app.schemas.insights import SkillDemandItem, SkillDemandResponse

# Common filler words to ignore so they don't dominate the "top skills" list.
STOPWORDS = {
    "a", "an", "the", "and", "or", "for", "with", "who", "know", "knows",
    "knowledge", "of", "in", "on", "find", "candidate", "candidates",
    "student", "students", "intern", "internship", "experience", "skilled",
    "good", "strong", "looking", "want", "need", "someone", "person",
    "is", "are", "to", "this", "that", "has", "have", "can", "do", "does",
}

WORD_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z0-9+.#]*")


def _extract_terms(text: str) -> list[str]:
    words = WORD_PATTERN.findall(text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def compute_skill_demand(db: Session, discipline: str | None = None, limit: int = 15) -> SkillDemandResponse:
    query = db.query(SearchLog).filter(SearchLog.query_text.isnot(None))
    if discipline:
        query = query.filter(SearchLog.discipline == discipline)

    logs = query.all()
    total_searches = len(logs)

    counter: Counter[str] = Counter()
    for log in logs:
        counter.update(_extract_terms(log.query_text or ""))

    top_skills = [
        SkillDemandItem(skill=term, search_count=count)
        for term, count in counter.most_common(limit)
    ]

    return SkillDemandResponse(total_searches=total_searches, top_skills=top_skills)