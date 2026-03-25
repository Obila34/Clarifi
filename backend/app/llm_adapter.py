import os

import httpx


def _fallback_summary(prompt: str, context: str) -> str:
    return (
        f"Based on your prompt ('{prompt}'), here is a synthesized signal using current workflow context: "
        f"{context[:260]}"
    )


async def synthesize_summary(prompt: str, context: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        return _fallback_summary(prompt, context)

    system_prompt = (
        "You are Clarifi, a career copilot. Return one concise, human sounding summary sentence "
        "for the frontend. Keep under 40 words."
    )
    user_prompt = f"Prompt: {prompt}\nContext: {context}"

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.3,
                    "max_tokens": 90,
                },
            )
            response.raise_for_status()
            payload = response.json()

        content = payload["choices"][0]["message"]["content"].strip()
        return content or _fallback_summary(prompt, context)
    except Exception:
        return _fallback_summary(prompt, context)
