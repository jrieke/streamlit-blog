from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from markdownify import markdownify as md


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch a Streamlit Ghost blog article and save as Markdown."
    )
    parser.add_argument("url", help="Streamlit Ghost blog article URL")
    return parser.parse_args()


def validate_streamlit_ghost_url(url: str) -> None:
    """Validate that the URL points to streamlit.ghost.io."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must start with http or https.")
    if parsed.netloc != "streamlit.ghost.io":
        raise ValueError("URL must be from streamlit.ghost.io.")


def fetch_html(url: str) -> str:
    """Fetch HTML from a URL."""
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.text


def extract_title(soup: BeautifulSoup) -> str:
    """Extract the article title."""
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        return og_title["content"].strip()

    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)

    raise ValueError("Could not find article title.")


def extract_subtitle(soup: BeautifulSoup) -> str | None:
    """Extract the article subtitle/description."""
    og_desc = soup.find("meta", property="og:description")
    if og_desc and og_desc.get("content"):
        return og_desc["content"].strip()

    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        return meta_desc["content"].strip()

    return None


def extract_publish_date(soup: BeautifulSoup) -> str:
    """Extract publish date in YYYY-MM-DD."""
    meta_time = soup.find("meta", property="article:published_time")
    if meta_time and meta_time.get("content"):
        return _normalize_date(meta_time["content"])

    time_tag = soup.find("time")
    if time_tag and time_tag.get("datetime"):
        return _normalize_date(time_tag["datetime"])

    raise ValueError("Could not find publish date.")


def extract_authors(soup: BeautifulSoup) -> list[str]:
    """Extract a list of author names."""
    authors: list[str] = []

    for value in _extract_jsonld_values(soup, "author"):
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "name" in item:
                    authors.append(str(item["name"]).strip())
                elif isinstance(item, str):
                    authors.append(item.strip())
        elif isinstance(value, dict) and "name" in value:
            authors.append(str(value["name"]).strip())
        elif isinstance(value, str):
            authors.append(value.strip())

    if not authors:
        meta_author = soup.find("meta", property="article:author")
        if meta_author and meta_author.get("content"):
            authors.append(meta_author["content"].strip())

    return _unique_non_empty(authors)


def extract_category(soup: BeautifulSoup) -> str | None:
    """Extract the primary category/tag."""
    for value in _extract_jsonld_values(soup, "articleSection"):
        if isinstance(value, str) and value.strip():
            return value.strip()

    meta_section = soup.find("meta", property="article:section")
    if meta_section and meta_section.get("content"):
        return meta_section["content"].strip()

    tag_link = soup.select_one('a[href^="/tag/"]')
    if tag_link:
        text = tag_link.get_text(strip=True)
        if text:
            return text

    return None


def _normalize_date(value: str) -> str:
    """Normalize various date formats to YYYY-MM-DD."""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        pass

    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue

    raise ValueError(f"Unrecognized date format: {value}")


def extract_content(soup: BeautifulSoup, title: str, subtitle: str | None) -> str:
    """Extract the main article HTML content."""
    content = soup.select_one(".gh-content")
    if content is None:
        content = soup.select_one("article")
    if content is None:
        raise ValueError("Could not find article content.")

    _strip_unwanted_tags(content)
    _remove_duplicate_title(content, title)
    _remove_meta_blocks(content, subtitle)
    _remove_sections_by_heading(
        content,
        {
            "contents",
            "share this post",
            "comments",
            "also in product",
        },
    )
    _remove_all_posts_link(content)
    _make_urls_absolute(content, "https://streamlit.ghost.io/")
    return str(content)


def _strip_unwanted_tags(root: Tag) -> None:
    """Remove tags that don't belong in Markdown."""
    for tag in root.find_all(["script", "style", "noscript"]):
        tag.decompose()

    for tag in root.find_all(True):
        classes = set(tag.get("class", []))
        if classes.intersection(
            {
                "gh-article-header",
                "gh-article-meta",
                "gh-article-footer",
                "gh-post-header",
                "gh-post-meta",
                "gh-post-footer",
                "gh-post-share",
                "gh-share",
                "gh-read-next",
            }
        ):
            tag.decompose()


def _remove_duplicate_title(root: Tag, title: str) -> None:
    """Remove the duplicated H1 title within the content."""
    title_norm = _normalize_text(title)
    for h1 in root.find_all("h1"):
        if _normalize_text(h1.get_text(" ", strip=True)) == title_norm:
            h1.decompose()
            break


def _remove_meta_blocks(root: Tag, subtitle: str | None) -> None:
    """Remove author/tag metadata blocks inside the content."""
    for tag in root.find_all(["p", "div", "span"]):
        text = _normalize_text(tag.get_text(" ", strip=True))
        if text.startswith("by ") and tag.find("a", href=re.compile(r"/author/")):
            tag.decompose()
            continue
        if "posted in" in text and tag.find("a", href=re.compile(r"/tag/")):
            tag.decompose()
            continue
        if subtitle and _normalize_text(subtitle) == text:
            tag.decompose()


def _remove_sections_by_heading(root: Tag, titles: set[str]) -> None:
    """Remove sections by heading title, including following siblings."""
    for heading in list(root.find_all(["h1", "h2", "h3", "h4"])):
        heading_text = _normalize_text(heading.get_text(" ", strip=True))
        if heading_text not in titles:
            continue

        to_remove: list[Tag] = [heading]
        for sibling in heading.find_next_siblings():
            if isinstance(sibling, Tag) and sibling.name in {
                "h1",
                "h2",
                "h3",
                "h4",
            }:
                break
            if isinstance(sibling, Tag):
                to_remove.append(sibling)

        for tag in to_remove:
            tag.decompose()


def _remove_all_posts_link(root: Tag) -> None:
    """Remove the 'All posts' back link."""
    for link in root.find_all("a"):
        text = _normalize_text(link.get_text(" ", strip=True))
        if "all posts" in text:
            link.decompose()


def _make_urls_absolute(root: Tag, base_url: str) -> None:
    """Convert relative href/src URLs to absolute."""
    for tag in root.find_all(href=True):
        href = tag.get("href", "")
        if href.startswith("/"):
            tag["href"] = urljoin(base_url, href)

    for tag in root.find_all(src=True):
        src = tag.get("src", "")
        if src.startswith("/"):
            tag["src"] = urljoin(base_url, src)


def _normalize_text(text: str) -> str:
    """Normalize text for matching."""
    return " ".join(text.lower().split())


def _extract_jsonld_values(soup: BeautifulSoup, key: str) -> list[Any]:
    """Extract values for a key from JSON-LD blocks."""
    values: list[Any] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(script.string or "")
        except json.JSONDecodeError:
            continue

        values.extend(_find_jsonld_key(data, key))

    return values


def _find_jsonld_key(data: Any, key: str) -> list[Any]:
    """Recursively find values for key in JSON structures."""
    found: list[Any] = []
    if isinstance(data, dict):
        for k, v in data.items():
            if k == key:
                found.append(v)
            else:
                found.extend(_find_jsonld_key(v, key))
    elif isinstance(data, list):
        for item in data:
            found.extend(_find_jsonld_key(item, key))
    return found


def _unique_non_empty(values: list[str]) -> list[str]:
    """Return unique, non-empty values preserving order."""
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = value.strip()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        result.append(clean)
    return result

def slugify(text: str) -> str:
    """Convert text to a filesystem-safe slug."""
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    return slug.strip("-") or "article"


def render_markdown(
    title: str,
    subtitle: str | None,
    date_str: str,
    authors: list[str],
    category: str | None,
    html: str,
) -> str:
    """Render final Markdown content."""
    body = md(html, heading_style="ATX").strip()
    frontmatter = _build_frontmatter(
        title=title,
        subtitle=subtitle,
        date_str=date_str,
        authors=authors,
        category=category,
    )
    return f"{frontmatter}\n\n{body}\n"


def _build_frontmatter(
    title: str,
    subtitle: str | None,
    date_str: str,
    authors: list[str],
    category: str | None,
) -> str:
    """Build YAML frontmatter."""
    lines = [
        "---",
        f"title: {json.dumps(title)}",
    ]

    if subtitle:
        lines.append(f"subtitle: {json.dumps(subtitle)}")

    lines.append(f"date: {date_str}")

    if authors:
        lines.append("authors:")
        lines.extend([f"  - {json.dumps(author)}" for author in authors])

    if category:
        lines.append(f"category: {json.dumps(category)}")

    lines.append("---")
    return "\n".join(lines)


def write_markdown_file(title: str, date_str: str, markdown: str) -> Path:
    """Write Markdown to the articles directory."""
    output_dir = Path("articles")
    output_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{date_str}-{slugify(title)}.md"
    output_path = output_dir / filename
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def main() -> int:
    """CLI entrypoint."""
    args = parse_args()
    try:
        validate_streamlit_ghost_url(args.url)
        html = fetch_html(args.url)
        soup = BeautifulSoup(html, "html.parser")
        title = extract_title(soup)
        subtitle = extract_subtitle(soup)
        date_str = extract_publish_date(soup)
        authors = extract_authors(soup)
        category = extract_category(soup)
        content_html = extract_content(soup, title, subtitle)
        markdown = render_markdown(
            title=title,
            subtitle=subtitle,
            date_str=date_str,
            authors=authors,
            category=category,
            html=content_html,
        )
        output_path = write_markdown_file(title, date_str, markdown)
    except (requests.RequestException, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
