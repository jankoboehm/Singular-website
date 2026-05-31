#!/usr/bin/env python3
"""Extract the transferred legacy publication list into Hugo data JSON."""
from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path


TYPE_BY_SECTION = {
    "Introductory Textbooks": ("5", "introductory textbooks"),
    "Overview Articles": ("4", "overview articles"),
    "Manual, Tutorial and Reference Card for Singular": ("3", "Singular manual / tutorial"),
    "Singular Presentations": ("6", "Singular presentation"),
    "Information on Implemented Algorithms and Libraries": ("2", "publication providing implemented algorithms"),
    "Further Books Providing Singular Examples": ("1", "publication providing Singular examples"),
    "Further Publications Referring to Singular": ("0", "publication referring to Singular"),
}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def strip_tags(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment)
    return parser.text()


def content_body(path: Path) -> str:
    text = read_text(path)
    if text.startswith("---"):
        return text.split("---", 2)[2]
    return text


def first_href(fragment: str) -> str:
    match = re.search(r'href=["\']([^"\']+)["\']', fragment, re.I)
    return html.unescape(match.group(1)) if match else ""


def title_from_entry(fragment: str, text: str) -> str:
    match = re.search(r"<a\b[^>]*>(.*?)</a>", fragment, re.I | re.S)
    if match:
        title = strip_tags(match.group(1))
        if title:
            return title
    if ":" in text:
        return text.split(":", 1)[1].split(".", 1)[0].strip()
    return text[:160]


def authors_from_text(text: str) -> str:
    if ":" not in text:
        return ""
    return text.split(":", 1)[0].strip()


def year_from_text(text: str) -> str:
    years = re.findall(r"\b(19[0-9]{2}|20[0-9]{2})\b", text)
    return years[-1] if years else ""


def extract(project_dir: Path) -> list[dict]:
    source = project_dir / "content" / "stubs" / "publications-related.md"
    fragment = content_body(source)
    records: list[dict] = []
    section = ""
    token_re = re.compile(r"<h2\b[^>]*>.*?</h2>|<li\b[^>]*>.*?(?=<li\b|</ol>|<h2\b|$)", re.I | re.S)
    for match in token_re.finditer(fragment):
        token = match.group(0).strip()
        if token.lower().startswith("<h2"):
            section = strip_tags(token)
            continue
        text = strip_tags(token)
        if len(text) < 30:
            continue
        if section in {"Overview", "Search Publications"}:
            continue
        type_id, type_label = TYPE_BY_SECTION.get(section, ("0", "publication referring to Singular"))
        record_no = len(records) + 1
        records.append(
            {
                "id": f"pub-{record_no:04d}",
                "legacy_source": "index.php/publications/singular-related-publications.html",
                "legacy_category": section,
                "type": type_id,
                "type_label": type_label,
                "authors_text": authors_from_text(text),
                "title": title_from_entry(token, text),
                "journal": "",
                "volume": "",
                "pages": "",
                "year": year_from_text(text),
                "extra": "",
                "links": [{"url": first_href(token)}] if first_href(token) else [],
                "raw_legacy_html": token,
                "legacy_text": text,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Hugo project directory")
    args = parser.parse_args()
    project_dir = args.project.resolve()
    records = extract(project_dir)
    data_dir = project_dir / "data" / "publications"
    data_dir.mkdir(parents=True, exist_ok=True)
    target = data_dir / "publications.json"
    target.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(records)} publication records to {target.relative_to(project_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
