#!/usr/bin/env python3
"""Audit local links across Hugo output plus old/ and ftp/ mounts."""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
import posixpath


LOCAL_HOSTS = {"singular.uni-kl.de", "www.singular.uni-kl.de", "127.0.0.1", "localhost"}
SKIP_SCHEMES = {"", "mailto", "javascript", "data", "tel", "ftp"}
LEGACY_ROOT_PREFIXES = {
    "BOOK",
    "BOOK_DL",
    "DEMOS",
    "GP_BOOK_EXAMPLES",
    "Images",
    "MEGA",
    "Manual",
    "dox",
    "forum",
    "gap-meeting-2012",
    "icons",
    "images",
    "images_2",
    "media",
    "plugins",
    "singalg2026",
    "templates",
    "tmp",
    "zca",
}
LEGACY_ROOT_FILES = {
    "DynMod.ps",
    "GP_BOOK_EXAMPLES.html",
    "Hans.png",
    "Singular-book.html",
    "dep2.pdf",
    "footer.html",
    "header.html",
    "history.html",
    "index.html",
    "index.php",
    "index.php.html",
    "jenksprize.html",
    "links.html",
    "news.html",
    "print.css",
    "publications.html",
    "robots.txt",
    "search.css",
    "search.html",
    "singular.css",
    "singular.jpg",
    "tutor_resol.pdf",
    "zca.1.html",
}


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for key, value in attrs:
            if value and key.lower() in {"href", "src", "action"}:
                self.links.append((key.lower(), value))


CSS_URL_RE = re.compile(r"url\([\"']?([^\"')]+)[\"']?\)", re.I)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    for encoding in ("utf-8", "latin-1"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", "replace")


def file_url(path: Path, public_root: Path, old_root: Path, ftp_root: Path) -> str:
    if path.is_relative_to(old_root):
        rel = path.relative_to(old_root).as_posix()
        return "/old/" + quote(rel, safe="/%=&;")
    if path.is_relative_to(ftp_root):
        rel = path.relative_to(ftp_root).as_posix()
        return "/ftp/" + quote(rel, safe="/%=&;")
    rel = path.relative_to(public_root).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + quote(rel, safe="/%=&;")


def resolve_url(source_url: str, link: str) -> tuple[str, str] | None:
    if not link or link.startswith("#"):
        return None
    split = urlsplit(link)
    if split.scheme and split.scheme not in SKIP_SCHEMES:
        if split.hostname not in LOCAL_HOSTS:
            return None
    if split.scheme in SKIP_SCHEMES and split.scheme:
        return None
    if split.netloc and split.hostname not in LOCAL_HOSTS:
        return None
    if split.path.startswith("/"):
        path = split.path
    else:
        base = source_url if source_url.endswith("/") else source_url.rsplit("/", 1)[0] + "/"
        path = posixpath.normpath(posixpath.join(base, split.path))
        if not path.startswith("/"):
            path = "/" + path
    return unquote(path), split.query


def is_legacy_root_path(url_path: str) -> bool:
    first = url_path.strip("/").split("/", 1)[0]
    return first in LEGACY_ROOT_PREFIXES or first in LEGACY_ROOT_FILES


def map_url_to_file(url_path: str, public_root: Path, old_root: Path, ftp_root: Path) -> tuple[str, Path | None]:
    if url_path == "/":
        return "public", public_root / "index.html"
    if url_path.startswith("/old/"):
        return "old", old_root / url_path.removeprefix("/old/").lstrip("/")
    if url_path == "/old":
        return "old", old_root / "index.html"
    if url_path.startswith("/ftp/"):
        return "ftp", ftp_root / url_path.removeprefix("/ftp/").lstrip("/")
    if url_path == "/ftp":
        return "ftp", ftp_root
    return "public", public_root / url_path.lstrip("/")


def exists_target(path: Path) -> bool:
    if path.is_dir():
        return (path / "index.html").exists() or (path / "index.htm").exists() or True
    if path.exists():
        return True
    if not path.suffix:
        return (path / "index.html").exists() or (path / "index.htm").exists()
    return False


def classify(source_url: str, link: str, url_path: str, query: str, mount: str, target: Path | None) -> str:
    if mount == "ftp":
        return "ftp-mount"
    if query and url_path.startswith("/old/forum/") and ".php" in url_path:
        return "forum-query-not-static"
    if not url_path.startswith("/old/") and is_legacy_root_path(url_path):
        return "legacy-root-not-localized"
    if target is not None and not exists_target(target):
        return "missing-target"
    return "ok"


def collect_links(path: Path) -> list[tuple[str, str]]:
    text = read_text(path)
    links: list[tuple[str, str]] = []
    if path.suffix.lower() in {".html", ".htm"}:
        parser = LinkParser()
        parser.feed(text)
        links.extend(parser.links)
    if path.suffix.lower() in {".html", ".htm", ".css"}:
        links.extend(("css-url", match.group(1)) for match in CSS_URL_RE.finditer(text))
    return links


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--old", type=Path, default=Path("old"))
    parser.add_argument("--ftp", type=Path, default=Path("ftp"))
    parser.add_argument("--include-ftp-missing", action="store_true")
    parser.add_argument("--limit", type=int, default=30)
    args = parser.parse_args()

    public_root = args.public.resolve()
    old_root = args.old.resolve()
    ftp_root = args.ftp.resolve()
    files = list(public_root.rglob("*.html"))
    for pattern in ("*.html", "*.htm", "*.css"):
        files.extend(old_root.rglob(pattern))

    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    total_links = 0

    for path in sorted(set(files)):
        source_url = file_url(path.resolve(), public_root, old_root, ftp_root)
        for kind, link in collect_links(path):
            resolved = resolve_url(source_url, link)
            if not resolved:
                continue
            total_links += 1
            url_path, query = resolved
            mount, target = map_url_to_file(url_path, public_root, old_root, ftp_root)
            status = classify(source_url, link, url_path, query, mount, target)
            if status == "ftp-mount" and not args.include_ftp_missing:
                counts[status] += 1
                continue
            if status == "ok":
                counts[status] += 1
                continue
            counts[status] += 1
            if len(examples[status]) < args.limit:
                target_text = str(target) if target else ""
                examples[status].append(f"{source_url} -> {link} ({target_text})")

    print(f"Audited {len(set(files))} files and {total_links} local links.")
    for status, count in counts.most_common():
        print(f"{status}: {count}")
    for status, rows in examples.items():
        print(f"\n[{status}]")
        print("\n".join(rows))

    failures = counts["legacy-root-not-localized"] + counts["forum-query-not-static"] + counts["missing-target"]
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
