from dataclasses import dataclass

from .models import ClarifiMode


@dataclass(frozen=True)
class RoutingDecision:
    mode: ClarifiMode
    reason: str


MARKET_KEYWORDS = {
    "salary",
    "market",
    "trend",
    "latest",
    "demand",
    "hiring",
    "job board",
    "new role",
    "news",
}
RESUME_KEYWORDS = {"resume", "cv", "ats", "rewrite", "bullet", "experience"}
GAP_KEYWORDS = {"course", "skill gap", "missing skill", "learn", "certification", "upskill"}


def route_mode(prompt: str) -> RoutingDecision:
    normalized = prompt.lower()

    if any(keyword in normalized for keyword in RESUME_KEYWORDS):
        return RoutingDecision(mode="resume_glowup", reason="Resume optimization intent detected")

    if any(keyword in normalized for keyword in GAP_KEYWORDS):
        return RoutingDecision(mode="gap_bridge", reason="Learning-path intent detected")

    if any(keyword in normalized for keyword in MARKET_KEYWORDS):
        return RoutingDecision(mode="market_pulse", reason="Time-sensitive market signal requested")

    return RoutingDecision(mode="career_guide", reason="Default evergreen career guidance path")
