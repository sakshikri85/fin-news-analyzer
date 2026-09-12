"""
sentiment_analyzer.py
NLP sentiment scoring for financial news text.

Uses VADER (rule-based sentiment analyzer, fast and dependency-light -
ideal for real-time processing without a GPU) as the base engine, and
layers a finance-specific lexicon on top since VADER out of the box is
tuned for social-media text rather than financial reporting language
(e.g. "profit plunges" should score negative, "beats estimates" positive).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from config import FINANCE_LEXICON_BOOST


@dataclass
class SentimentResult:
    compound: float          # -1 .. +1 overall sentiment
    positive: float
    negative: float
    neutral: float
    label: str                # "Positive" / "Negative" / "Neutral"


class SentimentAnalyzer:
    def __init__(self):
        self._vader = SentimentIntensityAnalyzer()
        # Merge our finance-specific phrase boosts into VADER's lexicon.
        self._vader.lexicon.update(FINANCE_LEXICON_BOOST)

    @staticmethod
    def _clean(text: str) -> str:
        text = re.sub(r"<[^>]+>", " ", text)     # strip any HTML in RSS summaries
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def analyze(self, text: str) -> SentimentResult:
        clean_text = self._clean(text)
        scores = self._vader.polarity_scores(clean_text)

        # Apply multi-word finance phrase boosts VADER's tokenizer would
        # otherwise miss (VADER scores word-by-word).
        lowered = clean_text.lower()
        phrase_adjustment = 0.0
        for phrase, weight in FINANCE_LEXICON_BOOST.items():
            if " " in phrase and phrase in lowered:
                phrase_adjustment += weight * 0.1  # scaled contribution

        compound = max(-1.0, min(1.0, scores["compound"] + phrase_adjustment))

        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"

        return SentimentResult(
            compound=round(compound, 4),
            positive=scores["pos"],
            negative=scores["neg"],
            neutral=scores["neu"],
            label=label,
        )


if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    samples = [
        "TCS profit beats estimates, stock surges to record high",
        "Vodafone Idea shares plunge after fraud probe launched",
        "RBI keeps repo rate unchanged, markets flat",
    ]
    for s in samples:
        result = analyzer.analyze(s)
        print(f"{result.label:8s} ({result.compound:+.3f})  {s}")
