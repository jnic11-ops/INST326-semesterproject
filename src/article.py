from typing import List, Dict, Optional, Any
from datetime import datetime
from collections import Counter

class Article:
    """
    Represents a financial news article with analysis capabilities.
    
    Attributes:
        title (str): Article headline
        description (str): Article body/summary text
        source (str): News source/publisher
        published_at (datetime): Publication timestamp
        url (str): Article URL (read-only)
    
    Examples:
        >>> article = Article("Apple Reports Earnings", "Strong results...")
        >>> article.get_keywords(5)
        ['apple', 'reports', 'earnings', 'strong', 'results']
    """
    
    def __init__(self, title: str, description: str, 
                 source: Optional[str] = None,
                 published_at: Optional[datetime] = None,
                 url: Optional[str] = None):
        """
        Initialize an Article.
        
        Args:
            title: Article headline
            description: Article body text
            source: News source (default: None)
            published_at: Publication time (default: now)
            url: Article URL (default: None)
            
        Raises:
            ValueError: If title or description is empty
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")
        
        self._title = title.strip()
        self._description = description.strip()
        self._source = source.strip() if source else "Unknown"
        self._published_at = published_at or datetime.now()
        self._url = url.strip() if url else None
        self._tokens: Optional[List[str]] = None
    
    @property
    def title(self) -> str:
        """str: Get the article title."""
        return self._title
    
    @property
    def description(self) -> str:
        """str: Get the article description."""
        return self._description
    
    @property
    def source(self) -> str:
        """str: Get the news source."""
        return self._source
    
    @property
    def published_at(self) -> datetime:
        """datetime: Get the publication date."""
        return self._published_at
    
    @property
    def url(self) -> Optional[str]:
        """Optional[str]: Get the article URL (read-only)."""
        return self._url
    
    def get_tokens(self) -> List[str]:
        """
        Extract word tokens from article text.
        
        Returns:
            List[str]: List of lowercase alphabetic words
        """
        if self._tokens is None:
            text = f"{self._title} {self._description}".lower()
            self._tokens = [w for w in text.split() if w.isalpha()]
        return self._tokens.copy()
    
    def get_keywords(self, n: int = 10) -> List[str]:
        """
        Get top N most frequent keywords.
        
        Args:
            n: Number of keywords (default: 10)
            
        Returns:
            List[str]: Top keywords by frequency
        """
        freq = Counter(self.get_tokens())
        return [word for word, _ in freq.most_common(n)]
    
    def contains_keyword(self, keyword: str) -> bool:
        """
        Check if article contains keyword (case-insensitive).
        
        Args:
            keyword: Word to search for
            
        Returns:
            bool: True if keyword found
        """
        return keyword.lower() in self.get_tokens() if keyword else False
    
    def __str__(self) -> str:
        return f"{self._title} - {self._source}"
    
    def __repr__(self) -> str:
        return f"Article(title='{self._title[:30]}...', source='{self._source}')"


class ArticleCollection:
    """
    Manages a collection of news articles with aggregate analysis.
    
    Attributes:
        articles (List[Article]): List of articles (read-only)
        article_count (int): Number of articles
    
    Examples:
        >>> collection = ArticleCollection()
        >>> collection.add_article(Article("News", "Content"))
        >>> collection.article_count
        1
    """
    
    def __init__(self):
        """Initialize an empty ArticleCollection."""
        self._articles: List[Article] = []
    
    @property
    def articles(self) -> List[Article]:
        """List[Article]: Get articles list (read-only copy)."""
        return self._articles.copy()
    
    @property
    def article_count(self) -> int:
        """int: Get number of articles."""
        return len(self._articles)
    
    def add_article(self, article: Article) -> None:
        """
        Add an article to collection.
        
        Args:
            article: Article instance to add
            
        Raises:
            TypeError: If not an Article instance
        """
        if not isinstance(article, Article):
            raise TypeError("Must provide an Article instance")
        self._articles.append(article)
    
    def filter_by_source(self, source: str) -> List[Article]:
        """
        Filter articles by source (case-insensitive).
        
        Args:
            source: Source name or substring
            
        Returns:
            List[Article]: Matching articles
        """
        if not source:
            return []
        return [a for a in self._articles if source.lower() in a.source.lower()]
    
    def filter_by_keyword(self, keyword: str) -> List[Article]:
        """
        Filter articles containing keyword.
        
        Args:
            keyword: Keyword to search for
            
        Returns:
            List[Article]: Articles with keyword
        """
        if not keyword:
            return []
        return [a for a in self._articles if a.contains_keyword(keyword)]
    
    def get_top_keywords(self, n: int = 20) -> Dict[str, int]:
        """
        Get most frequent keywords across all articles.
        
        Args:
            n: Number of keywords (default: 20)
            
        Returns:
            Dict[str, int]: Top keywords with frequencies
        """
        all_tokens = []
        for article in self._articles:
            all_tokens.extend(article.get_tokens())
        return dict(Counter(all_tokens).most_common(n))
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Generate collection summary.
        
        Returns:
            Dict with article count, sources, and top keywords
        """
        sources = list(set(a.source for a in self._articles))
        return {
            "total_articles": self.article_count,
            "sources": sources,
            "top_keywords": self.get_top_keywords(10) if self._articles else {}
        }
    
    def __len__(self) -> int:
        return self.article_count
    
    def __str__(self) -> str:
        return f"ArticleCollection with {self.article_count} articles"
    
    def __repr__(self) -> str:
        return f"ArticleCollection(articles={self.article_count})"
