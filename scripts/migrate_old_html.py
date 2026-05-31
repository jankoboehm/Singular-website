#!/usr/bin/env python3
"""Migrate the local legacy Singular website into Hugo content.

This converter deliberately preserves the legacy article HTML instead of
round-tripping it through Markdown. The old site contains dense tables, forms,
and publication lists; keeping the source fragment as HTML avoids information
loss while still allowing Hugo to own the surrounding page chrome.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import urlsplit


LOCAL_DOMAINS = {"www.singular.uni-kl.de", "singular.uni-kl.de"}
OLD_PREFIXES = "BOOK|BOOK_DL|DEMOS|GP_BOOK_EXAMPLES|Manual|MEGA|dox|forum|gap-meeting-2012|icons|singalg2026|WINDOWS|zca"
OLD_ASSET_PREFIXES = "templates|media|plugins|images_2|images"
OLD_ROOT_FILES = "DynMod\\.ps|GP_BOOK_EXAMPLES\\.html|Hans\\.png|Singular-book\\.html|dep2\\.pdf|tutor_resol\\.pdf|zca\\.1\\.html"

TARGETS = {
    "index.html": "content/_index.md",
    "index.php/news.html": "content/legacy/news.md",
    "index.php/publications.html": "content/legacy/publications.md",
    "index.php/links.html": "content/legacy/links.md",
    "index.php/background/history.html": "content/legacy/history.md",
    "index.php/background/jenks-prize.html": "content/legacy/jenks-prize.md",
    "index.php/singular-books.html": "content/legacy/singular-book.md",
    "index.php/singular-download.html": "content/stubs/download.md",
    "index.php/singular-manual.html": "content/stubs/manual.md",
    "index.php/background/funding.html": "content/stubs/funding.md",
    "index.php/graphical-interface.html": "content/stubs/graphical-interface.md",
    "index.php/how-to-cite-singular.html": "content/stubs/how-to-cite.md",
    "index.php/internal.html": "content/stubs/internal.md",
    "index.php/new-libraries.html": "content/stubs/new-libraries.md",
    "index.php/publications/singular-related-publications.html": "content/stubs/publications-related.md",
    "index.php/publications/upload-publications.html": "content/stubs/publications-upload.md",
    "index.php/singular-report-bugs.html": "content/stubs/report-bugs.md",
    "index.php/source-code.html": "content/stubs/source-code.md",
    "index.php/third-party-software.html": "content/stubs/third-party-software.md",
    "index.php/third-party-software/13692.html": "content/stubs/third-party-software-detail.md",
    "GP_BOOK_EXAMPLES.html": "content/legacy/gp-book-examples.md",
    "Singular-book.html": "content/legacy/singular-book-legacy.md",
    "zca.1.html": "content/legacy/zca.md",
    "search.html": "content/legacy/search.md",
}

ALIASES = {
    "index.html": ["/index.php.html", "/index.php", "/index.html"],
    "index.php/news.html": ["/news.html"],
    "index.php/publications.html": ["/publications.html", "/publications/"],
    "index.php/links.html": ["/links.html"],
    "index.php/background/history.html": ["/history.html"],
    "index.php/background/jenks-prize.html": ["/jenksprize.html"],
    "index.php/singular-books.html": ["/singular-books.html"],
}

SECTION_LABELS = {
    "index.html": "Computer algebra system",
    "index.php/news.html": "News",
    "index.php/publications.html": "Publications",
    "index.php/publications/singular-related-publications.html": "Publication database",
    "index.php/publications/upload-publications.html": "Publication database",
    "index.php/singular-download.html": "Download",
    "index.php/singular-manual.html": "Documentation",
    "index.php/background/history.html": "Background",
    "index.php/background/funding.html": "Background",
    "index.php/background/jenks-prize.html": "Background",
}

ROOT_CANONICALS = {
    "index.php.html",
    "news.html",
    "publications.html",
    "links.html",
    "history.html",
    "jenksprize.html",
}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def strip_tags(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment)
    return parser.text()


def read_legacy_text(path: Path) -> str:
    raw = path.read_bytes()
    head = raw[:4000].decode("ascii", "ignore").lower()
    if "charset=iso-8859-1" in head or "charset=latin" in head:
        return raw.decode("latin-1", "replace")
    return raw.decode("utf-8", "replace")


def find_matching_div(text: str, start_idx: int) -> str | None:
    tag_re = re.compile(r"</?div\b[^>]*>", re.I)
    depth = 0
    for match in tag_re.finditer(text, start_idx):
        tag = match.group(0).lower()
        if tag.startswith("</div"):
            depth -= 1
            if depth == 0:
                return text[start_idx:match.end()]
        else:
            depth += 1
    return None


def extract_div_by_class(text: str, class_name: str) -> str | None:
    match = re.search(
        r'<div\b[^>]*class=["\'][^"\']*\b' + re.escape(class_name) + r'\b[^"\']*["\'][^>]*>',
        text,
        re.I,
    )
    if not match:
        return None
    block = find_matching_div(text, match.start())
    if not block:
        return None
    block = re.sub(r"^<div\b[^>]*>", "", block, count=1, flags=re.I)
    block = re.sub(r"</div>\s*$", "", block, count=1, flags=re.I)
    return block


def extract_divs_by_class(text: str, class_name: str) -> list[str]:
    pattern = re.compile(
        r'<div\b[^>]*class=["\'][^"\']*\b' + re.escape(class_name) + r'\b[^"\']*["\'][^>]*>',
        re.I,
    )
    blocks: list[str] = []
    for match in pattern.finditer(text):
        block = find_matching_div(text, match.start())
        if not block:
            continue
        block = re.sub(r"^<div\b[^>]*>", "", block, count=1, flags=re.I)
        block = re.sub(r"</div>\s*$", "", block, count=1, flags=re.I)
        if block.strip():
            blocks.append(block)
    return blocks


def extract_body(text: str) -> str:
    body = re.search(r"<body\b[^>]*>(.*?)</body>", text, re.I | re.S)
    return body.group(1) if body else text


def extract_joomla_content(text: str) -> str:
    articles = extract_divs_by_class(text, "article-content")
    if articles:
        return "\n\n".join(articles)
    match = re.search(
        r'<div\b[^>]*id=["\']ja-content["\'][^>]*>(.*?)(?:<!--\s*END:\s*CONTENT\s*-->|<div\b[^>]*id=["\']ja-col)',
        text,
        re.I | re.S,
    )
    if match:
        block = match.group(1)
        block = re.sub(r'<div\b[^>]*id=["\']ja-pathway["\'][^>]*>.*?</div>', "", block, flags=re.I | re.S)
        return block
    return extract_body(text)


def extract_generic_content(rel: str, text: str) -> str:
    if rel == "Singular-book.html":
        start = text.find('<div id="path">')
        end = text.find('<div id="footer">')
        if start >= 0 and end > start:
            return text[start:end]
    if rel == "GP_BOOK_EXAMPLES.html":
        return extract_body(text)
    if rel == "zca.1.html":
        return extract_body(text)
    return extract_joomla_content(text)


def extract_meta(text: str, name: str) -> str:
    match = re.search(
        r'<meta\b[^>]*name=["\']' + re.escape(name) + r'["\'][^>]*content=["\']([^"\']*)["\']',
        text,
        re.I,
    )
    return html.unescape(match.group(1)).strip() if match else ""


def extract_title(rel: str, text: str, fragment: str) -> str:
    for pattern in [
        r'<h2\b[^>]*class=["\']contentheading["\'][^>]*>(.*?)</h2>',
        r"<h1\b[^>]*>(.*?)</h1>",
        r"<h2\b[^>]*>(.*?)</h2>",
    ]:
        match = re.search(pattern, text, re.I | re.S)
        if match:
            title = strip_tags(match.group(1))
            if title:
                return clean_title(title)
    title = extract_meta(text, "title")
    if not title:
        match = re.search(r"<title\b[^>]*>(.*?)</title>", text, re.I | re.S)
        title = strip_tags(match.group(1)) if match else ""
    if title:
        return clean_title(title)
    return clean_title(Path(rel).stem.replace("-", " ").replace("_", " "))


def clean_title(title: str) -> str:
    title = html.unescape(re.sub(r"\s+", " ", title)).strip()
    title = re.sub(r"^Singular\s*(::|-|:)\s*", "", title, flags=re.I)
    return title or "Singular"


def localize_url(url: str) -> str:
    split = urlsplit(url)
    if not split.scheme or split.scheme not in {"http", "https"}:
        return url
    if split.hostname not in LOCAL_DOMAINS:
        return url
    if split.port:
        return url
    path = split.path or "/"
    if path in {"", "/"}:
        return "/"
    query = f"?{split.query}" if split.query else ""
    return path + query


def disable_legacy_form_actions(fragment: str) -> str:
    def repl(match: re.Match[str]) -> str:
        prefix, quote, url = match.groups()
        localized = localize_url(html.unescape(url))
        if localized == url and urlsplit(url).scheme in {"http", "https"}:
            return match.group(0)
        escaped_original = html.escape(url, quote=True)
        return f'{prefix} data-legacy-action="{escaped_original}" action="#"'

    return re.sub(r'(<form\b[^>]*?)\saction=(["\'])(.*?)\2', repl, fragment, flags=re.I | re.S)


def rewrite_static_mount_links(fragment: str) -> str:
    fragment = re.sub(
        r'((?:href|src)=["\'])(?:\.\./)+images/(M_images|stories)/',
        r"\1/old/images_2/\2/",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        r'((?:href|src)=["\'])/images/(M_images|stories)/',
        r"\1/old/images_2/\2/",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        r'((?:href|src)=["\'])images/(M_images|stories)/',
        r"\1/old/images_2/\2/",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        rf'((?:href|src)=["\'])(?:\.\./)+({OLD_PREFIXES})/',
        r"\1/old/\2/",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        rf'((?:href|src)=["\'])/({OLD_PREFIXES})/',
        r"\1/old/\2/",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        rf'((?:href|src)=["\'])({OLD_PREFIXES})/',
        r"\1/old/\2/",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        rf'((?:href|src)=["\'])/({OLD_ASSET_PREFIXES})/',
        r"\1/old/\2/",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        rf'((?:href|src)=["\'])(?:\.\./)+({OLD_ROOT_FILES})',
        r"\1/old/\2",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        rf'((?:href|src)=["\'])/({OLD_ROOT_FILES})',
        r"\1/old/\2",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(
        rf'((?:href|src)=["\'])({OLD_ROOT_FILES})',
        r"\1/old/\2",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(r'((?:href|src)=["\'])(?:\.\./)+ftp/', r"\1/ftp/", fragment, flags=re.I)
    fragment = re.sub(r'((?:href|src)=["\'])ftp/', r"\1/ftp/", fragment, flags=re.I)
    return fragment


def rewrite_static_url_value(url: str) -> str:
    url = localize_url(html.unescape(url))
    url = re.sub(r"^(?:\.\./)+images/(M_images|stories)/", r"/old/images_2/\1/", url, flags=re.I)
    url = re.sub(r"^/images/(M_images|stories)/", r"/old/images_2/\1/", url, flags=re.I)
    url = re.sub(r"^images/(M_images|stories)/", r"/old/images_2/\1/", url, flags=re.I)
    url = re.sub(rf"^(?:\.\./)+({OLD_PREFIXES})/", r"/old/\1/", url, flags=re.I)
    url = re.sub(rf"^/({OLD_PREFIXES})/", r"/old/\1/", url, flags=re.I)
    url = re.sub(rf"^({OLD_PREFIXES})/", r"/old/\1/", url, flags=re.I)
    url = re.sub(rf"^/({OLD_ASSET_PREFIXES})/", r"/old/\1/", url, flags=re.I)
    url = re.sub(rf"^(?:\.\./)+({OLD_ROOT_FILES})", r"/old/\1", url, flags=re.I)
    url = re.sub(rf"^/({OLD_ROOT_FILES})", r"/old/\1", url, flags=re.I)
    url = re.sub(rf"^({OLD_ROOT_FILES})", r"/old/\1", url, flags=re.I)
    url = re.sub(r"^(?:\.\./)+ftp/", "/ftp/", url, flags=re.I)
    url = re.sub(r"^ftp/", "/ftp/", url, flags=re.I)
    return url


def rewrite_css_urls(fragment: str) -> str:
    def repl(match: re.Match[str]) -> str:
        quote = match.group(1)
        url = rewrite_static_url_value(match.group(2))
        return f"url({quote}{url}{quote})"

    return re.sub(r"url\(\s*([\"']?)(.*?)\1\s*\)", repl, fragment, flags=re.I)


def cleanup_html(fragment: str) -> str:
    fragment = re.sub(r"<!--\s*>>>\s*Articles Anywhere\s*>>>\s*-->", "", fragment)
    fragment = re.sub(r"<!--\s*<<<\s*Articles Anywhere\s*<<<\s*-->", "", fragment)
    fragment = re.sub(
        r'<span\b[^>]*font-variant:\s*small-caps[^>]*>\s*(Singular|SINGULAR)\s*</span>',
        "Singular",
        fragment,
        flags=re.I,
    )
    fragment = re.sub(r'<div\b[^>]*id=["\']_mcePaste["\'][^>]*>.*?</div>', "", fragment, flags=re.I | re.S)
    fragment = re.sub(r"<script\b.*?</script>", "", fragment, flags=re.I | re.S)
    fragment = re.sub(
        r'\b(href|src)=("|\')(https?://(?:www\.)?singular\.uni-kl\.de[^"\']*)\2',
        lambda m: f'{m.group(1)}={m.group(2)}{localize_url(m.group(3))}{m.group(2)}',
        fragment,
        flags=re.I,
    )
    fragment = rewrite_static_mount_links(fragment)
    fragment = rewrite_css_urls(fragment)
    fragment = disable_legacy_form_actions(fragment)
    return fragment.strip()


def enrich_fragment(rel: str, fragment: str) -> str:
    if rel == "index.html":
        fragment = re.sub(
            r'<div class="article-content" style="border-style:solid;background-color:\s*lightgrey;margin:\s*15px;">',
            '<div class="article-content memorial-notice">',
            fragment,
            count=1,
            flags=re.I,
        )
        fragment = re.sub(
            r'<div class="article-content" style="border:2px solid #006599;background-color:#eef7fa;margin:\s*15px;padding:\s*12px 15px;">',
            '<div class="article-content memorial-event">',
            fragment,
            count=1,
            flags=re.I,
        )
        fragment = re.sub(
            r"^\s*(<table\b.*?</table>)",
            r'<div class="memorial-notice">\1</div>',
            fragment,
            count=1,
            flags=re.I | re.S,
        )
        fragment = re.sub(
            r'(<p style="margin:0;"><b>In honor of Hans Schönemann</b>.*?</p>)',
            r'<div class="memorial-event">\1</div>',
            fragment,
            count=1,
            flags=re.I | re.S,
        )
        fragment = re.sub(
            r'<ol[^>]*>\s*<li[^>]*>\s*(<a\b[^>]*href="index\.php/background/funding\.html"[^>]*>Funding</a>)\s*</li>\s*</ol>\s*'
            r'<ol[^>]*>\s*<li[^>]*>\s*(<a\b[^>]*href="index\.php/background/jenks-prize\.html"[^>]*>Jenks Prize</a>)\s*</li>\s*</ol>\s*'
            r'<ol[^>]*>\s*<li[^>]*>\s*(<a\b[^>]*href="index\.php/background/history\.html"[^>]*>History</a>)\s*</li>\s*</ol>',
            r'<div class="home-background-links">\1 \2 \3</div>',
            fragment,
            flags=re.I | re.S,
        )
        fragment = re.sub(r'<ol[^>]*>\s*<br\s*/?>\s*</ol>', "", fragment, flags=re.I)
        return fragment
    if rel == "index.php/singular-manual.html":
        return """
<p>The comprehensive online manual is a valuable source for becoming familiar with Singular, and browsing it can be equally useful for the beginner and the expert. The manual's frontpage with its table of contents is one possible starting point:</p>
<div class="manual-actions">
  <a class="button" href="/old/Manual/4-4/index.htm">Manual front page</a>
  <a class="button button--secondary" href="/ftp/pub/Math/Singular/doc/singular.pdf">PDF manual</a>
</div>
<p>Alternatively, check the example section, see what libraries are available, or make use of the index which in particular highlights all Singular commands:</p>
<div class="manual-actions">
  <a class="button button--secondary" href="/old/Manual/4-4/sing_931.htm">Examples</a>
  <a class="button button--secondary" href="/old/Manual/4-4/sing_1018.htm">Libraries</a>
  <a class="button button--secondary" href="/old/Manual/4-4/sing_3124.htm">Index</a>
</div>
""".strip()
    if rel == "index.php/new-libraries.html":
        return fragment.replace(
            'href="new-libraries/not-distributed-experimental-libraries.html"',
            'href="/old/index.php/new-libraries/not-distributed-experimental-libraries.html"',
        )
    if rel == "index.php/publications.html":
        actions = """
<div class="publication-actions">
  <a class="button" href="/publications/search/">Search publications</a>
  <a class="button button--secondary" href="/index.php/publications/singular-related-publications.html">Browse publications citing Singular</a>
  <a class="button button--secondary" href="/publications/submit/">Give notice of a publication</a>
</div>
"""
        intro = "The publication database lists works citing or using Singular. Use the search page for full-text filtering, browse the categorized listing, or submit a publication notice for review."
        return actions.strip() + "\n\n" + intro
    if rel == "index.php/publications/singular-related-publications.html":
        actions = """
<div class="publication-actions">
  <a class="button" href="/publications/search/">Search publications</a>
  <a class="button button--secondary" href="/publications/submit/">Give notice of a publication</a>
</div>
"""
        fragment = re.sub(r'\s*<li>\s*<a href="/publications/submit/">Upload your Singular related publications</a></li>', "", fragment, count=1, flags=re.I)
        fragment = re.sub(
            r'\s*<a name="upload"></a><p>To inform us on a publication referring to Singular, check here:</p>\s*'
            r'<ol style="list-style-type: none;">\s*'
            r'<li style="float:left;"><a class="wantedwider" href="/publications/submit/">Give Notice of a Publication</a></li>\s*'
            r'</ol>',
            "",
            fragment,
            count=1,
            flags=re.I,
        )
        fragment = re.sub(r'action="#"', 'action="/publications/search/"', fragment, count=1)
        fragment = re.sub(r'method="post"', 'method="get"', fragment, count=1, flags=re.I)
        fragment = re.sub(r"(?m)^[ \t]+(<[^>]+>)", r"\1", fragment)
        return actions.strip() + "\n\n" + fragment
    if rel == "index.php/publications/upload-publications.html":
        fragment = re.sub(
            r'(<form\b[^>]*?)\s*action=(["\']).*?\2',
            r'\1 action="/publications/submit/notice.php"',
            fragment,
            count=1,
            flags=re.I | re.S,
        )
        fragment = re.sub(r"<noscript\b.*?</noscript>", "", fragment, count=1, flags=re.I | re.S)
        fragment = fragment.replace(
            "</form>",
            '<input type="text" name="website" value="" autocomplete="off" tabindex="-1" class="honeypot" aria-hidden="true" />\n</form>',
            1,
        )
        return fragment
    return fragment


def yaml_scalar(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def front_matter(meta: dict) -> str:
    lines = ["---"]
    for key in ["title", "url", "description", "section_label"]:
        if meta.get(key):
            lines.append(f"{key}: {yaml_scalar(meta[key])}")
    aliases = meta.get("aliases") or []
    if aliases:
        lines.append("aliases:")
        for alias in aliases:
            lines.append(f"  - {yaml_scalar(alias)}")
    lines.append(f"legacy_source: {yaml_scalar(meta['source'])}")
    lines.append('migration_status: "migrated from local legacy copy"')
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def url_for_rel(rel: str) -> str:
    if rel == "index.html":
        return "/"
    return "/" + rel


def slug_for_rel(rel: str) -> str:
    slug = rel
    slug = re.sub(r"\.html?$", "", slug, flags=re.I)
    slug = slug.replace("index.php/", "")
    slug = slug.replace("/", "--")
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", slug)
    slug = slug.strip("-").lower()
    return slug or "page"


def target_for_rel(rel: str) -> str:
    if rel in TARGETS:
        return TARGETS[rel]
    if rel.startswith("index.php/news/") and rel.endswith(".html"):
        return f"content/news-details/{Path(rel).stem}.md"
    return f"content/legacy-index/{slug_for_rel(rel)}.md"


def page_candidates(source_dir: Path) -> Iterable[Path]:
    yield source_dir / "index.html"
    for path in sorted((source_dir / "index.php").rglob("*.html")):
        yield path
    for name in ["GP_BOOK_EXAMPLES.html", "Singular-book.html", "zca.1.html", "search.html"]:
        path = source_dir / name
        if path.exists():
            yield path


def write_page(source_dir: Path, project_dir: Path, path: Path) -> dict | None:
    rel = path.relative_to(source_dir).as_posix()
    if rel in ROOT_CANONICALS:
        return None
    text = read_legacy_text(path)
    fragment = enrich_fragment(rel, cleanup_html(extract_generic_content(rel, text)))
    if (
        not strip_tags(fragment)
        and "<img" not in fragment.lower()
        and "<form" not in fragment.lower()
        and "<!--" not in fragment
    ):
        return None
    title = extract_title(rel, text, fragment)
    description = extract_meta(text, "description")
    meta = {
        "title": title,
        "url": url_for_rel(rel),
        "description": description,
        "section_label": SECTION_LABELS.get(rel),
        "aliases": ALIASES.get(rel, []),
        "source": rel,
    }
    target = project_dir / target_for_rel(rel)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(front_matter(meta) + fragment + "\n", encoding="utf-8")
    return {
        "source": rel,
        "target": target.relative_to(project_dir).as_posix(),
        "url": meta["url"],
        "title": title,
        "bytes": path.stat().st_size,
    }


def write_inventory(source_dir: Path, project_dir: Path, pages: list[dict]) -> None:
    zero_byte = [
        path.relative_to(source_dir).as_posix()
        for path in sorted(source_dir.rglob("*"))
        if path.is_file() and path.stat().st_size == 0
    ]
    inventory = {
        "source": source_dir.as_posix(),
        "generated_pages": len(pages),
        "pages": pages,
        "zero_byte_files": zero_byte,
    }
    target = project_dir / "data" / "migration_inventory.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def generate(source_dir: Path, project_dir: Path) -> list[dict]:
    pages: list[dict] = []
    for path in page_candidates(source_dir):
        if path.exists():
            generated = write_page(source_dir, project_dir, path)
            if generated:
                pages.append(generated)
    write_inventory(source_dir, project_dir, pages)
    return pages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Path to the extracted old Singular web snapshot")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Hugo project directory")
    args = parser.parse_args()
    pages = generate(args.source.resolve(), args.project.resolve())
    print(f"Generated {len(pages)} Hugo content pages from {args.source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
