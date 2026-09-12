"""
app.py
Streamlit real-time dashboard for the Financial News Impact Analyzer.

Run with:
    streamlit run app.py

The page auto-refreshes on a timer, re-fetches the latest financial news
from RSS feeds, runs NLP sentiment analysis, classifies articles by
sector, and displays a BUY / SELL / HOLD signal card per sector.
"""

from __future__ import annotations

import time
from datetime import datetime

import pandas as pd
import streamlit as st

from config import REFRESH_INTERVAL_SECONDS
from database import SignalDatabase
from news_fetcher import NewsFetcher
from signal_engine import SignalEngine

st.set_page_config(
    page_title="Financial News Impact Analyzer",
    page_icon="\U0001F4C8",
    layout="wide",
)

SIGNAL_COLORS = {"BUY": "#1a7f37", "SELL": "#d1242f", "HOLD": "#9a6700"}
SIGNAL_ICONS = {"BUY": "\u2B06\uFE0F", "SELL": "\u2B07\uFE0F", "HOLD": "\u27A1\uFE0F"}


@st.cache_resource
def get_engine_and_db():
    return NewsFetcher(), SignalEngine(), SignalDatabase()


def render_sector_card(sector, sig):
    color = SIGNAL_COLORS.get(sig.signal, "#666")
    icon = SIGNAL_ICONS.get(sig.signal, "")
    st.markdown(
        f"""
        <div style="border:1px solid #333;border-radius:10px;padding:14px 16px;
                    margin-bottom:10px;background-color:rgba(255,255,255,0.02);">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-size:16px;font-weight:600;">{sector}</span>
                <span style="font-size:15px;font-weight:700;color:{color};">
                    {icon} {sig.signal}
                </span>
            </div>
            <div style="margin-top:6px;font-size:13px;color:#aaa;">
                Sentiment: <b>{sig.avg_sentiment:+.3f}</b> &nbsp;|&nbsp;
                Confidence: <b>{sig.confidence_pct:.1f}%</b> &nbsp;|&nbsp;
                Articles analyzed: <b>{sig.article_count}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander(f"Top headlines \u2014 {sector}"):
        for a in sig.top_articles:
            st.markdown(
                f"- **[{a.sentiment.label}]** {a.news.title}  \n"
                f"  <small>{a.news.source} &middot; {a.news.published.strftime('%d %b %Y %H:%M UTC')}</small>",
                unsafe_allow_html=True,
            )


def main():
    st.title("\U0001F4C8 Financial News Impact Analyzer")
    st.caption(
        "Real-time NLP-driven sentiment analysis of financial news, "
        "mapped to sector-wise investment signals. "
        "**Educational tool only \u2014 not financial advice.**"
    )

    fetcher, engine, db = get_engine_and_db()

    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        auto_refresh = st.checkbox("Enable auto-refresh", value=True)
    with col_b:
        interval = st.number_input(
            "Refresh every (sec)", min_value=30, max_value=1800,
            value=REFRESH_INTERVAL_SECONDS, step=30,
        )
    with col_c:
        run_now = st.button("Refresh now", use_container_width=True)

    placeholder = st.empty()

    def run_and_render():
        with placeholder.container():
            with st.spinner("Fetching latest financial news and running NLP analysis..."):
                news_items = fetcher.fetch_latest_news()

                if not news_items:
                    st.error(
                        "No news could be fetched. Check your internet connection "
                        "or try again \u2014 some RSS feeds may be temporarily unavailable."
                    )
                    return

                signals = engine.generate_sector_signals(news_items)
                db.save_signals(signals)

            st.success(
                f"Last updated: {datetime.now().strftime('%d %b %Y, %H:%M:%S')} "
                f"\u2014 {len(news_items)} articles analyzed across {len(signals)} sectors."
            )

            summary_rows = [
                {
                    "Sector": sector,
                    "Signal": sig.signal,
                    "Sentiment": sig.avg_sentiment,
                    "Confidence %": sig.confidence_pct,
                    "Articles": sig.article_count,
                }
                for sector, sig in signals.items()
            ]
            df = pd.DataFrame(summary_rows).sort_values("Sentiment", ascending=False)

            tab1, tab2 = st.tabs(["Sector Signal Cards", "Table & Chart"])

            with tab1:
                ranked = sorted(signals.items(), key=lambda kv: -kv[1].avg_sentiment)
                left, right = st.columns(2)
                for i, (sector, sig) in enumerate(ranked):
                    with (left if i % 2 == 0 else right):
                        render_sector_card(sector, sig)

            with tab2:
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.bar_chart(df.set_index("Sector")["Sentiment"])

    if run_now or "initialized" not in st.session_state:
        st.session_state["initialized"] = True
        run_and_render()
    else:
        run_and_render()

    if auto_refresh:
        time.sleep(interval)
        st.rerun()


if __name__ == "__main__":
    main()
