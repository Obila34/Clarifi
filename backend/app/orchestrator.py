from datetime import datetime, timezone
import logging
from uuid import uuid4

from .knowledge_base import retrieve_relevant_docs
from .llm_adapter import synthesize_summary
from .models import (
    GapBridgeResponse,
    QueryResponse,
    ResourceCard,
    ResumeUploadResponse,
)
from .resume_processing import build_rewrites, compute_missing_skills, detect_skills, extract_text_from_upload
from .router import RoutingDecision
from .search_adapter import search_market_cards
from .session_store import InMemorySessionStore, ResumeSession


class ClarifiOrchestrator:
    def __init__(self, store: InMemorySessionStore) -> None:
        self.store = store
        self.logger = logging.getLogger("clarifi.orchestrator")

    async def handle_query(self, prompt: str, decision: RoutingDecision) -> QueryResponse:
        if decision.mode == "market_pulse":
            cards = await search_market_cards(prompt)
            summary = await synthesize_summary(
                prompt=prompt,
                context=(
                    f"Mode: market_pulse. Reason: {decision.reason}. "
                    "Sources are recent market pages and job trends."
                ),
            )
            return QueryResponse(
                mode="market_pulse",
                summary=summary,
                cards=cards,
            )

        if decision.mode == "resume_glowup":
            summary = await synthesize_summary(
                prompt=prompt,
                context=(
                    f"Mode: resume_glowup. Reason: {decision.reason}. "
                    "User should upload resume for ATS rewrite and gap analysis."
                ),
            )
            return QueryResponse(
                mode="resume_glowup",
                summary=summary,
                cards=[
                    ResourceCard(
                        title="Upload CV to generate bullet rewrites",
                        url="https://example.com/resume-upload-flow",
                        platform_icon="📄",
                        price="Free",
                    ),
                    ResourceCard(
                        title="ATS keyword alignment checklist",
                        url="https://example.com/ats-checklist",
                        platform_icon="🧠",
                        price="Free",
                    ),
                    ResourceCard(
                        title="Leadership tone and impact framing",
                        url="https://example.com/leadership-framing",
                        platform_icon="🚀",
                        price="Free",
                    ),
                ],
            )

        if decision.mode == "gap_bridge":
            summary = await synthesize_summary(
                prompt=prompt,
                context=(
                    f"Mode: gap_bridge. Reason: {decision.reason}. "
                    "Need uploaded resume context before targeted course recommendations."
                ),
            )
            return QueryResponse(
                mode="gap_bridge",
                summary=summary,
                cards=[
                    ResourceCard(
                        title="Skill-gap mapping method",
                        url="https://example.com/skill-gap-mapping",
                        platform_icon="🧩",
                        price="Free",
                    ),
                    ResourceCard(
                        title="Career transition planning framework",
                        url="https://example.com/transition-framework",
                        platform_icon="🛤️",
                        price="Free",
                    ),
                    ResourceCard(
                        title="90-day upskilling sprint template",
                        url="https://example.com/90-day-sprint",
                        platform_icon="📅",
                        price="Free",
                    ),
                ],
            )

        docs = retrieve_relevant_docs(prompt)
        cards = [
            ResourceCard(
                title=doc.title,
                url=f"https://example.com/{doc.title.lower().replace(' ', '-')}",
                platform_icon="🧭",
                price="Free",
            )
            for doc in docs
        ]

        summary_chunks = [doc.body for doc in docs]
        summary = await synthesize_summary(
            prompt=prompt,
            context=" ".join(summary_chunks),
        )

        return QueryResponse(mode="career_guide", summary=summary, cards=cards)

    def process_resume_upload(self, filename: str, file_bytes: bytes, dream_vibe: str) -> ResumeUploadResponse:
        extracted_text = extract_text_from_upload(filename=filename, file_bytes=file_bytes)
        skills = detect_skills(extracted_text)
        missing_skills = compute_missing_skills(existing_skills=skills, dream_vibe=dream_vibe)
        rewrites = build_rewrites(extracted_text)

        resume_id = str(uuid4())
        self.store.put(
            ResumeSession(
                resume_id=resume_id,
                text=extracted_text,
                skills=skills,
                dream_vibe=dream_vibe,
                created_at=datetime.now(timezone.utc),
            )
        )
        self.store.prune_old(hours=12)

        cards = [
            ResourceCard(
                title="ATS Rewrite Playbook",
                url="https://example.com/ats-rewrite-playbook",
                platform_icon="✍️",
                price="Free",
            ),
            ResourceCard(
                title="Hiring Manager Signal Checklist",
                url="https://example.com/hiring-manager-checklist",
                platform_icon="✅",
                price="Free",
            ),
            ResourceCard(
                title="Career Storyline Framework",
                url="https://example.com/career-storyline",
                platform_icon="🎤",
                price="Free",
            ),
        ]

        self.logger.info(
            "resume_processed resume_id=%s dream_vibe=%s skills=%s missing_skills=%s",
            resume_id,
            dream_vibe,
            skills,
            missing_skills,
        )

        return ResumeUploadResponse(
            resume_id=resume_id,
            summary=(
                "Resume parsed successfully. I found your strongest signals and generated rewrites "
                "designed to improve ATS matching and impact clarity."
            ),
            missing_skills=missing_skills,
            rewrites=rewrites,
            cards=cards,
        )

    async def build_gap_bridge(self, resume_id: str, dream_vibe: str) -> GapBridgeResponse:
        session = self.store.get(resume_id)
        if not session:
            raise ValueError("Resume session not found. Upload your CV first.")

        missing_skills = compute_missing_skills(existing_skills=session.skills, dream_vibe=dream_vibe)
        cards: list[ResourceCard] = []

        for skill in missing_skills[:3]:
            search_cards = await search_market_cards(f"best free course {skill}")
            if search_cards:
                cards.append(
                    ResourceCard(
                        title=f"Top learning path for {skill.title()}",
                        url=search_cards[0].url,
                        platform_icon="🎓",
                        price="Free",
                    )
                )

        if not cards:
            cards = [
                ResourceCard(
                    title="Learning path starter",
                    url="https://www.coursera.org/",
                    platform_icon="🎓",
                    price="Free",
                )
            ]

        self.logger.info(
            "gap_bridge_built resume_id=%s dream_vibe=%s missing_skills=%s card_count=%s",
            resume_id,
            dream_vibe,
            missing_skills,
            len(cards),
        )

        return GapBridgeResponse(
            summary=(
                "Gap Bridge complete. These learning resources target your highest-impact missing skills "
                "for the selected career vibe."
            ),
            missing_skills=missing_skills,
            cards=cards,
        )
