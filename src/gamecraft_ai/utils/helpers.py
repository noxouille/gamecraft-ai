import re


def format_duration(seconds: int) -> str:
    """Format duration in seconds to MM:SS format"""
    if seconds <= 0:
        return "00:00"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"


def extract_video_id(url: str) -> str | None:
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})",
        r"youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def clean_text(text: str) -> str:
    """Clean and normalize text"""
    if not text:
        return ""

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text.strip())

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\-.,!?:;"\'()[\]{}]', "", text)

    return text


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text

    return text[: max_length - len(suffix)] + suffix


def extract_game_name_candidates(text: str) -> list[str]:
    """Extract potential game names from text"""
    candidates = []

    # Common game name patterns
    patterns = [
        r"\b([A-Z][a-zA-Z\s:]+(?:\d+|[IVX]+)?)\b",  # Title case names with numbers/roman numerals
        r'"([^"]+)"',  # Quoted names
        r"'([^']+)'",  # Single quoted names
    ]

    for pattern in patterns:
        matches = re.findall(pattern, text)
        candidates.extend(matches)

    # Filter candidates
    filtered = []
    for candidate in candidates:
        candidate = candidate.strip()
        # Skip common words and short candidates
        if len(candidate) > 3 and candidate.lower() not in [
            "game",
            "video",
            "review",
            "trailer",
            "gameplay",
        ]:
            filtered.append(candidate)

    return list(set(filtered))  # Remove duplicates


def validate_url(url: str) -> bool:
    """Validate if string is a proper URL"""
    url_pattern = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    return bool(url_pattern.match(url))


def detect_language_simple(text: str) -> str:
    """Simple language detection based on common words"""
    french_indicators = [
        "le",
        "la",
        "les",
        "de",
        "du",
        "des",
        "un",
        "une",
        "et",
        "est",
        "sur",
        "avec",
        "pour",
        "dans",
        "par",
        "fais",
        "crée",
        "résumé",
        "minutes",
        "vidéo",
        "critique",
        "aperçu",
        "jeu",
    ]

    english_indicators = [
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "make",
        "create",
        "video",
        "review",
        "preview",
        "game",
        "about",
        "minutes",
    ]

    text_lower = text.lower()
    words = text_lower.split()

    french_count = sum(1 for word in words if word in french_indicators)
    english_count = sum(1 for word in words if word in english_indicators)

    if french_count > english_count:
        return "fr"
    else:
        return "en"


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system use"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Remove multiple underscores
    filename = re.sub(r"_+", "_", filename)

    # Trim and remove leading/trailing dots and spaces
    filename = filename.strip(". ")

    # Limit length
    if len(filename) > 255:
        filename = filename[:255]

    return filename or "untitled"
