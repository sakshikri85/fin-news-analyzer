"""
sector_classifier.py
Classifies a piece of financial news text into one or more market sectors
using keyword/company-name matching (fast, deterministic, no model needed
for real-time throughput). A news item can belong to more than one sector
if it mentions companies/keywords from multiple sectors.
"""

from __future__ import annotations

from typing import List

from config import SECTOR_KEYWORDS

UNCLASSIFIED = "General / Unclassified"


class SectorClassifier:
    def __init__(self):
        # Pre-lowercase keywords once for fast matching.
        self._map = {
            sector: [kw.lower() for kw in keywords]
            for sector, keywords in SECTOR_KEYWORDS.items()
        }

    def classify(self, text: str) -> List[str]:
        lowered = text.lower()
        matched = [
            sector
            for sector, keywords in self._map.items()
            if any(kw in lowered for kw in keywords)
        ]
        return matched if matched else [UNCLASSIFIED]


if __name__ == "__main__":
    clf = SectorClassifier()
    tests = [
        "HDFC Bank Q2 profit rises 15%, beats estimates",
        "Maruti Suzuki and Tata Motors post strong auto sales in festive season",
        "Local weather turns pleasant across northern India",
    ]
    for t in tests:
        print(t, "->", clf.classify(t))
