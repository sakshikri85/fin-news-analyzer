# Financial News Impact Analyzer — Sector-wise Investment Signals

Real-time NLP project jo financial news ko fetch karke, sentiment analysis
karta hai, news ko market **sector** (Banking, IT, Pharma, Auto, FMCG,
Energy, Metals, Infra, Telecom, Media) me classify karta hai, aur har
sector ke liye **BUY / SELL / HOLD** investment signal generate karta hai.

> ⚠️ Educational/demo tool hai — **financial advice nahi hai**.

---

## Features

- **Real-time news fetching** — free RSS feeds (Economic Times, Moneycontrol,
  Business Standard, Livemint) se, koi paid API key ki zaroorat nahi.
- **NLP sentiment analysis** — VADER sentiment engine + custom finance-specific
  lexicon (jaise "beats estimates", "plunges", "fraud probe" etc. sahi se
  weight ho).
- **Sector classification** — keyword/company-based mapping se har news item
  ko relevant sector(s) me classify karta hai.
- **Signal engine** — recency-weighted rolling sentiment average se
  BUY/SELL/HOLD signal + confidence % banata hai.
- **Historical storage** — SQLite me har cycle ka signal save hota hai.
- **Two ways to run**:
  1. `main.py` — terminal me real-time loop (auto-refresh)
  2. `app.py` — Streamlit live dashboard (visual, auto-refreshing UI)

---

## Project Structure

```
fin-news-analyzer/
├── config.py              # RSS feeds, sector keywords, thresholds
├── news_fetcher.py         # Real-time RSS news fetching
├── sentiment_analyzer.py   # NLP sentiment scoring (VADER + finance lexicon)
├── sector_classifier.py    # Keyword-based sector classification
├── signal_engine.py        # Aggregates sentiment -> BUY/SELL/HOLD signal
├── database.py             # SQLite storage for signal history
├── main.py                 # Real-time CLI runner
├── app.py                  # Streamlit real-time dashboard
├── requirements.txt
└── README.md
```

---

## Setup (VS Code)

1. **Project folder VS Code me open karo** (`File > Open Folder`).

2. **Python interpreter select karo** (recent Python 3.10+ recommended):
   `Ctrl+Shift+P` → `Python: Select Interpreter`.

3. **Virtual environment banao** (recommended) — VS Code ke integrated
   terminal me (`` Ctrl+` ``):

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

4. **Dependencies install karo:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Run

### Option A — Terminal, real-time loop

```bash
python main.py
```

- Har `REFRESH_INTERVAL_SECONDS` (default 120s, `config.py` me change kar
  sakte ho) me fresh news fetch karke naya signal print karega.
- Single cycle ke liye: `python main.py --once`
- Custom interval: `python main.py --interval 60`
- Stop karne ke liye: `Ctrl+C`

### Option B — Streamlit live dashboard (recommended, visual)

```bash
streamlit run app.py
```

- Browser me `http://localhost:8501` par dashboard khulega.
- Sector-wise signal cards, sentiment table, aur bar chart dikhega.
- "Enable auto-refresh" checkbox on rakhoge to page apne aap refresh hoga.
- "Refresh now" button se manual refresh bhi kar sakte ho.

---

## Customization

- **Naye sectors/companies add karne ke liye**: `config.py` me
  `SECTOR_KEYWORDS` dictionary edit karo.
- **Naye news sources add karne ke liye**: `config.py` me `RSS_FEEDS`
  list me RSS URL add karo.
- **Signal sensitivity tune karne ke liye**: `config.py` me
  `BUY_THRESHOLD` / `SELL_THRESHOLD` adjust karo.
- **Rolling window size** (kitne recent articles consider ho): `config.py`
  me `ROLLING_WINDOW_SIZE`.

---

## How the signal is calculated

1. Har news article ki sentiment score nikalti hai (`-1` se `+1`).
2. Article ko uske recency ke hisaab se weight milta hai (naya article =
   zyada weight, 24 ghante se purana = kam weight).
3. Har sector ke top-N recent articles ka weighted average sentiment
   nikalta hai.
4. Threshold se compare karke signal decide hota hai:
   - `avg_sentiment >= BUY_THRESHOLD` → **BUY**
   - `avg_sentiment <= SELL_THRESHOLD` → **SELL**
   - warna → **HOLD**
5. Confidence % = `|avg_sentiment|` ko scale karke.

---

## Notes / Troubleshooting

- Agar "No news items fetched" dikhe, to internet connection check karo —
  ho sakta hai koi ek RSS feed temporarily down ho; baaki feeds se bhi kaam
  chal jaata hai, isiliye code crash nahi karta.
- Ye tool **educational/demo purpose** ke liye hai — real investment
  decisions ke liye proper research aur licensed financial advisor se
  consult karo.
