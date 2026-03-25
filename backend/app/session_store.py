from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class ResumeSession:
    resume_id: str
    text: str
    skills: list[str]
    dream_vibe: str
    created_at: datetime


class InMemorySessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, ResumeSession] = {}

    def put(self, session: ResumeSession) -> None:
        self._sessions[session.resume_id] = session

    def get(self, resume_id: str) -> ResumeSession | None:
        return self._sessions.get(resume_id)

    def prune_old(self, hours: int = 12) -> None:
        now = datetime.now(timezone.utc)
        expired = []
        for resume_id, session in self._sessions.items():
            age_hours = (now - session.created_at).total_seconds() / 3600
            if age_hours > hours:
                expired.append(resume_id)

        for resume_id in expired:
            self._sessions.pop(resume_id, None)
