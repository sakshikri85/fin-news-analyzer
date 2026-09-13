
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime

from config import REFRESH_INTERVAL_SECONDS
from database import SignalDatabase
from news_fetcher import NewsFetcher
from signal_engine import SignalEngine


def run_cycle(fetcher: NewsFetcher, engine: SignalEngine, db: SignalDatabase) -> None:
    print(f"\n{'=' * 70}")
    print(f"Cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    news_items = fetcher.fetch_latest_news()
    if not news_items:
        print("No news items fetched this cycle (check internet connection "
              "or RSS feed availability). Will retry next cycle.")
        return

    signals = engine.generate_sector_signals(news_items)
    db.save_signals(signals)

    ranked = sorted(signals.items(), key=lambda kv: -abs(kv[1].avg_sentiment))
    print(f"{'Sector':32s} {'Signal':6s} {'Sentiment':>10s} {'Confidence':>11s} {'#News':>6s}")
    print("-" * 70)
    for sector, sig in ranked:
        print(f"{sector:32s} {sig.signal:6s} {sig.avg_sentiment:>+10.3f} "
              f"{sig.confidence_pct:>10.1f}% {sig.article_count:>6d}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Financial News Impact Analyzer")
    parser.add_argument("--once", action="store_true", help="Run a single cycle and exit")
    parser.add_argument(
        "--interval", type=int, default=REFRESH_INTERVAL_SECONDS,
        help=f"Seconds between refresh cycles (default: {REFRESH_INTERVAL_SECONDS})",
    )
    args = parser.parse_args()

    fetcher = NewsFetcher()
    engine = SignalEngine()
    db = SignalDatabase()

    if args.once:
        run_cycle(fetcher, engine, db)
        return

    print("Starting real-time Financial News Impact Analyzer.")
    print(f"Refreshing every {args.interval} seconds. Press Ctrl+C to stop.")
    try:
        while True:
            run_cycle(fetcher, engine, db)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nStopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
