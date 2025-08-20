"""Web Scraping Tool for reviews, news, and media data."""

import logging
import time
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def scrape_web_data_tool(urls: list[str], data_type: str) -> dict[str, Any]:
    """
    Scrapes additional game info from websites.

    Args:
        urls: List of URLs to scrape
        data_type: Type of data to extract ('reviews', 'news', 'specs', 'media')

    Returns:
        Dict containing structured data based on data_type
    """
    try:
        logger.info(f"Scraping {data_type} data from {len(urls)} URLs")

        results = {
            "data_type": data_type,
            "scraped_data": [],
            "errors": [],
            "total_urls": len(urls),
            "successful_scrapes": 0,
        }

        for url in urls:
            try:
                scraped = _scrape_single_url(url, data_type)
                if scraped:
                    results["scraped_data"].append(scraped)
                    results["successful_scrapes"] += 1
                else:
                    # Empty result means scraping failed
                    error_msg = f"Failed to scrape {url}: No data extracted"
                    results["errors"].append(error_msg)

                # Rate limiting
                time.sleep(1)

            except Exception as e:
                error_msg = f"Error scraping {url}: {str(e)}"
                logger.warning(error_msg)
                results["errors"].append(error_msg)

        logger.info(f"Scraping completed: {results['successful_scrapes']}/{len(urls)} successful")
        return results

    except Exception as e:
        logger.error(f"Web scraping error: {str(e)}")
        return {
            "data_type": data_type,
            "scraped_data": [],
            "errors": [str(e)],
            "total_urls": len(urls) if urls else 0,
            "successful_scrapes": 0,
        }


def _scrape_single_url(url: str, data_type: str) -> dict[str, Any]:
    """Scrape a single URL based on data type."""

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract data based on type
        if data_type == "reviews":
            return _extract_review_data(soup, url)
        elif data_type == "news":
            return _extract_news_data(soup, url)
        elif data_type == "specs":
            return _extract_specs_data(soup, url)
        elif data_type == "media":
            return _extract_media_data(soup, url)
        else:
            return _extract_general_data(soup, url)

    except Exception as e:
        logger.warning(f"Failed to scrape {url}: {str(e)}")
        return {}


def _extract_review_data(soup: BeautifulSoup, url: str) -> dict[str, Any]:
    """Extract review data from webpage."""

    review_data = {
        "url": url,
        "type": "review",
        "title": "",
        "score": "",
        "summary": "",
        "author": "",
        "date": "",
        "pros": [],
        "cons": [],
    }

    try:
        # Title extraction
        title_selectors = ["h1", ".review-title", ".article-title", "[data-testid='review-title']"]

        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                review_data["title"] = title_elem.get_text(strip=True)
                break

        # Score extraction (common patterns)
        score_selectors = [
            ".score",
            ".rating",
            ".review-score",
            "[data-testid='score']",
            ".metacritic-score",
        ]

        for selector in score_selectors:
            score_elem = soup.select_one(selector)
            if score_elem:
                review_data["score"] = score_elem.get_text(strip=True)
                break

        # Summary/content extraction
        content_selectors = [".review-content", ".article-content", ".review-body", "article p"]

        for selector in content_selectors:
            content_elems = soup.select(selector)
            if content_elems:
                paragraphs = [p.get_text(strip=True) for p in content_elems[:3]]
                review_data["summary"] = " ".join(paragraphs)[:500] + "..."
                break

        # Author extraction
        author_selectors = [".author", ".reviewer", ".byline", "[data-testid='author']"]

        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                review_data["author"] = author_elem.get_text(strip=True)
                break

        # Pros/Cons extraction
        pros_elem = soup.select_one(".pros, .positive, .review-pros")
        if pros_elem:
            pros_items = pros_elem.find_all("li")
            review_data["pros"] = [item.get_text(strip=True) for item in pros_items]

        cons_elem = soup.select_one(".cons, .negative, .review-cons")
        if cons_elem:
            cons_items = cons_elem.find_all("li")
            review_data["cons"] = [item.get_text(strip=True) for item in cons_items]

    except Exception as e:
        logger.warning(f"Error extracting review data from {url}: {str(e)}")

    return review_data


def _extract_news_data(soup: BeautifulSoup, url: str) -> dict[str, Any]:
    """Extract news article data."""

    news_data = {
        "url": url,
        "type": "news",
        "headline": "",
        "summary": "",
        "author": "",
        "date": "",
        "tags": [],
    }

    try:
        # Headline
        headline_selectors = ["h1", ".headline", ".article-title"]
        for selector in headline_selectors:
            headline_elem = soup.select_one(selector)
            if headline_elem:
                news_data["headline"] = headline_elem.get_text(strip=True)
                break

        # Summary from first few paragraphs
        paragraphs = soup.select("article p, .content p, .article-body p")
        if paragraphs:
            summary_text = " ".join([p.get_text(strip=True) for p in paragraphs[:2]])
            news_data["summary"] = summary_text[:400] + "..."

        # Tags/categories
        tag_selectors = [".tags a", ".categories a", ".keywords a"]
        for selector in tag_selectors:
            tag_elems = soup.select(selector)
            if tag_elems:
                news_data["tags"] = [tag.get_text(strip=True) for tag in tag_elems]
                break

    except Exception as e:
        logger.warning(f"Error extracting news data from {url}: {str(e)}")

    return news_data


def _extract_specs_data(soup: BeautifulSoup, url: str) -> dict[str, Any]:
    """Extract technical specifications."""

    specs_data = {
        "url": url,
        "type": "specs",
        "system_requirements": {},
        "technical_details": {},
        "features": [],
    }

    try:
        # Look for system requirements tables
        req_tables = soup.select(".system-requirements table, .specs-table")

        for table in req_tables:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all(["td", "th"])
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    specs_data["system_requirements"][key] = value

        # Features list
        feature_lists = soup.select(".features ul, .game-features ul")
        for feature_list in feature_lists:
            items = feature_list.find_all("li")
            specs_data["features"] = [item.get_text(strip=True) for item in items]
            break

    except Exception as e:
        logger.warning(f"Error extracting specs data from {url}: {str(e)}")

    return specs_data


def _extract_media_data(soup: BeautifulSoup, url: str) -> dict[str, Any]:
    """Extract media links and assets."""

    media_data = {"url": url, "type": "media", "images": [], "videos": [], "trailers": []}

    try:
        base_url = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

        # Extract images
        img_tags = soup.find_all("img")
        for img in img_tags:
            src = img.get("src") or img.get("data-src")
            if src:
                full_url = urljoin(base_url, src)
                alt_text = img.get("alt", "")
                if any(
                    keyword in alt_text.lower() for keyword in ["screenshot", "game", "trailer"]
                ):
                    media_data["images"].append({"url": full_url, "alt": alt_text})

        # Extract video/iframe embeds
        video_tags = soup.find_all(["video", "iframe"])
        for video in video_tags:
            src = video.get("src")
            if src:
                if "youtube" in src or "vimeo" in src:
                    media_data["videos"].append(src)

        # Look for trailer links
        trailer_links = soup.find_all("a", href=True)
        for link in trailer_links:
            href = link.get("href")
            text = link.get_text(strip=True).lower()
            if "trailer" in text and ("youtube.com" in href or "youtu.be" in href):
                media_data["trailers"].append({"url": href, "title": link.get_text(strip=True)})

    except Exception as e:
        logger.warning(f"Error extracting media data from {url}: {str(e)}")

    return media_data


def _extract_general_data(soup: BeautifulSoup, url: str) -> dict[str, Any]:
    """Extract general page data."""

    return {
        "url": url,
        "type": "general",
        "title": soup.title.string if soup.title else "",
        "description": "",
        "content_preview": "",
    }
