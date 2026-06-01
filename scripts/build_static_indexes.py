#!/usr/bin/env python3
"""Build static client-side indexes for archived legacy data."""
from __future__ import annotations

import argparse
import base64
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, urlsplit


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_depth = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style"}:
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style"} and self.skip_depth:
            self.skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_depth:
            self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


TRANSPARENT_GIF = base64.b64decode("R0lGODlhAQABAIABAP///wAAACH5BAEKAAEALAAAAAABAAEAAAICRAEAOw==")
FORUM_PLACEHOLDER_GIFS = [
    "styles/Singular/imageset/announce_read.gif",
    "styles/Singular/imageset/forum_read.gif",
    "styles/Singular/imageset/forum_read_locked.gif",
    "styles/Singular/imageset/forum_unread.gif",
    "styles/Singular/imageset/icon_post_target.gif",
    "styles/Singular/imageset/icon_topic_attach.gif",
    "styles/Singular/imageset/icon_topic_latest.gif",
    "styles/Singular/imageset/sticky_read.gif",
    "styles/Singular/imageset/topic_moved.gif",
    "styles/Singular/imageset/topic_read.gif",
    "styles/Singular/imageset/topic_read_hot.gif",
    "styles/Singular/imageset/topic_read_locked.gif",
    "styles/Singular/imageset/topic_unread.gif",
    "styles/Singular/imageset/topic_unread_hot.gif",
    "styles/Singular/imageset/topic_unread_locked.gif",
    "styles/Singular/imageset/en/button_topic_new.gif",
    "styles/Singular/imageset/en/button_topic_reply.gif",
    "styles/Singular/imageset/en/icon_post_quote.gif",
    "styles/Singular/imageset/en/icon_post_report.gif",
    "styles/Singular/imageset/en/icon_user_profile.gif",
    "styles/Singular/theme/images/icon_mini_faq.gif",
    "styles/Singular/theme/images/icon_mini_login.gif",
    "styles/Singular/theme/images/icon_mini_register.gif",
    "styles/Singular/theme/images/icon_mini_search.gif",
]


FORUM_STYLESHEET = """/* Minimal static archive replacement for missing phpBB style assets. */
.postbody { font-size: 1rem; line-height: 1.55; overflow-wrap: anywhere; }
.postauthor { font-weight: 700; }
.postdetails { color: #5e6b7e; font-size: .9rem; }
.postprofile, .profile-icons, .rules, .topic-actions { display: none !important; }
.row1, .row2, .row3 { background: #fff; }
.tablebg { width: 100%; }
.gensmall { color: #5e6b7e; font-size: .9rem; }
.nav, .pagination { font-size: .95rem; }
"""


def ensure_old_placeholder_assets(old_dir: Path) -> int:
    if not old_dir.exists():
        return 0
    written = 0
    jquery = old_dir / "templates/ja_purity/js/jquery.js"
    if not jquery.exists():
        jquery.parent.mkdir(parents=True, exist_ok=True)
        jquery.write_text("// Static archive placeholder for missing legacy template script.\n", encoding="utf-8")
        written += 1
    return written


def ensure_forum_placeholder_assets(forum_dir: Path) -> int:
    if not forum_dir.exists():
        return 0
    written = 0
    stylesheet = forum_dir / "styles/Singular/theme/stylesheet.css"
    if not stylesheet.exists():
        stylesheet.parent.mkdir(parents=True, exist_ok=True)
        stylesheet.write_text(FORUM_STYLESHEET, encoding="utf-8")
        written += 1
    editor = forum_dir / "styles/Singular/template/editor.js"
    if not editor.exists():
        editor.parent.mkdir(parents=True, exist_ok=True)
        editor.write_text("// Static archive placeholder.\n", encoding="utf-8")
        written += 1
    for rel in FORUM_PLACEHOLDER_GIFS:
        path = forum_dir / rel
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(TRANSPARENT_GIF)
            written += 1
    return written


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1", "replace")


def strip_tags(fragment: str) -> str:
    parser = TextExtractor()
    parser.feed(fragment)
    return parser.text()


def local_old_url(url: str) -> str:
    split = urlsplit(url)
    if not split.scheme and split.netloc and split.hostname not in {"singular.uni-kl.de", "www.singular.uni-kl.de"}:
        return url
    if split.scheme in {"http", "https"}:
        if split.hostname not in {"singular.uni-kl.de", "www.singular.uni-kl.de"} or split.port:
            return url
        path = split.path or "/"
    elif not split.scheme and split.netloc in {"singular.uni-kl.de", "www.singular.uni-kl.de"}:
        path = split.path or "/"
    else:
        path = split.path or ""
        if not path.startswith("/"):
            return url
    if path.startswith("/ftp/"):
        rewritten = path
    elif path.startswith("/old/images/M_images/") or path.startswith("/old/images/stories/"):
        rewritten = path.replace("/old/images/", "/old/images_2/", 1)
    elif path.startswith("/old/") or path.startswith("/assets/"):
        rewritten = path
    elif path.startswith("/images/M_images/") or path.startswith("/images/stories/"):
        rewritten = "/old/images_2" + path.removeprefix("/images")
    elif is_legacy_root_path(path):
        rewritten = "/old" + path
    elif split.scheme or split.netloc:
        rewritten = "/old" + path
    else:
        return url
    if not (split.scheme or split.netloc):
        query = split.query
        fragment = split.fragment
    else:
        query = split.query
        fragment = split.fragment
    if query:
        rewritten += "?" + query
    if fragment:
        rewritten += "#" + fragment
    return rewritten


def is_legacy_root_path(path: str) -> bool:
    first = path.strip("/").split("/", 1)[0]
    legacy_dirs = {
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
    legacy_files = {
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
    return first in legacy_dirs or first in legacy_files


def static_forum_url(url: str) -> str:
    split = urlsplit(url)
    if not split.path.startswith("/old/forum/") or ".php" not in split.path or not split.query:
        return url
    query = split.query
    if "?" in query:
        query = query.split("?", 1)[0]
    rewritten = split.path + "%3F" + query
    if not rewritten.endswith(".html"):
        rewritten += ".html"
    if split.fragment:
        rewritten += "#" + split.fragment
    return rewritten


def process_old_archive_links(old_dir: Path) -> int:
    if not old_dir.exists():
        return 0
    changed = 0
    file_patterns = ("*.html", "*.htm", "*.css", "*.js")
    files: list[Path] = []
    for pattern in file_patterns:
        files.extend(old_dir.rglob(pattern))
    attr_re = re.compile(r'((?:href|src|action)=["\'])(.*?)(["\'])', re.I | re.S)
    css_url_re = re.compile(r'(url\(["\']?)(https?:\/\/(?:www\.)?singular\.uni-kl\.de\/[^)"\']+|\/\/(?:www\.)?singular\.uni-kl\.de\/[^)"\']+)(["\']?\))', re.I)

    for path in sorted(set(files)):
        text = read_text(path)

        def attr_repl(match: re.Match[str]) -> str:
            start, value, end = match.groups()
            value = local_old_url(html.unescape(value))
            value = static_forum_url(value)
            return start + value + end

        def css_repl(match: re.Match[str]) -> str:
            start, value, end = match.groups()
            return start + local_old_url(value) + end

        new_text = attr_re.sub(attr_repl, text)
        new_text = css_url_re.sub(css_repl, new_text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"<title\b[^>]*>(.*?)</title>", text, re.I | re.S)
    if match:
        title = strip_tags(match.group(1))
        title = re.sub(r"^Singular\s*(::|-|:)\s*", "", title, flags=re.I)
        if title:
            return title
    return fallback


def encoded_static_url(prefix: str, rel: str) -> str:
    return prefix.rstrip("/") + "/" + quote(rel, safe="/%=&;")


def build_forum_index(forum_dir: Path, forum_url_prefix: str) -> list[dict]:
    records: list[dict] = []
    if not forum_dir.exists():
        return records
    for path in sorted(forum_dir.rglob("*.html")):
        rel = path.relative_to(forum_dir).as_posix()
        if rel in {"search.html"}:
            continue
        text = read_text(path)
        body_text = extract_forum_text(text)
        if len(body_text) < 20:
            continue
        records.append(
            {
                "title": extract_title(text, rel),
                "url": encoded_static_url(forum_url_prefix, rel),
                "text": body_text[:2400],
            }
        )
    return records


def extract_forum_text(text: str) -> str:
    posts = re.findall(
        r'<div\b[^>]*class=["\'][^"\']*\bpostbody\b[^"\']*["\'][^>]*>(.*?)</div>',
        text,
        flags=re.I | re.S,
    )
    if posts:
        return re.sub(r"\s+", " ", " ".join(strip_tags(post) for post in posts)).strip()
    body_text = strip_tags(text)
    noise_patterns = [
        r"Read-only forum archive New discussions Search old forum",
        r"Skip to content Skip to main navigation Skip to first column Skip to second column",
        r"Search Download Try Online Online Manual Graphical Interface Get Help Report Bugs Books Teams Join Us",
        r"Login Register Forum FAQ",
    ]
    for pattern in noise_patterns:
        body_text = re.sub(pattern, " ", body_text, flags=re.I)
    return re.sub(r"\s+", " ", body_text).strip()


def process_forum_html(forum_dir: Path, forum_url_prefix: str) -> int:
    if not forum_dir.exists():
        return 0
    local_php = re.compile(r"(^|/)(?:viewtopic|viewforum|search|memberlist|ucp|posting|report|faq)\.php\?")
    archive_css = '<link rel="stylesheet" href="/assets/css/forum-archive.css">'
    archive_bar = f"""<div class="forum-archive-bar">
  <strong>Read-only forum archive</strong>
  <a href="https://github.com/Singular/Singular/discussions">New discussions</a>
  <a href="{forum_url_prefix.rstrip('/')}/search.html">Search old forum</a>
</div>"""

    def rewrite_attr(match: re.Match[str]) -> str:
        start, value, end = match.groups()
        if re.match(r"^[a-z][a-z0-9+.-]*:", value, flags=re.I) or value.startswith("#"):
            return match.group(0)
        if local_php.search(html.unescape(value)):
            value = value.replace("?", "%3F", 1)
        return f"{start}{value}{end}"

    rewritten = 0
    attr_re = re.compile(r'((?:href|src)=["\'])(.*?)(["\'])', re.I | re.S)
    for path in sorted(forum_dir.rglob("*.html")):
        text = read_text(path)
        new_text = attr_re.sub(rewrite_attr, text)
        new_text = re.sub(
            r'<img\b[^>]*\bsrc=["\']cron\.php%3F[^"\']*["\'][^>]*>',
            "",
            new_text,
            flags=re.I | re.S,
        )
        new_text = re.sub(
            r'<meta\s+name=["\']robots["\']\s+content=["\']noindex,?\s*follow["\']\s*/?>',
            '<meta name="robots" content="index,follow">',
            new_text,
            count=1,
            flags=re.I,
        )
        if archive_css not in new_text:
            new_text = re.sub(r"</head>", f"  {archive_css}\n</head>", new_text, count=1, flags=re.I)
        if "forum-archive-bar" in new_text:
            new_text = re.sub(
                r'<div class="forum-archive-bar">.*?</div>',
                archive_bar,
                new_text,
                count=1,
                flags=re.I | re.S,
            )
        else:
            new_text = re.sub(r"(<body\b[^>]*>)", r"\1\n" + archive_bar, new_text, count=1, flags=re.I)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            rewritten += 1
    return rewritten


def write_forum_search(forum_dir: Path, records: list[dict], forum_url_prefix: str) -> None:
    forum_dir.mkdir(parents=True, exist_ok=True)
    (forum_dir / "search-index.json").write_text(
        json.dumps(records, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    search_html = (
        """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Search the Singular forum archive</title>
  <style>
    body{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;color:#152033;background:#f7f9fc;line-height:1.55}
    main{max-width:980px;margin:0 auto;padding:2rem 1rem 4rem}
    a{color:#0b4e8a} .search{display:flex;gap:.75rem;flex-wrap:wrap;margin:1.25rem 0}
    input{flex:1 1 24rem;min-height:2.7rem;border:1px solid #b8c6d8;border-radius:.45rem;padding:.5rem .7rem;font:inherit}
    button{min-height:2.7rem;border:1px solid #0b4e8a;border-radius:.45rem;background:#0b4e8a;color:white;font:inherit;font-weight:700;padding:.45rem .9rem}
    .result{background:white;border:1px solid #d9e1ec;border-radius:.5rem;padding:1rem;margin:.75rem 0}
    .result h2{font-size:1rem;margin:0 0 .35rem}.result p{margin:.35rem 0 0;color:#4d5b6e}.meta{color:#5e6b7e}
  </style>
</head>
<body>
<main>
  <p><a href="/discussions/">Discussions</a> / <a href="__FORUM_URL__">Forum archive</a></p>
  <h1>Search the Singular forum archive</h1>
  <form class="search" id="search-form">
    <input id="q" type="search" autocomplete="off" autofocus placeholder="Search old forum topics and posts">
    <button type="submit">Search</button>
  </form>
  <p class="meta" id="status">Loading static index...</p>
  <div id="results"></div>
</main>
<script>
let records = [];
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const inputEl = document.getElementById("q");

function esc(value) {
  const chars = {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"};
  return String(value).replace(/[&<>"']/g, c => chars[c]);
}

function search(query) {
  const terms = query.toLowerCase().split(/\\s+/).filter(Boolean);
  if (!terms.length) {
    resultsEl.innerHTML = "";
    statusEl.textContent = `${records.length} archived pages indexed.`;
    return;
  }
  const matches = [];
  for (const item of records) {
    const haystack = `${item.title} ${item.text}`.toLowerCase();
    let score = 0;
    for (const term of terms) {
      if (!haystack.includes(term)) { score = 0; break; }
      score += item.title.toLowerCase().includes(term) ? 4 : 1;
    }
    if (score) matches.push({ item, score });
  }
  matches.sort((a, b) => b.score - a.score || a.item.title.localeCompare(b.item.title));
  const shown = matches.slice(0, 80);
  statusEl.textContent = `${matches.length} match${matches.length === 1 ? "" : "es"} found.`;
  resultsEl.innerHTML = shown.map(({ item }) => `
    <article class="result">
      <h2><a href="${item.url}">${esc(item.title)}</a></h2>
      <div class="meta">${esc(item.url)}</div>
      <p>${esc(item.text.slice(0, 360))}${item.text.length > 360 ? "..." : ""}</p>
    </article>`).join("");
}

fetch("search-index.json")
  .then(response => response.json())
  .then(data => {
    records = data;
    statusEl.textContent = `${records.length} archived pages indexed.`;
    const initial = new URLSearchParams(location.search).get("q") || "";
    inputEl.value = initial;
    search(initial);
  });

document.getElementById("search-form").addEventListener("submit", event => {
  event.preventDefault();
  const query = inputEl.value.trim();
  history.replaceState(null, "", query ? `?q=${encodeURIComponent(query)}` : location.pathname);
  search(query);
});
inputEl.addEventListener("input", () => search(inputEl.value));
</script>
</body>
</html>
"""
    ).replace("__FORUM_URL__", html.escape(forum_url_prefix.rstrip("/") + "/", quote=True))
    (forum_dir / "search.html").write_text(
        search_html,
        encoding="utf-8",
    )


def read_publication_fragment(project_dir: Path) -> str:
    path = project_dir / "content" / "stubs" / "publications-related.md"
    text = read_text(path)
    if text.startswith("---"):
        return text.split("---", 2)[2]
    return text


def build_publication_index(project_dir: Path) -> list[dict]:
    data_path = project_dir / "data" / "publications" / "publications.json"
    if data_path.exists():
        records = json.loads(read_text(data_path))
        return [
            {
                "section": item.get("legacy_category", ""),
                "title": item.get("title", ""),
                "text": item.get("legacy_text", ""),
                "href": (item.get("links") or [{}])[0].get("url", "") if isinstance(item.get("links"), list) else "",
                "html": item.get("raw_legacy_html", ""),
            }
            for item in records
        ]
    fragment = read_publication_fragment(project_dir)
    records: list[dict] = []
    section = ""
    token_re = re.compile(r"<h2\b[^>]*>.*?</h2>|<li\b[^>]*>.*?(?=<li\b|</ol>|<h2\b|$)", re.I | re.S)
    for match in token_re.finditer(fragment):
        token = match.group(0)
        if token.lower().startswith("<h2"):
            section = strip_tags(token)
            continue
        text = strip_tags(token)
        if len(text) < 30 or section.lower() in {"overview", "search publications"}:
            continue
        href = ""
        href_match = re.search(r'href=["\']([^"\']+)["\']', token, re.I)
        if href_match:
            href = html.unescape(href_match.group(1))
        records.append(
            {
                "section": section,
                "title": text[:160],
                "text": text,
                "href": href,
                "html": token,
            }
        )
    return records


def write_publication_search(static_dir: Path, records: list[dict]) -> None:
    pub_dir = static_dir / "publications"
    search_dir = pub_dir / "search"
    search_dir.mkdir(parents=True, exist_ok=True)
    (pub_dir / "publications-index.json").write_text(
        json.dumps(records, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    (search_dir / "index.html").write_text(
        """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Search Singular publications</title>
  <style>
    *{box-sizing:border-box}
    body{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;color:#152033;background:#e9f5fa;line-height:1.55}
    header{background:#006699;border-bottom:1px solid #004d73;box-shadow:0 8px 24px rgba(0,70,105,.14);z-index:5}
    .header-inner{max-width:1160px;margin:0 auto;padding:.95rem 1rem;display:flex;flex-direction:column;align-items:stretch;gap:.72rem}
    .brand{display:inline-flex;align-items:center;justify-content:flex-start;text-decoration:none;padding-left:.45rem;padding-bottom:.7rem}
    .brand img{width:205px;max-height:69px}
    nav{display:grid;gap:.05rem;border-top:1px solid rgba(255,255,255,.55);padding-top:.68rem}
    .nav-cartouche{display:grid;gap:.55rem}
    .nav-cartouche nav{border-top:0;padding-top:0;gap:.16rem}.nav-cartouche nav+nav{border-top:1px solid rgba(255,255,255,.55);padding-top:.56rem}
    nav a,.support-note a{text-decoration:none;color:#fff;font-weight:700;font-size:1.25rem;line-height:1.2;padding:.26rem .45rem;border-radius:.5rem}
    nav a:hover,.support-note a:hover{background:rgba(255,255,255,.16);color:#fff}
    .header-bottom{display:grid;gap:.46rem;margin-top:.2rem;border-top:1px solid rgba(255,255,255,.34);padding-top:.58rem;color:rgba(255,255,255,.82)}
    .header-bottom>*+*{border-top:1px solid rgba(255,255,255,.34);padding-top:.58rem}
    .legal-nav a,.support-note a,.copyright-note{padding-left:0;padding-right:0;font-size:.78rem;font-weight:400}
    .support-note,.copyright-note{margin:0;font-size:.78rem;font-weight:400;line-height:1.35}.support-note>a{display:block;padding-top:.2rem;padding-bottom:.2rem}.support-note__inner,.support-note--with-logo>a,.support-note__funding-item{display:flex;flex-direction:column;align-items:flex-start;gap:.3rem}.support-note--funding{display:grid;gap:.42rem;color:#fff;font-size:.78rem;font-weight:400}.support-note__heading{margin:0}.support-note--with-logo img{flex:0 0 auto;width:min(5.75rem,100%);max-height:2.75rem;object-fit:contain;background:#fff;border-radius:.28rem;padding:.18rem}.support-note--with-logo img[src$="symbtools-logo.svg"]{padding-left:.08rem;padding-right:.32rem}.support-note__text{display:block}.support-note--funding a:hover{background:transparent;text-decoration:underline}.support-note--plain a{display:inline;padding:0;font-size:inherit;font-weight:inherit}.support-note--plain a:hover{background:transparent;text-decoration:underline}.support-note--inline{color:#fff;font-size:.78rem;font-weight:400}.support-note--inline a{display:inline;padding:0;font-size:inherit;font-weight:inherit}.support-note--inline a:hover{background:transparent;text-decoration:underline}
    @media(min-width:980px){body{padding-left:280px}header{position:fixed;inset:.75rem auto .75rem .75rem;width:calc(280px - 1.5rem);height:calc(100vh - 1.5rem);overflow-y:auto;border:1px solid #004d73;border-radius:1.15rem;box-shadow:0 28px 62px rgba(0,32,54,.36),0 8px 18px rgba(0,32,54,.24)}.header-inner{max-width:none;min-height:100%;margin:0;padding:.8rem .85rem}.header-bottom{margin-top:auto}}
    @media(max-width:820px){.brand{justify-content:flex-start}.brand img{width:190px;max-height:64px}}
    main{max-width:1040px;margin:0 auto;padding:2rem 1rem 4rem}
    a{color:#0b4e8a}.search{display:flex;gap:.75rem;flex-wrap:wrap;margin:1.25rem 0}
    input{flex:1 1 24rem;min-height:2.7rem;border:1px solid #b8c6d8;border-radius:.45rem;padding:.5rem .7rem;font:inherit}
    button{min-height:2.7rem;border:1px solid #0b4e8a;border-radius:.45rem;background:#0b4e8a;color:white;font:inherit;font-weight:700;padding:.45rem .9rem}
    .result{background:white;border:1px solid #d9e1ec;border-radius:.5rem;padding:1rem;margin:.75rem 0;box-shadow:0 18px 44px rgba(0,32,54,.32),0 4px 12px rgba(0,32,54,.2)}
    .result h2{font-size:1rem;margin:0 0 .35rem}.result p{margin:.35rem 0 0}.meta{color:#5e6b7e}
  </style>
</head>
<body>
<header>
  <div class="header-inner">
    <a class="brand" href="/" aria-label="Singular home"><img src="/Images/singular-logo-white.svg" alt="Singular"></a>
    <div class="nav-cartouche">
      <nav class="primary-nav" aria-label="Primary navigation">
        <a href="/index.php/singular-manual.html">Manual</a>
        <a href="/index.php/singular-download.html">Download</a>
        <a href="https://github.com/Singular/Singular/discussions">Discussions</a>
        <a href="/index.php/singular-report-bugs.html">Report Issues</a>
      </nav>
      <nav class="secondary-nav" aria-label="Singular tools and resources">
        <a href="/index.php/news.html">News</a>
        <a href="/index.php/source-code.html">Contribute</a>
        <a href="/index.php/publications.html">Publications</a>
        <a href="/index.php/singular-books.html">Books</a>
        <a href="/index.php/graphical-interface.html">Jupyter Interface</a>
        <a href="https://singular-in-browser.pages.dev" target="_blank" rel="noopener">Try Online</a>
        <a href="https://www.mathematik.uni-kl.de/~boehm/singulargpispace/" target="_blank" rel="noopener">Singular/GPI-Space</a>
      </nav>
    </div>
    <div class="header-bottom">
      <p class="support-note support-note--plain">Supported by <a href="https://www.computeralgebra.de/sfb/">DFG SFB-TRR 195</a> and <a href="https://rptu.de/projekte/symbtools">Forschungsinitiative Rheinland-Pfalz</a>.</p>
      <nav class="legal-nav" aria-label="Institutional links">
        <a href="mailto:singular@rptu.de">Contact</a>
        <a href="https://rptu.de/en/imprint">Impressum</a>
        <a href="https://rptu.de/en/privacy">Datenschutzerklärung</a>
      </nav>
      <p class="copyright-note">Copyright 1990-2026 Singular group</p>
    </div>
  </div>
</header>
<main>
  <p><a href="/index.php/publications.html">Publications</a> / <a href="/index.php/publications/singular-related-publications.html">Publication database</a></p>
  <h1>Search Singular publications</h1>
  <form class="search" id="search-form">
    <input id="q" type="search" autocomplete="off" autofocus placeholder="Author, title, journal, year, keyword">
    <button type="submit">Search</button>
  </form>
  <p class="meta" id="status">Loading static index...</p>
  <div id="results"></div>
</main>
<script>
let records = [];
const statusEl = document.getElementById("status");
const resultsEl = document.getElementById("results");
const inputEl = document.getElementById("q");

function esc(value) {
  const chars = {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"};
  return String(value).replace(/[&<>"']/g, c => chars[c]);
}

function search(query) {
  const terms = query.toLowerCase().split(/\\s+/).filter(Boolean);
  if (!terms.length) {
    resultsEl.innerHTML = "";
    statusEl.textContent = `${records.length} publication entries indexed.`;
    return;
  }
  const matches = [];
  for (const item of records) {
    const haystack = `${item.section} ${item.text}`.toLowerCase();
    let score = 0;
    for (const term of terms) {
      if (!haystack.includes(term)) { score = 0; break; }
      score += item.text.toLowerCase().startsWith(term) ? 4 : 1;
    }
    if (score) matches.push({ item, score });
  }
  matches.sort((a, b) => b.score - a.score || a.item.text.localeCompare(b.item.text));
  const shown = matches.slice(0, 100);
  statusEl.textContent = `${matches.length} match${matches.length === 1 ? "" : "es"} found.`;
  resultsEl.innerHTML = shown.map(({ item }) => `
    <article class="result">
      <h2>${esc(item.section || "Publication")}</h2>
      <p>${item.html}</p>
    </article>`).join("");
}

fetch("../publications-index.json")
  .then(response => response.json())
  .then(data => {
    records = data;
    statusEl.textContent = `${records.length} publication entries indexed.`;
    const initial = new URLSearchParams(location.search).get("q") || "";
    inputEl.value = initial;
    search(initial);
  });

document.getElementById("search-form").addEventListener("submit", event => {
  event.preventDefault();
  const query = inputEl.value.trim();
  history.replaceState(null, "", query ? `?q=${encodeURIComponent(query)}` : location.pathname);
  search(query);
});
inputEl.addEventListener("input", () => search(inputEl.value));
</script>
</body>
</html>
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="Hugo project directory")
    parser.add_argument("--old-dir", type=Path, default=None, help="Copied old website tree; defaults to old")
    parser.add_argument("--forum-dir", type=Path, default=None, help="Static forum export to process; defaults to old/forum")
    parser.add_argument("--forum-url-prefix", default="/old/forum", help="Public URL prefix for the forum export")
    args = parser.parse_args()
    project_dir = args.project.resolve()
    static_dir = project_dir / "static"
    old_dir = args.old_dir.resolve() if args.old_dir else project_dir / "old"
    forum_dir = args.forum_dir.resolve() if args.forum_dir else old_dir / "forum"

    old_assets = ensure_old_placeholder_assets(old_dir)
    old_links = process_old_archive_links(old_dir)
    forum_assets = ensure_forum_placeholder_assets(forum_dir)
    rewritten = process_forum_html(forum_dir, args.forum_url_prefix)
    forum_records = build_forum_index(forum_dir, args.forum_url_prefix)
    write_forum_search(forum_dir, forum_records, args.forum_url_prefix)
    publication_records = build_publication_index(project_dir)
    write_publication_search(static_dir, publication_records)

    print(f"Old placeholder assets: wrote {old_assets} files")
    print(f"Old archive links: localized {old_links} files")
    print(f"Forum placeholder assets: wrote {forum_assets} files")
    print(f"Forum index: {len(forum_records)} pages; rewrote links in {rewritten} forum files")
    print(f"Publication index: {len(publication_records)} entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
