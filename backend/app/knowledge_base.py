from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeDoc:
    title: str
    body: str


CAREER_KB: list[KnowledgeDoc] = [
    KnowledgeDoc(
        title="Career Positioning Framework",
        body=(
            "Strong candidates position their impact using outcomes, stakeholders, and measurable results. "
            "A simple pattern: what you did, why it mattered, and what changed."
        ),
    ),
    KnowledgeDoc(
        title="Interview Story Design",
        body=(
            "Use concise STAR stories with one business metric and one collaboration detail. "
            "Interviewers reward clarity, prioritization, and ownership."
        ),
    ),
    KnowledgeDoc(
        title="Portfolio Signal Boost",
        body=(
            "A small portfolio with clear READMEs, before/after results, and architecture decisions "
            "often outperforms a large unfinished portfolio."
        ),
    ),
    KnowledgeDoc(
        title="Career Pivot Strategy",
        body=(
            "For role transitions, map existing strengths to adjacent job requirements and close only "
            "the top two skill gaps first."
        ),
    ),
]


def retrieve_relevant_docs(prompt: str, limit: int = 2) -> list[KnowledgeDoc]:
    prompt_terms = set(prompt.lower().split())

    ranked = sorted(
        CAREER_KB,
        key=lambda doc: len(prompt_terms.intersection(set(doc.body.lower().split()))),
        reverse=True,
    )
    return ranked[:limit]
