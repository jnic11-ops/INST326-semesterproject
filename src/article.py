from __future__ import annotations
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Iterable, Any
import logging

# Optional imports from the project; gracefully degrade if missing
_project_clean_text = None
_validate_ticker = None
_project_normalize_date = None
_fetch_news = None
_log_metadata = None

try:
    from src.utils.nlp_utils import clean_text as _project_clean_text
except Exception:
    _project_clean_text = None

try:
    from src.utils.validation_utils import validate_ticker as _validate_ticker
except Exception:
    _validate_ticker = None

try:
    from src.utils.date_utils import normalize_date as _project_normalize_date
except Exception:
    _project_normalize_date = None

try:
    from src.data_collection.fetch_news import fetch_news as _fetch_news
except Exception:
    _fetch_news = None

try:
    from src.utils.log_utils import log_metadata as _log_metadata
except Exception:
    _log_metadata = None

_logger = logging.getLogger(__name__)


def _simple_tokenize(text: str) -> List[str]:
    if not text:
        return []
    tokens = text.lower().split()
    return [t for t in tokens if t.isalpha()]


def _clean_and_tokenize(text: str) -> List[str]:
    """
    Use project clean_text if available; otherwise use simple tokenizer.
    Filters tokens to alphabetic-only tokens.
    """
    if _project_clean_text:
        cleaned = _project_clean_text(text)
        toks = cleaned.lower().split()
        return [t for t in toks if t.isalpha()]
    else:
        return _simple_tokenize(text)


def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """
    Use project's normalize_date if available; otherwise try common formats.
    Returns datetime or None on failure.
    """
    if not date_str:
        return None
    if _project_normalize_date:
        try:
            return _project_normalize_date(date_str)
        except Exception:
            return None
    # local fallback
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except Exception:
            continue
    return None


@dataclass
class Article:
    title: str
    description: str
    source: Optional[str] = None
    published_at: Optional[datetime] = None
    url: Optional[str] = None
    meta: Dict[str, Any] = field(default_factory=dict)

    _tokens: Optional[List[str]] = field(default=None, init=False, repr=False)
    _freq: Optional[Dict[str, int]] = field(default=None, init=False, repr=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any], title_key: str = "title", desc_key: str = "description", source_key: str = "source", date_key: str = "published_at"):
        if not isinstance(data, dict):
            raise TypeError("Article.from_dict expects a dict")
        title = data.get(title_key) or data.get("title") or ""
        description = data.get(desc_key) or data.get("summary") or data.get("content") or ""
        src = data.get(source_key)
        if isinstance(src, dict):
            source = src.get("name") or src.get("id")
        else:
            source = src
        url = data.get("url") or data.get("link")
        date_raw = data.get(date_key) or data.get("publishedAt") or data.get("published") or data.get("date")
        published = _parse_date(date_raw) if date_raw else None
        meta = data.copy()
        return cls(title=str(title), description=str(description), source=source, published_at=published, url=url, meta=meta)

    def full_text(self) -> str:
        return " ".join(filter(None, [self.title, self.description]))

    def tokens(self, force_recompute: bool = False) -> List[str]:
        if self._tokens is None or force_recompute:
            self._tokens = _clean_and_tokenize(self.full_text())
            self._freq = None
        return self._tokens

    def word_frequency(self, top_n: Optional[int] = None, force_recompute: bool = False) -> Dict[str, int]:
        if self._freq is None or force_recompute:
            self._freq = dict(Counter(self.tokens(force_recompute=force_recompute)))
        if top_n is None:
            return self._freq
        return dict(Counter(self._freq).most_common(top_n))

    def keyword_list(self, n: int = 10) -> List[str]:
        return [w for w, _ in Counter(self.word_frequency()).most_common(n)]

    def contains(self, substring: str) -> bool:
        if not substring:
            return False
        s = substring.lower()
        return s in self.full_text().lower()

    def positions_of(self, token: str) -> List[int]:
        t = token.lower()
        return [i for i, w in enumerate(self.tokens()) if w == t]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "source": self.source,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "url": self.url,
            "meta": self.meta,
        }

    def extract_entities(self) -> Dict[str, List[str]]:
        # placeholder for NER extraction; override in subclass
        return {"persons": [], "organizations": [], "locations": []}


class ArticleCollection:
    def __init__(self, articles: Optional[Iterable[Article]] = None):
        self._articles: List[Article] = []
        if articles:
            self.add_many(articles)

    @classmethod
    def from_dicts(cls, dicts: Iterable[Dict[str, Any]], **kwargs) -> "ArticleCollection":
        arts = [Article.from_dict(d, **kwargs) for d in dicts]
        return cls(arts)

    @classmethod
    def from_fetch_news(cls, ticker: str, providers: Iterable, cleaner=None, limit: Optional[int] = None, validate_ticker: bool = True) -> "ArticleCollection":
        """
        Convenience constructor that calls the project's fetch_news function (if available)
        and converts results to Article instances.
        """
        if validate_ticker and _validate_ticker:
            if not _validate_ticker(ticker):
                raise ValueError(f"Ticker '{ticker}' failed validation")

        if not _fetch_news:
            raise RuntimeError("fetch_news integration not available in this environment")

        raw = _fetch_news(ticker, providers, cleaner=cleaner, limit=limit)
        arts = [Article.from_dict(item) for item in raw]
        # Optionally log metadata about the fetch if project's log_metadata is available
        if _log_metadata:
            try:
                meta = _log_metadata("fetch_news", {"ticker": ticker, "count": len(arts)})
                _logger.info("Fetched news metadata: %s", meta)
            except Exception:
                _logger.info("Fetched %d articles for %s", len(arts), ticker)
        return cls(arts)

    def add(self, article: Article):
        if not isinstance(article, Article):
            raise TypeError("article must be an Article instance")
        self._articles.append(article)

    def add_many(self, articles: Iterable[Article]):
        for a in articles:
            self.add(a)

    def __len__(self):
        return len(self._articles)

    def __iter__(self):
        return iter(self._articles[:])

    def filter_by_source(self, source_substr: str) -> List[Article]:
        if not source_substr:
            return []
        s = source_substr.lower()
        return [a for a in self._articles if a.source and s in str(a.source).lower()]

    def filter_by_keyword(self, token: str) -> List[Article]:
        if not token:
            return []
        t = token.lower()
        return [a for a in self._articles if t in a.tokens() or a.contains(t)]

    def date_range(self) -> Optional[Dict[str, datetime]]:
        dates = [a.published_at for a in self._articles if a.published_at is not None]
        if not dates:
            return None
        return {"min": min(dates), "max": max(dates)}

    def _all_tokens(self) -> List[str]:
        tokens = []
        for a in self._articles:
            tokens.extend(a.tokens())
        return tokens

    def overall_frequency(self) -> Dict[str, int]:
        return dict(Counter(self._all_tokens()))

    def top_keywords(self, top_n: int = 20) -> Dict[str, int]:
        return dict(Counter(self._all_tokens()).most_common(top_n))

    def generate_wordcloud_data(self, top_n: int = 200, min_freq: int = 1) -> Dict[str, int]:
        all_freq = Counter(self._all_tokens())
        filtered = {w: c for w, c in all_freq.items() if c >= min_freq}
        most = Counter(filtered).most_common(top_n)
        return dict(most)

    def to_list_of_dicts(self) -> List[Dict[str, Any]]:
        return [a.to_dict() for a in self._articles]

    def summarize_top_keywords_str(self, top_n: int = 10) -> str:
        top = self.top_keywords(top_n)
        return ", ".join(f"{w} ({c})" for w, c in top.items())