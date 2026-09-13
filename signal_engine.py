
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List

from config import BUY_THRESHOLD, SELL_THRESHOLD, ROLLING_WINDOW_SIZE
from news_fetcher import NewsItem
from sector_classifier import SectorClassifier
from sentiment_analyzer import SentimentAnalyzer, SentimentResult


@dataclass
class AnalyzedArticle:
    news: NewsItem
    sentiment: SentimentResult
    sectors: List[str]


@dataclass
class SectorSignal:
    sector: str
    avg_sentiment: float
    article_count: int
    signal: str
    confidence_pct: float
    top_articles: List[AnalyzedArticle]


class SignalEngine:
    def __init__(self):
        self.sector_classifier = SectorClassifier()
        self.sentiment_analyzer = SentimentAnalyzer()

    def analyze_articles(self, news_items: List[NewsItem]) -> List[AnalyzedArticle]:
        analyzed = []
        for item in news_items:
            sentiment = self.sentiment_analyzer.analyze(item.full_text)
            sectors = self.sector_classifier.classify(item.full_text)
            analyzed.append(AnalyzedArticle(news=item, sentiment=sentiment, sectors=sectors))
        return analyzed

    @staticmethod
    def _recency_weight(published: datetime) -> float:
        now = datetime.now(timezone.utc)
        age_hours = max(0.0, (now - published).total_seconds() / 3600.0)
        weight = 1.0 - min(age_hours / 24.0, 0.8)
        return max(weight, 0.2)

    def _signal_from_score(self, score: float) -> str:
        if score >= BUY_THRESHOLD:
            return "BUY"
        if score <= SELL_THRESHOLD:
            return "SELL"
        return "HOLD"

    def generate_sector_signals(self, news_items: List[NewsItem]) -> Dict[str, SectorSignal]:
        analyzed = self.analyze_articles(news_items)

        by_sector: Dict[str, List[AnalyzedArticle]] = defaultdict(list)
        for article in analyzed:
            for sector in article.sectors:
                by_sector[sector].append(article)

        results: Dict[str, SectorSignal] = {}
        for sector, articles in by_sector.items():

            articles = sorted(articles, key=lambda a: a.news.published, reverse=True)
            window = articles[:ROLLING_WINDOW_SIZE]

            weighted_sum = 0.0
            weight_total = 0.0
            for a in window:
                w = self._recency_weight(a.news.published)
                weighted_sum += a.sentiment.compound * w
                weight_total += w

            avg_sentiment = weighted_sum / weight_total if weight_total else 0.0
            signal = self._signal_from_score(avg_sentiment)
            confidence = round(min(abs(avg_sentiment) / 0.5, 1.0) * 100, 1)

            results[sector] = SectorSignal(
                sector=sector,
                avg_sentiment=round(avg_sentiment, 4),
                article_count=len(window),
                signal=signal,
                confidence_pct=confidence,
                top_articles=window[:5],
            )

        return results


if __name__ == "__main__":
    from news_fetcher import NewsFetcher

    engine = SignalEngine()
    items = NewsFetcher().fetch_latest_news()
    signals = engine.generate_sector_signals(items)
    for sector, sig in sorted(signals.items(), key=lambda kv: -abs(kv[1].avg_sentiment)):
        print(f"{sector:30s} {sig.signal:5s} sentiment={sig.avg_sentiment:+.3f} "
              f"conf={sig.confidence_pct:5.1f}%  n={sig.article_count}")
