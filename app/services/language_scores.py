"""
Computes each student's "language/domain score" as a transparent composite
of up to three real signals:

  1. Verified test score  — best (max) percent across completed, non-
     disqualified test attempts for that language/domain. Weighted most
     heavily, since it's the only independently verified signal.
  2. Self-reported skill  — proficiency (0-100) from a matching entry in
     the student's own Skills list (case-insensitive name match).
  3. Project evidence     — how many of the student's real projects list
     this language/domain in their tech stack. Used as a small, capped
     signal (having built something with it is meaningful, but isn't the
     same as a graded assessment) — never the majority of the score.

Nothing here invents a number: every language that appears in the result
has at least one real signal behind it, and the response exposes exactly
which signals contributed (`sources`) plus their individual raw values,
so the UI can show its work rather than presenting an opaque percentage.

This is a new, standalone file — it doesn't modify or depend on your
existing assessment logic, tests, questions, proctoring, or tab-switch
detection. It only reads from test_attempts, tests, skills, and projects,
all already in your schema.
"""

import re
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.models import Test, TestAttempt, Skill, Project
from app.schemas.assessment import LanguageScoreSchema

# Weights used when ALL THREE signals are present for a language. When a
# signal is missing, its weight is redistributed proportionally across
# whichever signals ARE present, so the final number always reflects 100%
# of whatever real evidence exists — never padded with an assumed value.
TEST_WEIGHT = 0.65
SKILL_WEIGHT = 0.20
PROJECT_WEIGHT = 0.15

# Each project that uses a language contributes this many "project evidence"
# points, capped at 100 before weighting — i.e. 5+ real projects using a
# language maxes out this component. This is a proxy signal, not a grade.
POINTS_PER_PROJECT = 20

# When project evidence is the ONLY signal for a language (no test taken,
# no self-reported skill), the final percent is additionally capped here —
# unverified project usage alone shouldn't be able to claim the same
# confidence as a real test or even a self-rating.
PROJECT_ONLY_CAP = 75.0


def _normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def compute_language_scores(db: Session, student_id: UUID) -> list[LanguageScoreSchema]:
    """
    Returns one LanguageScoreSchema per distinct skill key seen across
    tests, self-reported skills, and project tech stacks — each with a
    composite `percent` and a `sources` list disclosing what fed into it.
    """
    skill_key = func.coalesce(Test.subcategory, Test.topic)

    test_rows = (
        db.query(
            skill_key.label("language"),
            func.max(TestAttempt.percent).label("percent"),
            func.count(TestAttempt.id).label("tests_taken"),
        )
        .join(Test, Test.id == TestAttempt.test_id)
        .filter(TestAttempt.student_id == student_id)
        .filter(TestAttempt.status == "completed")
        .filter(skill_key.isnot(None))
        .group_by(skill_key)
        .all()
    )

    self_reported_skills = db.query(Skill).filter(Skill.student_id == student_id).all()
    projects = db.query(Project).filter(Project.student_id == student_id).all()

    # Build a lookup from normalized language name -> display name, seeding
    # it from test data first since that's the canonical spelling/casing.
    display_name: dict[str, str] = {}
    test_percent: dict[str, float] = {}
    tests_taken: dict[str, int] = {}
    for row in test_rows:
        key = _normalize(row.language)
        display_name[key] = row.language
        test_percent[key] = round(float(row.percent), 1)
        tests_taken[key] = row.tests_taken

    skill_percent: dict[str, float] = {}
    for skill in self_reported_skills:
        key = _normalize(skill.name)
        display_name.setdefault(key, skill.name)
        # If a student has multiple skill entries with the same name,
        # keep the highest self-reported proficiency.
        skill_percent[key] = max(skill_percent.get(key, 0), float(skill.proficiency))

    project_count: dict[str, int] = {}
    for project in projects:
        if not project.tech_stack:
            continue
        for raw_tech in project.tech_stack.split(","):
            tech = raw_tech.strip()
            if not tech:
                continue
            key = _normalize(tech)
            display_name.setdefault(key, tech)
            project_count[key] = project_count.get(key, 0) + 1

    all_keys = set(display_name.keys())

    scores: list[LanguageScoreSchema] = []
    for key in all_keys:
        t = test_percent.get(key)
        s = skill_percent.get(key)
        p_count = project_count.get(key, 0)
        p = min(100.0, p_count * POINTS_PER_PROJECT) if p_count > 0 else None

        components = []
        sources = []
        if t is not None:
            components.append((t, TEST_WEIGHT))
            sources.append("test")
        if s is not None:
            components.append((s, SKILL_WEIGHT))
            sources.append("skill")
        if p is not None:
            components.append((p, PROJECT_WEIGHT))
            sources.append("projects")

        if not components:
            continue  # shouldn't happen, but guards against a stray key with no evidence

        total_weight = sum(w for _, w in components)
        final_percent = sum(v * w for v, w in components) / total_weight

        # Unverified project evidence alone can't claim near-mastery.
        if sources == ["projects"]:
            final_percent = min(final_percent, PROJECT_ONLY_CAP)

        final_percent = round(final_percent, 1)

        scores.append(
            LanguageScoreSchema(
                language=display_name[key],
                percent=final_percent,
                tests_taken=tests_taken.get(key, 0),
                test_percent=t,
                skill_percent=s,
                project_count=p_count,
                sources=sources,
            )
        )

    scores.sort(key=lambda s: s.language.lower())
    return scores


def top_language_scores(
    scores: list[LanguageScoreSchema], limit: int = 5
) -> list[LanguageScoreSchema]:
    """Highest-percent languages first, for a resume-style preview."""
    return sorted(scores, key=lambda s: s.percent, reverse=True)[:limit]