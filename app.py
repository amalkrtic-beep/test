from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@dataclass(frozen=True)
class AdCopy:
    headlines: list[str]
    descriptions: list[str]


BENEFITS = [
    "Fast Results",
    "Trusted Experts",
    "Affordable Pricing",
    "Easy Setup",
    "24/7 Support",
    "Proven Quality",
]

CTAS = [
    "Get a Free Quote",
    "Book a Demo",
    "Shop Now",
    "Start Today",
    "Contact Us",
    "Learn More",
]


def normalize_keywords(raw: str) -> list[str]:
    return [kw.strip().title() for kw in raw.split(",") if kw.strip()]


def fit_limit(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text

    words = text.split()
    trimmed: list[str] = []
    for word in words:
        next_text = " ".join([*trimmed, word]).strip()
        if len(next_text) <= limit:
            trimmed.append(word)
        else:
            break

    fallback = " ".join(trimmed).strip()
    return (fallback[: limit - 1] + "…") if not fallback else fallback


def unique(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def generate_copy(keywords: list[str], headline_count: int, description_count: int) -> AdCopy:
    seed = keywords[0] if keywords else "Your Business"

    headline_candidates: list[str] = [
        f"{seed} Near You",
        f"Best {seed} Deals",
        f"Top Rated {seed}",
        f"{seed} - {BENEFITS[0]}",
        f"{seed} - {BENEFITS[1]}",
    ]

    for kw in keywords[1:]:
        headline_candidates.extend(
            [
                f"{kw} Specials",
                f"Save on {kw}",
                f"{kw} {BENEFITS[2]}",
            ]
        )

    for cta in CTAS:
        headline_candidates.append(f"{cta} | {seed}")

    description_candidates: list[str] = [
        f"Need {seed.lower()}? Get {BENEFITS[0].lower()} and {BENEFITS[2].lower()} from our team.",
        f"Compare {seed.lower()} options and choose a plan that fits your goals and budget.",
        f"Work with {BENEFITS[1].lower()} for {seed.lower()}. {CTAS[0]} and start now.",
    ]

    for kw in keywords:
        description_candidates.extend(
            [
                f"Discover premium {kw.lower()} with transparent pricing and friendly support.",
                f"We make {kw.lower()} simple with fast setup, expert help, and clear next steps.",
            ]
        )

    for cta in CTAS:
        description_candidates.append(f"{cta} for {seed.lower()} and see how easy it is to get started.")

    headlines = [fit_limit(text, 30) for text in unique(headline_candidates)]
    descriptions = [fit_limit(text, 90) for text in unique(description_candidates)]

    return AdCopy(headlines=headlines[:headline_count], descriptions=descriptions[:description_count])


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate():
    payload = request.get_json(silent=True) or {}
    keywords = normalize_keywords(payload.get("keywords", ""))

    if not keywords:
        return jsonify({"error": "Please enter at least one keyword."}), 400

    headline_count = max(3, min(int(payload.get("headline_count", 10)), 15))
    description_count = max(2, min(int(payload.get("description_count", 4)), 8))

    copy = generate_copy(keywords, headline_count, description_count)

    return jsonify(
        {
            "keywords": keywords,
            "headlines": copy.headlines,
            "descriptions": copy.descriptions,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
