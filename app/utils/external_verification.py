"""
Verifies a student's external profile links.

GitHub is genuinely checked against GitHub's public API (a real, free,
unauthenticated call — no API key needed for this level of usage).
LeetCode has no simple free public API, so it's checked for a well-formed
URL only, exactly as the spec asks for a hackathon-appropriate version.
LinkedIn and portfolio links are self-reported — there's no reasonable way
to verify ownership of a LinkedIn profile or personal site without OAuth,
so they're honestly labeled "self_reported" rather than pretending to verify
something that isn't actually being checked.
"""

import re
from typing import Optional
from urllib.parse import urlparse

try:
    import requests
    HAS_REQUESTS = True
except Exception:
    HAS_REQUESTS = False

GITHUB_API_TIMEOUT = 5  # seconds — never let a slow external API hang a request


def _parse_github_username(url: str) -> Optional[str]:
    match = re.search(r"github\.com/([A-Za-z0-9\-]+)/?", url)
    return match.group(1) if match else None


def _parse_leetcode_username(url: str) -> Optional[str]:
    # Supports both leetcode.com/u/username/ and the older leetcode.com/username/
    match = re.search(r"leetcode\.com/(?:u/)?([A-Za-z0-9_\-]+)/?", url)
    return match.group(1) if match else None


def _is_well_formed_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


# ---------- a) GitHub ----------
def verify_github_profile(github_url: Optional[str]) -> dict:
    result = {"github_verified": False, "github_username": None, "github_public_repos": None}
    if not github_url:
        return result

    username = _parse_github_username(github_url)
    if not username:
        return result

    if not HAS_REQUESTS:
        print("[EXTERNAL_VERIFICATION] 'requests' library not available — cannot call GitHub API.")
        return result

    try:
        resp = requests.get(
            f"https://api.github.com/users/{username}",
            headers={"User-Agent": "placement-portal-verification"},  # GitHub API requires this or returns 403
            timeout=GITHUB_API_TIMEOUT,
        )
        if resp.status_code == 200:
            data = resp.json()
            result["github_verified"] = True
            result["github_username"] = username
            result["github_public_repos"] = data.get("public_repos")
        else:
            print(f"[EXTERNAL_VERIFICATION] GitHub API returned {resp.status_code} for '{username}' "
                  "— account may not exist, or GitHub is rate-limiting unauthenticated requests.")
    except Exception as e:
        print(f"[EXTERNAL_VERIFICATION] GitHub check failed: {e}")

    return result


# ---------- b) LeetCode ----------
def verify_leetcode_profile(leetcode_url: Optional[str]) -> dict:
    """
    LeetCode has no simple free public API for profile lookups, so — per the
    spec — this checks the URL is well-formed and marks it verified on that
    basis alone. This is a deliberately weaker guarantee than the GitHub
    check; say so plainly in your demo rather than implying it's the same
    level of verification.
    """
    result = {"leetcode_verified": False, "leetcode_username": None, "leetcode_rating": None}
    if not leetcode_url:
        return result

    if not _is_well_formed_url(leetcode_url) or "leetcode.com" not in leetcode_url.lower():
        return result

    username = _parse_leetcode_username(leetcode_url)
    if username:
        result["leetcode_verified"] = True
        result["leetcode_username"] = username
        # leetcode_rating intentionally left None — no reliable free API for this;
        # wire up a real fetch here later if a working method is found

    return result


# ---------- c) LinkedIn ----------
def verify_linkedin_profile(linkedin_url: Optional[str]) -> dict:
    result = {"linkedin_verified": "self_reported", "linkedin_url": None}
    if linkedin_url and _is_well_formed_url(linkedin_url):
        result["linkedin_url"] = linkedin_url
    return result


# ---------- d) Portfolio ----------
def verify_portfolio_url(portfolio_url: Optional[str]) -> dict:
    result = {"portfolio_verified": "self_reported", "portfolio_url": None}
    if portfolio_url and _is_well_formed_url(portfolio_url):
        result["portfolio_url"] = portfolio_url
    return result
