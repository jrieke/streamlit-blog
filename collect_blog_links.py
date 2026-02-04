from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://streamlit.ghost.io/"
PAGE_COUNT = 22
OUTPUT_PATH = Path("article_links.txt")


def fetch_page(url: str) -> str:
    """Fetch HTML from a URL."""
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.text


def extract_article_links(html: str) -> list[str]:
    """Extract article links from a page."""
    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if href.startswith("/author/") or href.startswith("/tag/"):
            continue
        if href.startswith("https://streamlit.ghost.io/"):
            full = href
        elif href.startswith("/"):
            full = urljoin(BASE_URL, href)
        else:
            continue

        if re.match(r"^https://streamlit\.ghost\.io/[a-z0-9-_]+/?$", full):
            if full.rstrip("/") != BASE_URL.rstrip("/"):
                links.append(full.rstrip("/"))
    return _unique_preserve_order(links)


def _unique_preserve_order(items: list[str]) -> list[str]:
    """Return unique items preserving order."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def main() -> int:
    """Collect blog links across all pages."""
    all_links: list[str] = []
    mismatches: list[str] = []
    for page in range(1, PAGE_COUNT + 1):
        url = BASE_URL if page == 1 else f"{BASE_URL}page/{page}/"
        html = fetch_page(url)
        links = extract_article_links(html)

        if page == 1:
            expected = 11
        elif page == PAGE_COUNT:
            expected = 3
        else:
            expected = 10
        if len(links) != expected:
            mismatches.append(
                f"page {page}: {len(links)} links (expected {expected})"
            )

        all_links.extend(links)

    OUTPUT_PATH.write_text("\n".join(all_links) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH} with {len(all_links)} links.")
    if mismatches:
        print("Link count mismatches:", file=sys.stderr)
        for entry in mismatches:
            print(f"- {entry}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
