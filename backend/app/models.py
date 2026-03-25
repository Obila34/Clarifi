from typing import Literal

from pydantic import BaseModel, Field


ClarifiMode = Literal["career_guide", "market_pulse", "resume_glowup", "gap_bridge"]


class ResourceCard(BaseModel):
    title: str
    url: str
    platform_icon: str
    price: str


class QueryRequest(BaseModel):
    prompt: str = Field(min_length=2, max_length=600)


class QueryResponse(BaseModel):
    mode: ClarifiMode
    summary: str
    cards: list[ResourceCard]


class GapBridgeRequest(BaseModel):
    resume_id: str
    dream_vibe: str = Field(min_length=2, max_length=120)


class GapBridgeResponse(BaseModel):
    mode: Literal["gap_bridge"] = "gap_bridge"
    summary: str
    missing_skills: list[str]
    cards: list[ResourceCard]


class ResumeRewrite(BaseModel):
    original: str
    improved: str


class ResumeUploadResponse(BaseModel):
    mode: Literal["resume_glowup"] = "resume_glowup"
    resume_id: str
    summary: str
    missing_skills: list[str]
    rewrites: list[ResumeRewrite]
    cards: list[ResourceCard]
