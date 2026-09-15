"""
Generates concrete, explainable improvement suggestions per language/domain,
based on the student's real composite scores (see language_scores.py).

This is a deterministic, rule-based engine — not a live call to an external
AI API. That's a deliberate choice: an external API adds a network
dependency and a failure point that could visibly break live during a
demo, for a feature that doesn't need it. Every suggestion here is derived
directly from real data already in the system (test scores, self-reported
skills, project evidence), so it's fast, always available offline, and
easy to explain if asked "how does this work?"

Thresholds:
  < 40%      -> "low"     — clear gaps, concrete next steps
  40-69%     -> "average" — solid start, specific ways to strengthen it
  >= 70%     -> "strong"  — positive reinforcement, optional stretch goals
"""

from app.schemas.assessment import LanguageScoreSchema
from app.schemas.recommendation import RecommendationSchema

LOW_THRESHOLD = 40
STRONG_THRESHOLD = 70

# A few well-known free/well-reviewed resources per language — used as a
# starting suggestion, not an exhaustive catalog. Falls back to a generic
# suggestion for any language not listed here.
COURSE_SUGGESTIONS: dict[str, str] = {
    "python": "Try a beginner-to-intermediate Python course on freeCodeCamp or CS50P (Harvard, free).",
    "java": "Try a Java fundamentals course on freeCodeCamp or the official Oracle Java tutorials.",
    "c++": "Try a C++ fundamentals course on freeCodeCamp or LearnCpp.com.",
    "dsa": "Practice on LeetCode or GeeksforGeeks, starting with arrays, strings, and basic recursion.",
    "accounting": "Try an introductory accounting course on Coursera or Khan Academy's finance section.",
    "anatomy": "Review core systems (cardiovascular, respiratory, skeletal) using Kenhub or Khan Academy.",
    "physiology": "Revisit core organ-system physiology using Khan Academy or Ninja Nerd (YouTube).",
    "biochemistry": "Review core metabolic pathways using Khan Academy's biochemistry unit.",
    "pharmacology": "Review drug classes and mechanisms using a pharmacology basics course on Coursera.",
    "pathology": "Review disease mechanisms using Khan Academy's pathology-adjacent health & medicine unit.",
    "microbiology": "Review core microbiology using Khan Academy or a beginner course on Coursera.",
}


def _course_suggestion(language: str) -> str:
    return COURSE_SUGGESTIONS.get(
        language.lower(),
        f"Look for a well-reviewed beginner/intermediate {language} course on freeCodeCamp, "
        f"Coursera, or YouTube.",
    )


def generate_recommendations(scores: list[LanguageScoreSchema]) -> list[RecommendationSchema]:
    recommendations: list[RecommendationSchema] = []

    for score in scores:
        sources = score.sources or []
        actions: list[str] = []

        if score.percent < LOW_THRESHOLD:
            level = "low"
            message = f"Your {score.language} score is low right now — here's where to start."
        elif score.percent < STRONG_THRESHOLD:
            level = "average"
            message = f"You have a solid start in {score.language} — a bit more work will push this up."
        else:
            level = "strong"
            message = f"Great work in {score.language} — this is one of your strongest areas."

        if level in ("low", "average"):
            if "test" not in sources:
                actions.append(f"Take the {score.language} assessment test to get a verified score.")
            elif score.test_percent is not None and score.test_percent < STRONG_THRESHOLD:
                actions.append(f"Retake the {score.language} test after brushing up — your best score counts.")

            if "projects" not in sources:
                actions.append(f"Build a small real project using {score.language} to strengthen this score.")

            actions.append(_course_suggestion(score.language))
        else:
            actions.append(f"Consider a project or two that pushes {score.language} further, or mentor others.")

        recommendations.append(
            RecommendationSchema(
                language=score.language,
                percent=score.percent,
                level=level,
                message=message,
                suggested_actions=actions,
            )
        )

    # Weakest areas first — that's what the student most needs to see.
    recommendations.sort(key=lambda r: r.percent)
    return recommendations