# Financial News Impact Analyzer — Sector-wise Investment Signals

A real-time **Financial News Impact Analyzer** that uses NLP and sentiment analysis to transform financial news into **sector-wise market insights and investment signals**.

> ⚠️ **Educational/Demo Project:** Generated signals are for analytical purposes only and do not constitute financial advice.

## 📌 Overview

The system automatically fetches financial news from multiple RSS sources, analyzes its sentiment, classifies articles into relevant market sectors, and generates **BUY / SELL / HOLD** signals based on recent sentiment trends.

## 🚀 Key Features

* **Real-Time News Processing** — Collects financial news from multiple RSS feeds.
* **NLP Sentiment Analysis** — Uses VADER with a custom finance-specific lexicon.
* **Sector Classification** — Categorizes news across Banking, IT, Pharma, Auto, FMCG, Energy, Metals, Infra, Telecom, and Media.
* **Signal Generation** — Produces BUY / SELL / HOLD signals using recency-weighted sentiment.
* **Confidence Scoring** — Estimates signal strength based on aggregated sentiment.
* **Historical Tracking** — Stores sector-wise sentiment and signals using SQLite.
* **Interactive Dashboard** — Streamlit dashboard for sector signals, sentiment analysis, and visual insights.

## 🛠️ Tech Stack

**Python • NLP • VADER • RSS/XML • Pandas • Streamlit • SQLite • Matplotlib**

## 🔄 Workflow

```text
Financial News
      ↓
RSS News Fetching
      ↓
Text Preprocessing & Sentiment Analysis
      ↓
Sector Classification
      ↓
Recency-Weighted Sentiment Aggregation
      ↓
BUY / SELL / HOLD Signal
      ↓
Streamlit Dashboard + SQLite History
```

## 📊 Signal Logic

Each article receives a sentiment score ranging from **-1 to +1**. Recent articles are assigned higher weights, and sector-level sentiment is aggregated to generate the final signal.

```text
Positive Sentiment → BUY
Negative Sentiment → SELL
Neutral Sentiment  → HOLD
```

## 🎯 Project Objective

To demonstrate the application of **NLP, real-time data processing, sentiment analysis, and data visualization** for extracting actionable insights from unstructured financial news.

## ⚠️ Disclaimer

This project is developed for **educational and demonstration purposes only**. It should not be used as a substitute for professional financial research or investment advice.
