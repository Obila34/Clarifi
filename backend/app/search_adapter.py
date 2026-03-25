import os

import httpx

from .models import ResourceCard


async def search_market_cards(query: str) -> list[ResourceCard]:
    serper_key = os.getenv("SERPER_API_KEY")

    if serper_key:
        try:
            async with httpx.AsyncClient(timeout=12) as client:
                response = await client.post(
                    "https://google.serper.dev/search",
                    json={"q": query},
                    headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
                )
                response.raise_for_status()
                payload = response.json()

            organic_results = payload.get("organic", [])[:3]
            cards = []
            for item in organic_results:
                cards.append(
                    ResourceCard(
                        title=item.get("title", "Market Insight"),
                        url=item.get("link", "https://example.com"),
                        platform_icon="🌐",
                        price="Live",
                    )
                )
            if cards:
                return cards
        except Exception:
            pass

    return [
        ResourceCard(
            title=f"Live Demand Signals for: {query}",
            url="https://www.linkedin.com/jobs/",
            platform_icon="💼",
            price="Free",
        ),
        ResourceCard(
            title="Salary Benchmarks and Role Trends",
            url="https://www.glassdoor.com/Salaries/",
            platform_icon="📊",
            price="Free",
        ),
        ResourceCard(
            title="Tech Career News and Role Launches",
            url="https://techcrunch.com/tag/artificial-intelligence/",
            platform_icon="📰",
            price="Free",
        ),
    ]
