"""
Configuration for Financial News Impact Analyzer.
Contains RSS news sources and sector -> keyword/company mappings
used for classifying each news item into a market sector.
"""

# ---------------------------------------------------------------------------
# Free, no-API-key RSS feeds (Indian financial/business news).
# You can add/remove feeds freely; the fetcher will skip any that fail.
# ---------------------------------------------------------------------------
RSS_FEEDS = [
    "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "https://www.moneycontrol.com/rss/business.xml",
    "https://www.moneycontrol.com/rss/marketreports.xml",
    "https://www.business-standard.com/rss/markets-106.rss",
    "https://www.livemint.com/rss/markets",
]

# How many seconds between automatic refresh cycles in real-time mode.
REFRESH_INTERVAL_SECONDS = 120

# How many most-recent articles (per sector) to consider when computing
# the rolling sentiment signal.
ROLLING_WINDOW_SIZE = 15

# Signal thresholds (on a -1 .. +1 compound sentiment scale)
BUY_THRESHOLD = 0.15
SELL_THRESHOLD = -0.15

# ---------------------------------------------------------------------------
# Sector classification map: sector name -> list of keywords / company
# names / tickers that indicate a news item belongs to that sector.
# Matching is case-insensitive substring matching on title + summary.
# ---------------------------------------------------------------------------
SECTOR_KEYWORDS = {
    "Banking & Financial Services": [
        "hdfc", "icici", "sbi", "state bank", "axis bank", "kotak mahindra",
        "bank of baroda", "pnb", "punjab national bank", "indusind",
        "bajaj finance", "bajaj finserv", "rbi", "reserve bank", "nbfc",
        "repo rate", "interest rate", "banking sector", "yes bank", "idfc",
    ],
    "Information Technology": [
        "tcs", "tata consultancy", "infosys", "wipro", "hcl tech", "hcltech",
        "tech mahindra", "lti mindtree", "ltimindtree", "it sector",
        "software services", "it stocks", "persistent systems", "coforge",
    ],
    "Pharma & Healthcare": [
        "sun pharma", "cipla", "dr reddy", "divi's lab", "divis lab",
        "lupin", "aurobindo pharma", "biocon", "apollo hospitals",
        "pharma sector", "drug", "fda approval", "healthcare stocks",
    ],
    "Automobile": [
        "maruti suzuki", "tata motors", "bajaj auto", "mahindra & mahindra",
        "m&m", "hero motocorp", "eicher motors", "tvs motor", "ashok leyland",
        "auto sector", "ev maker", "electric vehicle", "car sales",
        "auto stocks",
    ],
    "FMCG": [
        "itc", "hindustan unilever", "hul", "nestle india", "britannia",
        "dabur", "godrej consumer", "marico", "tata consumer", "fmcg sector",
        "fmcg stocks", "colgate",
    ],
    "Energy & Oil-Gas": [
        "reliance industries", "ongc", "bpcl", "hpcl", "indian oil", "iocl",
        "gail", "adani green", "adani energy", "ntpc", "power grid",
        "oil prices", "crude oil", "energy sector", "renewable energy",
    ],
    "Metals & Mining": [
        "tata steel", "jsw steel", "hindalco", "vedanta", "coal india",
        "nmdc", "sail", "steel authority", "metal stocks", "metal sector",
        "iron ore", "aluminium",
    ],
    "Infrastructure & Realty": [
        "larsen & toubro", "l&t", "dlf", "godrej properties", "oberoi realty",
        "prestige estates", "infra sector", "realty stocks", "real estate",
        "construction sector", "highway", "nhai",
    ],
    "Telecom": [
        "bharti airtel", "airtel", "vodafone idea", "vi ", "reliance jio",
        "jio", "telecom sector", "telecom stocks", "5g rollout", "trai",
    ],
    "Media & Entertainment": [
        "zee entertainment", "sun tv", "pvr inox", "media sector",
        "entertainment stocks", "network18", "ott platform",
    ],
}

# Extra finance-specific words that push VADER's generic sentiment score
# in the right direction for market news (VADER's default lexicon is
# tuned for social-media text, not financial reporting).
FINANCE_LEXICON_BOOST = {
    # positive
    "rally": 2.0, "surge": 2.2, "surges": 2.2, "soar": 2.3, "soars": 2.3,
    "jumps": 1.8, "beat estimates": 2.5, "beats estimates": 2.5,
    "record high": 2.4, "upgraded": 1.8, "outperform": 1.6, "bullish": 2.0,
    "profit rises": 2.0, "strong quarter": 1.8, "buyback": 1.2,
    "raises guidance": 2.0, "wins order": 1.5, "expansion": 1.0,
    # negative
    "plunge": -2.3, "plunges": -2.3, "tumbles": -2.0, "crashes": -2.4,
    "slumps": -2.0, "miss estimates": -2.5, "misses estimates": -2.5,
    "downgraded": -1.8, "bearish": -2.0, "probe": -1.7, "fraud": -2.6,
    "scam": -2.6, "loss widens": -2.2, "profit falls": -1.8,
    "profit declines": -1.8, "layoffs": -1.6, "resigns": -1.0,
    "default": -2.2, "insolvency": -2.4, "penalty": -1.5, "fine": -1.2,
}
