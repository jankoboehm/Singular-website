#!/usr/bin/env python3
"""Small generated-site link checker for internal static links.

It intentionally allows compatibility/static-mount prefixes such as /old/,
/Manual/, /ftp/, and /web/ that may be served outside Hugo.
"""
from __future__ import annotations
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
import posixpath
import sys

PUBLIC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("public")
ALLOWED_EXTERNAL_PREFIXES = (
    "/old/",
    "/Manual/",
    "/ftp/",
    "/web/",
    "/publications/search/",
    "/publications/submit/",
    "/publications/view/",
)

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []
    def handle_starttag(self, tag, attrs):
        if tag not in {"a", "img", "script", "link"}:
            return
        key = "href" if tag in {"a", "link"} else "src"
        for k, v in attrs:
            if k == key and v:
                self.links.append(v)

def exists_for_path(path: str) -> bool:
    if path == "/":
        return (PUBLIC / "index.html").exists()
    candidate = PUBLIC / path.lstrip("/")
    if candidate.is_dir():
        return (candidate / "index.html").exists()
    if candidate.exists():
        return True
    if not candidate.suffix:
        return (candidate / "index.html").exists()
    return False

def url_for_html_path(html_path: Path) -> str:
    rel = html_path.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel

def resolve_link_path(html_path: Path, link_path: str) -> str:
    if link_path.startswith("/"):
        return unquote(link_path)
    current_url = url_for_html_path(html_path)
    base = current_url if current_url.endswith("/") else current_url.rsplit("/", 1)[0] + "/"
    resolved = posixpath.normpath(posixpath.join(base, link_path))
    if not resolved.startswith("/"):
        resolved = "/" + resolved
    return unquote(resolved)

errors = []
for html_path in PUBLIC.rglob("*.html"):
    if "/archive/" in html_path.as_posix():
        continue
    parser = LinkParser()
    parser.feed(html_path.read_text(encoding="utf-8", errors="ignore"))
    for link in parser.links:
        parsed = urlparse(link)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        path = resolve_link_path(html_path, parsed.path)
        if path.startswith(ALLOWED_EXTERNAL_PREFIXES):
            continue
        if not exists_for_path(path):
            errors.append(f"{html_path}: missing {path}")

if errors:
    print("Internal link check failed:")
    print("\n".join(errors[:200]))
    if len(errors) > 200:
        print(f"... {len(errors) - 200} more")
    raise SystemExit(1)

print("Internal link check passed.")
