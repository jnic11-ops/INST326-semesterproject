import re

def extract_domain(url: str) -> str:
    """
    Extract the domain (host) from a URL string.

    Parameters
    ----------
    url : str

    Returns
    -------
    str: Domain without 'www.' prefix

    Raises
    ------
    ValueError: If URL is invalid
    """
    if not isinstance(url, str) or not url.strip():
        raise ValueError("url must be a non-empty string")
    url = url.strip()
    m = re.match(r"^(?:https?://)?(?P<host>[^/:?#]+)", url, flags=re.IGNORECASE)
    if not m:
        raise ValueError(f"Could not extract domain from URL: {url}")
    host = m.group("host").lower()
    if host.startswith("www."):
        host = host[4:]
    return host
