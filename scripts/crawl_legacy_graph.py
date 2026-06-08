#!/usr/bin/env python3
"""Crawl the local legacy Singular site graph and compare converted pages.

The crawler starts at singular-www/index.html, follows local page links that
belong to the old Joomla-style site, and treats manuals, demos, forum, doxygen,
book examples, and ftp as preserved archive leaves.
"""
from __future__ import annotations

import argparse
import collections
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import migrate_old_html as migrate  # noqa: E402


LOCAL_DOMAINS = migrate.LOCAL_DOMAINS

ROOT_ALIASES = {
    "": "index.html",
    "index.php.html": "index.html",
    "download.html": "index.php/singular-download.html",
    "full package": "full&",
    "impressum.html": "index.php/impressum.html",
    "internal/": "index.php/internal.html",
    "news.html": "index.php/news.html",
    "publications.html": "index.php/publications.html",
    "links.html": "index.php/links.html",
    "history.html": "index.php/background/history.html",
    "jenksprize.html": "index.php/background/jenks-prize.html",
    "singular-books.html": "index.php/singular-books.html",
}

CONVERTED_ROOT_FILES = {
    "index.html",
    "GP_BOOK_EXAMPLES.html",
    "Singular-book.html",
    "zca.1.html",
    "search.html",
}

ARCHIVE_PREFIXES = (
    "BOOK/",
    "BOOK_DL/",
    "DEMOS/",
    "GP_BOOK_EXAMPLES/",
    "MEGA/",
    "Manual/",
    "dox/",
    "forum/",
    "gap-meeting-2012/",
    "icons/",
    "images/",
    "images_2/",
    "media/",
    "plugins/",
    "singalg2026/",
    "templates/",
    "tmp/",
    "WINDOWS/",
    "zca/",
)

ARCHIVE_ROOT_FILES = {
    "DynMod.ps",
    "Hans.png",
    "dep2.pdf",
    "forum.1.html",
    "tutor_resol.pdf",
    "singular.css",
    "singular.jpg",
}

IGNORED_SCHEMES = {"mailto", "javascript", "tel", "data"}


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if key and key.lower() in {"href", "src", "action"} and value:
                self.links.append((key.lower(), value))


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def strip_front_matter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            return text[end + 4 :]
    return text


def text_from_html(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment)
    return parser.text()


def tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9_À-ÖØ-öø-ÿ]{2,}", text.lower())


def token_coverage(old_text: str, new_text: str) -> float:
    old_counts = collections.Counter(tokens(old_text))
    if not old_counts:
        return 1.0
    new_counts = collections.Counter(tokens(new_text))
    kept = sum(min(count, new_counts[token]) for token, count in old_counts.items())
    return kept / sum(old_counts.values())


def extract_links(fragment: str) -> set[str]:
    parser = LinkExtractor()
    parser.feed(fragment)
    return {html.unescape(value).strip() for _, value in parser.links if value.strip()}


def normalize_raw_link(raw: str, base_rel: str) -> tuple[str, str | None]:
    value = html.unescape(raw).strip()
    if not value or value.startswith("#"):
        return "ignored", None

    split = urlsplit(value)
    if split.scheme.lower() in IGNORED_SCHEMES:
        return "external", value
    if split.scheme.lower() == "ftp":
        if split.path.startswith(("/pub/Math/Singular/", "/repo/")):
            return "ftp", "/ftp" + split.path
        return "external", value
    if split.scheme.lower() in {"http", "https"}:
        if split.hostname in LOCAL_DOMAINS and not split.port:
            value = split.path or "/"
            if split.query:
                value += "?" + split.query
        else:
            return "external", value
    elif value.startswith("//"):
        return "external", value

    if value.startswith("/"):
        joined = value
    else:
        joined = urljoin("/" + base_rel, value)

    joined = joined.split("#", 1)[0]
    if joined.startswith("/"):
        joined = joined[1:]
    joined = re.sub(r"/+", "/", joined)
    return "local", joined


def existing_rel(source_dir: Path, rel: str) -> str | None:
    candidates = [rel]
    split = urlsplit(rel)
    if split.query:
        candidates.append(split.path + "?" + split.query)
    if rel.endswith("/"):
        candidates.append(rel + "index.html")
    for candidate in candidates:
        if candidate in ROOT_ALIASES:
            return ROOT_ALIASES[candidate]
        if (source_dir / candidate).is_file():
            return candidate
    return None


def canonical_rel(source_dir: Path, rel: str) -> str:
    rel = rel.lstrip("./")
    if rel in ROOT_ALIASES:
        return ROOT_ALIASES[rel]
    existing = existing_rel(source_dir, rel)
    if existing:
        return ROOT_ALIASES.get(existing, existing)
    return rel


def hugo_content_urls(project_dir: Path) -> set[str]:
    urls: set[str] = set()
    for path in (project_dir / "content").rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        end = text.find("\n---", 3)
        if end < 0:
            continue
        front = text[3:end]
        for match in re.finditer(r'^\s*(?:url|\-\s*)\s*:\s*"([^"]+)"\s*$', front, re.M):
            url = match.group(1).lstrip("/")
            if url:
                urls.add(url)
    return urls


def is_converted(rel: str) -> bool:
    if rel in CONVERTED_ROOT_FILES:
        return True
    return rel.startswith("index.php/") and rel.endswith(".html")


def is_archive(rel: str) -> bool:
    return rel.startswith(ARCHIVE_PREFIXES) or rel in ARCHIVE_ROOT_FILES


def is_asset(source_dir: Path, rel: str) -> bool:
    if rel.startswith("Images/"):
        return (source_dir / rel).is_file()
    if Path(rel).suffix.lower() in {".css", ".gif", ".ico", ".jpg", ".jpeg", ".pdf", ".png"}:
        return (source_dir / rel).is_file()
    return False


def classify(source_dir: Path, project_urls: set[str], raw: str, base_rel: str) -> tuple[str, str | None]:
    kind, value = normalize_raw_link(raw, base_rel)
    if kind != "local":
        return kind, value
    assert value is not None
    rel = canonical_rel(source_dir, value)
    if "%3F" in rel or rel.startswith("index.php?format=feed"):
        return "dynamic", rel
    if rel.startswith("cgi-bin/") or rel.startswith("index.php/component/user/"):
        return "dynamic", rel
    if is_converted(rel):
        if (source_dir / rel).is_file():
            return "converted", rel
        if rel in project_urls:
            return "generated-only", rel
        return "missing-local", rel
    if rel in project_urls:
        return "generated-only", rel
    if rel.startswith("ftp/"):
        return "ftp", "/" + rel
    if is_archive(rel):
        return "archive", rel
    if is_asset(source_dir, rel):
        return "asset", rel
    if "?" in rel:
        return "dynamic", rel
    if (source_dir / rel).is_file():
        return "unconverted-local", rel
    return "missing-local", rel


def expected_fragment(source_dir: Path, rel: str) -> str:
    text = migrate.read_legacy_text(source_dir / rel)
    fragment = migrate.extract_generic_content(rel, text)
    fragment = migrate.cleanup_html(fragment)
    return migrate.enrich_fragment(rel, fragment)


def compare_page(source_dir: Path, project_dir: Path, rel: str) -> dict:
    target = project_dir / migrate.target_for_rel(rel)
    result: dict = {
        "old": rel,
        "new_url": migrate.url_for_rel(rel),
        "target": target.relative_to(project_dir).as_posix(),
        "target_exists": target.exists(),
    }
    if not target.exists():
        result["status"] = "missing-target"
        return result

    expected = expected_fragment(source_dir, rel)
    actual = strip_front_matter(target.read_text(encoding="utf-8", errors="replace"))
    coverage = token_coverage(text_from_html(expected), text_from_html(actual))
    expected_links = extract_links(expected)
    actual_links = extract_links(actual)
    missing_links = sorted(expected_links - actual_links)
    result.update(
        {
            "status": "ok" if coverage >= 0.985 and not missing_links else "content-diff",
            "text_coverage": round(coverage, 4),
            "expected_links": len(expected_links),
            "missing_links": missing_links[:50],
            "missing_links_total": len(missing_links),
        }
    )
    return result


def crawl(source_dir: Path, project_dir: Path) -> tuple[set[str], dict[str, set[str]], dict[str, set[str]], dict[str, dict[str, set[str]]]]:
    queue = collections.deque(["index.html"])
    seen: set[str] = set()
    edges: dict[str, set[str]] = collections.defaultdict(set)
    buckets: dict[str, set[str]] = collections.defaultdict(set)
    refs: dict[str, dict[str, set[str]]] = collections.defaultdict(lambda: collections.defaultdict(set))
    project_urls = hugo_content_urls(project_dir)

    while queue:
        rel = queue.popleft()
        if rel in seen:
            continue
        seen.add(rel)
        try:
            text = migrate.read_legacy_text(source_dir / rel)
        except FileNotFoundError:
            buckets["missing-local"].add(rel)
            continue
        parser = LinkExtractor()
        parser.feed(text)
        for _, raw in parser.links:
            kind, target = classify(source_dir, project_urls, raw, rel)
            if not target:
                continue
            buckets[kind].add(target)
            refs[kind][target].add(rel)
            if kind == "converted":
                edges[rel].add(target)
                if target not in seen:
                    queue.append(target)
    return seen, edges, buckets, refs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Path to the local old Singular web snapshot")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Hugo project directory")
    parser.add_argument("--json", type=Path, default=None, help="Optional JSON report path")
    args = parser.parse_args()

    source_dir = args.source.resolve()
    project_dir = args.project.resolve()
    seen, edges, buckets, refs = crawl(source_dir, project_dir)
    comparisons = [compare_page(source_dir, project_dir, rel) for rel in sorted(seen)]
    issues = [item for item in comparisons if item["status"] != "ok"]

    report = {
        "root": "index.html",
        "converted_nodes_crawled": len(seen),
        "converted_edges": sum(len(values) for values in edges.values()),
        "archive_links": len(buckets.get("archive", set())),
        "asset_links": len(buckets.get("asset", set())),
        "ftp_links": len(buckets.get("ftp", set())),
        "external_links": len(buckets.get("external", set())),
        "dynamic_links": sorted(buckets.get("dynamic", set())),
        "generated_only_links": sorted(buckets.get("generated-only", set())),
        "unconverted_local_links": sorted(buckets.get("unconverted-local", set())),
        "missing_local_links": sorted(buckets.get("missing-local", set())),
        "refs": {
            kind: {target: sorted(sources) for target, sources in targets.items()}
            for kind, targets in refs.items()
            if kind in {"missing-local", "unconverted-local", "generated-only", "dynamic"}
        },
        "content_issues": issues,
        "comparisons": comparisons,
    }

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Crawled {report['converted_nodes_crawled']} converted old-site nodes from {source_dir / 'index.html'}")
    print(f"Converted graph edges: {report['converted_edges']}")
    print(f"Archive leaves: {report['archive_links']}  Assets: {report['asset_links']}  FTP leaves: {report['ftp_links']}  External links: {report['external_links']}")
    print(f"Generated-only compatibility links: {len(report['generated_only_links'])}")
    print(f"Unconverted local links: {len(report['unconverted_local_links'])}")
    print(f"Missing local links: {len(report['missing_local_links'])}")
    print(f"Content issues: {len(issues)}")
    if issues:
        for issue in issues[:20]:
            print(f"- {issue['old']}: {issue['status']} coverage={issue.get('text_coverage')}")
    return 1 if issues or report["missing_local_links"] or report["unconverted_local_links"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
