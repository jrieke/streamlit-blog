from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any

import streamlit as st

APP_ROOT = Path(__file__).parent
ARTICLES_DIR = APP_ROOT / "articles"


@dataclass(frozen=True, eq=False)
class Post:
    title: str
    subtitle: str | None
    date: str | None
    authors: list[str]
    category: str | None
    path: Path
    body: str
    frontmatter: dict[str, Any]

    @property
    def year(self) -> str | None:
        if not self.date or len(self.date) < 4:
            return None
        return self.date[:4]

    @property
    def authors_display(self) -> str:
        return ", ".join(self.authors) if self.authors else ""


def _strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def _parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    frontmatter: dict[str, Any] = {}
    current_key: str | None = None

    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not line.strip():
            continue

        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            key, raw_value = match.group(1), match.group(2)
            if raw_value == "":
                frontmatter[key] = []
                current_key = key
            else:
                frontmatter[key] = _strip_quotes(raw_value)
                current_key = None
            continue

        if current_key and line.strip().startswith("- "):
            item = _strip_quotes(line.strip()[2:])
            if isinstance(frontmatter.get(current_key), list):
                frontmatter[current_key].append(item)
            continue

    return frontmatter


def _split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    end_idx = None
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        return {}, text

    frontmatter_text = "\n".join(lines[: end_idx + 1])
    body = "\n".join(lines[end_idx + 1 :]).lstrip("\n")
    return _parse_frontmatter(frontmatter_text), body


def _post_from_file(path: Path) -> Post | None:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return None

    fm, body = _split_frontmatter(content)
    title = str(fm.get("title") or path.stem)
    subtitle = fm.get("subtitle")
    date = fm.get("date")
    authors = fm.get("authors") or []
    if isinstance(authors, str):
        authors = [authors]
    category = fm.get("category")

    return Post(
        title=title,
        subtitle=subtitle,
        date=date,
        authors=list(authors),
        category=category,
        path=path,
        body=body,
        frontmatter=fm,
    )


@st.cache_data(show_spinner=False)
def load_posts(version: str) -> list[Post]:
    posts: list[Post] = []
    for path in sorted(ARTICLES_DIR.glob("*.md")):
        post = _post_from_file(path)
        if post:
            posts.append(post)
    return posts


def _sort_posts(posts: list[Post]) -> list[Post]:
    return sorted(posts, key=lambda p: p.date or "", reverse=True)


def _render_frontmatter(post: Post) -> None:
    st.caption(f"File: {post.path.as_posix()}")
    
    st.title(post.title)
    if post.subtitle:
        st.caption(post.subtitle)

    date_value = post.date or "Unknown date"
    category_value = post.category or "Uncategorized"

    with st.container(horizontal=True):
        st.badge(date_value, icon=":material/event:", color="gray")
        st.badge(category_value, icon=":material/label:", color="blue")
        for author in post.authors:
            st.badge(author, icon=":material/person:", color="green")

    extra_items: list[dict[str, str]] = []
    for key, value in post.frontmatter.items():
        if key in {"title", "subtitle", "date", "authors", "category"}:
            continue
        if isinstance(value, list):
            rendered = ", ".join(str(item) for item in value)
        else:
            rendered = str(value)
        extra_items.append({"Key": key, "Value": rendered})

    if extra_items:
        st.markdown("")
        with st.expander("More frontmatter"):
            st.dataframe(
                extra_items,
                column_config={
                    "Key": st.column_config.TextColumn("Key"),
                    "Value": st.column_config.TextColumn("Value"),
                },
                hide_index=True,
                use_container_width=True,
            )



def main() -> None:
    st.set_page_config(
        page_title="Streamlit Blog Viewer",
        page_icon="🗂️",
    )

    st.title("Streamlit blog viewer")
    st.caption("Pick a post and read it with frontmatter details.")

    posts = _sort_posts(load_posts("v2"))

    def label(post: Post) -> str:
        date_prefix = post.date or "Unknown date"
        return f"{date_prefix} — {post.title}"

    selected = st.selectbox(
        "Post",
        options=posts,
        format_func=label,
        index=0,
        label_visibility="visible",
        bind="query-params",
    )

    _render_frontmatter(selected)
    st.markdown(selected.body)


if __name__ == "__main__":
    main()
