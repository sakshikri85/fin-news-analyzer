
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

import feedparser

from config import RSS_FEEDS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class NewsItem:
    title: str
    summary: str
    link: str
    source: str
    published: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def full_text(self) -> str:
        return f"{self.title}. {self.summary}".strip()


class NewsFetcher:

    def __init__(self, feed_urls: List[str] | None = None):
        self.feed_urls = feed_urls or RSS_FEEDS

    def _parse_published(self, entry) -> datetime:
        for attr in ("published_parsed", "updated_parsed"):
            value = getattr(entry, attr, None)
            if value:
                try:
                    return datetime(*value[:6], tzinfo=timezone.utc)
                except Exception:
                    pass
        return datetime.now(timezone.utc)

    def fetch_feed(self, url: str) -> List[NewsItem]:
        items: List[NewsItem] = []
        try:
            parsed = feedparser.parse(url)
            if parsed.bozo and not parsed.entries:
                logger.warning("Feed unreachable or malformed, skipping: %s", url)
                return items
            source_name = parsed.feed.get("title", url) if hasattr(parsed, "feed") else url
            for entry in parsed.entries:
                items.append(
                    NewsItem(
                        title=entry.get("title", "").strip(),
                        summary=entry.get("summary", entry.get("description", "")).strip(),
                        link=entry.get("link", ""),
                        source=source_name,
                        published=self._parse_published(entry),
                    )
                )
        except Exception as exc:
            logger.warning("Failed to fetch feed %s: %s", url, exc)
        return items

    def fetch_latest_news(self) -> List[NewsItem]:
        all_items: List[NewsItem] = []
        seen_titles = set()

        for url in self.feed_urls:
            for item in self.fetch_feed(url):
                key = item.title.lower().strip()
                if key and key not in seen_titles:
                    seen_titles.add(key)
                    all_items.append(item)

        all_items.sort(key=lambda i: i.published, reverse=True)
        logger.info("Fetched %d unique news items across %d feeds", len(all_items), len(self.feed_urls))
        return all_items


if __name__ == "__main__":
    fetcher = NewsFetcher()
    news = fetcher.fetch_latest_news()
    for n in news[:5]:
        print(f"- [{n.source}] {n.title}")
