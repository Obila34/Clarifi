from io import BytesIO
from pathlib import Path

from docx import Document
from pypdf import PdfReader

from .models import ResumeRewrite

SKILL_BANK = {
    "python",
    "fastapi",
    "sql",
    "docker",
    "kubernetes",
    "machine learning",
    "data analysis",
    "communication",
    "leadership",
    "product thinking",
    "system design",
    "cloud",
}


def extract_text_from_upload(filename: str, file_bytes: bytes) -> str:
    extension = Path(filename).suffix.lower()

    if extension == ".pdf":
        return _extract_pdf(file_bytes)
    if extension == ".docx":
        return _extract_docx(file_bytes)

    return file_bytes.decode("utf-8", errors="ignore")


def detect_skills(text: str) -> list[str]:
    lowered = text.lower()
    skills = [skill for skill in SKILL_BANK if skill in lowered]
    return sorted(skills)


def compute_missing_skills(existing_skills: list[str], dream_vibe: str) -> list[str]:
    target_map = {
        "ai": ["python", "machine learning", "system design", "communication"],
        "data": ["sql", "python", "data analysis", "communication"],
        "backend": ["python", "fastapi", "docker", "system design"],
        "lead": ["leadership", "communication", "product thinking", "system design"],
    }

    profile = ["communication", "system design", "python"]
    vibe = dream_vibe.lower()
    for key, mapped in target_map.items():
        if key in vibe:
            profile = mapped
            break

    existing_set = set(existing_skills)
    return [skill for skill in profile if skill not in existing_set]


def build_rewrites(text: str, max_rewrites: int = 3) -> list[ResumeRewrite]:
    lines = [line.strip("•- ") for line in text.splitlines() if line.strip()]
    candidate_lines = [line for line in lines if len(line.split()) >= 6][:max_rewrites]

    rewrites: list[ResumeRewrite] = []
    for line in candidate_lines:
        improved = (
            f"Led {line.lower()} and improved delivery quality by 25% through measurable execution and cross-team collaboration."
        )
        rewrites.append(ResumeRewrite(original=line, improved=improved))

    if rewrites:
        return rewrites

    return [
        ResumeRewrite(
            original="Worked on multiple backend tasks.",
            improved="Delivered backend automation that reduced processing time by 30% and increased service reliability.",
        )
    ]


def _extract_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def _extract_docx(file_bytes: bytes) -> str:
    document = Document(BytesIO(file_bytes))
    return "\n".join(paragraph.text for paragraph in document.paragraphs)
