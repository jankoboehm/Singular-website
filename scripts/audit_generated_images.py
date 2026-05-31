#!/usr/bin/env python3
"""Audit generated Hugo pages for image references that cannot be served locally.

This checks img/src, srcset entries, inline style url(...), and stylesheet
url(...) references. When a generated page has a legacy_source front-matter
entry, the report includes likely matching image references from the old page.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


LOCAL_DOMAINS = {"www.singular.uni-kl.de", "singular.uni-kl.de"}
IMAGE_EXTENSIONS = {".gif", ".ico", ".jpeg", ".jpg", ".png", ".svg", ".webp"}
URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.I)


class RefParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[dict] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {k.lower(): v for k, v in attrs if k and v}
        for attr in ("src", "poster"):
            value = attr_map.get(attr)
            if value:
                self.refs.append({"kind": f"{tag}.{attr}", "value": value})
        for attr in ("srcset", "imagesrcset"):
            value = attr_map.get(attr)
            if value:
                for candidate in parse_srcset(value):
                    self.refs.append({"kind": f"{tag}.{attr}", "value": candidate})
        style = attr_map.get("style")
        if style:
            for value in css_urls(style):
                self.refs.append({"kind": f"{tag}.style", "value": value})


def parse_srcset(value: str) -> list[str]:
    refs: list[str] = []
    for part in value.split(","):
        candidate = part.strip().split()
        if candidate:
            refs.append(candidate[0])
    return refs


def css_urls(text: str) -> list[str]:
    return [match.group(2).strip() for match in URL_RE.finditer(text) if match.group(2).strip()]


def strip_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    front = text[3:end]
    body = text[end + 4 :]
    meta: dict[str, str] = {}
    for line in front.splitlines():
        match = re.match(r'\s*([A-Za-z0-9_-]+):\s*"?(.*?)"?\s*$', line)
        if match:
            meta[match.group(1)] = match.group(2)
    return meta, body


def content_url_for_path(content_path: Path, project_dir: Path) -> str | None:
    text = content_path.read_text(encoding="utf-8", errors="replace")
    meta, _ = strip_front_matter(text)
    return meta.get("url")


def legacy_sources_by_url(project_dir: Path) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for path in (project_dir / "content").rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        meta, _ = strip_front_matter(text)
        url = meta.get("url")
        source = meta.get("legacy_source")
        if url and source:
            mapping[normalize_url_path(url)] = source
    return mapping


def normalize_url_path(path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    return path


def url_for_html_path(public_dir: Path, html_path: Path) -> str:
    rel = html_path.relative_to(public_dir).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("/index.html")]
    return "/" + rel


def page_url_keys(url: str) -> list[str]:
    keys = [normalize_url_path(url)]
    if url.endswith("/"):
        keys.append(normalize_url_path(url[:-1]))
    if url.endswith(".html"):
        keys.append(normalize_url_path(url[:-5]))
    return list(dict.fromkeys(keys))


def source_for_page(source_map: dict[str, str], public_dir: Path, html_path: Path, html_text: str) -> str | None:
    match = re.search(r'href=["\']/old/([^"\']+)["\']', html_text)
    if match:
        return unquote(match.group(1))
    url = url_for_html_path(public_dir, html_path)
    for key in page_url_keys(url):
        if key in source_map:
            return source_map[key]
    return None


def resolve_generated_ref(public_dir: Path, old_dir: Path, ftp_dir: Path, html_path: Path, value: str) -> tuple[str, Path | None, str]:
    value = html.unescape(value).strip()
    parsed = urlparse(value)
    if parsed.scheme in {"data", "mailto", "javascript"}:
        return "ignored", None, value
    if parsed.scheme in {"http", "https"}:
        if parsed.hostname in LOCAL_DOMAINS and not parsed.port:
            path = parsed.path or "/"
            return "local-domain-remote", old_path_for_site_path(old_dir, path), path
        return "external", None, value
    if parsed.scheme:
        return "external", None, value
    path = unquote(parsed.path)
    if not path:
        return "ignored", None, value
    if path.startswith("/old/"):
        return "local", old_dir / path.removeprefix("/old/"), path
    if path.startswith("/ftp/"):
        return "local", ftp_dir / path.removeprefix("/ftp/"), path
    if path.startswith("/"):
        return "local", public_dir / path.lstrip("/"), path
    base_url = url_for_html_path(public_dir, html_path)
    base = base_url if base_url.endswith("/") else base_url.rsplit("/", 1)[0] + "/"
    normalized = urljoin(base, path)
    return "local", public_dir / normalized.lstrip("/"), normalized


def old_path_for_site_path(old_dir: Path, path: str) -> Path:
    rel = path.lstrip("/")
    if rel.startswith(("templates/", "media/", "plugins/", "images_2/", "Manual/", "DEMOS/", "dox/", "forum/")):
        return old_dir / rel
    if rel.startswith("images/M_images/") or rel.startswith("images/stories/"):
        return old_dir / "images_2" / rel.removeprefix("images/")
    return old_dir / rel


def old_image_refs(old_dir: Path, legacy_source: str | None) -> list[str]:
    if not legacy_source:
        return []
    path = old_dir / legacy_source
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    parser = RefParser()
    parser.feed(text)
    refs = [entry["value"] for entry in parser.refs]
    refs.extend(css_urls(text))
    return list(dict.fromkeys(refs))


def matching_old_refs(old_refs: list[str], value: str) -> list[str]:
    basename = Path(urlparse(value).path).name
    if not basename:
        return []
    matches = [ref for ref in old_refs if Path(urlparse(ref).path).name == basename]
    return matches[:10]


def is_image_like(value: str) -> bool:
    path = urlparse(value).path.lower()
    suffix = Path(path).suffix
    return suffix in IMAGE_EXTENSIONS or "image" in value.lower()


def audit(public_dir: Path, old_dir: Path, ftp_dir: Path, project_dir: Path) -> dict:
    source_map = legacy_sources_by_url(project_dir)
    issues: list[dict] = []
    total_refs = 0
    pages_checked = 0
    for html_path in sorted(public_dir.rglob("*.html")):
        if "/old/" in html_path.as_posix():
            continue
        text = html_path.read_text(encoding="utf-8", errors="replace")
        parser = RefParser()
        parser.feed(text)
        refs = list(parser.refs)
        for css_path in []:
            pass
        if not refs:
            continue
        pages_checked += 1
        legacy_source = source_for_page(source_map, public_dir, html_path, text)
        old_refs = old_image_refs(old_dir, legacy_source)
        page_url = url_for_html_path(public_dir, html_path)
        for ref in refs:
            value = ref["value"]
            if not is_image_like(value):
                continue
            total_refs += 1
            kind, local_path, resolved = resolve_generated_ref(public_dir, old_dir, ftp_dir, html_path, value)
            if kind == "ignored":
                continue
            exists = local_path.exists() if local_path else None
            if kind == "local-domain-remote" or (kind == "local" and not exists):
                issues.append(
                    {
                        "page": page_url,
                        "html": html_path.relative_to(public_dir).as_posix(),
                        "legacy_source": legacy_source,
                        "kind": ref["kind"],
                        "value": value,
                        "resolved": resolved,
                        "candidate_path": local_path.as_posix() if local_path else None,
                        "candidate_exists": bool(exists),
                        "old_matches": matching_old_refs(old_refs, value),
                    }
                )
    return {
        "public": public_dir.as_posix(),
        "old": old_dir.as_posix(),
        "pages_checked": pages_checked,
        "image_refs_checked": total_refs,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("public", type=Path)
    parser.add_argument("--old", type=Path, default=Path("old"))
    parser.add_argument("--ftp", type=Path, default=Path("ftp"))
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()

    report = audit(args.public.resolve(), args.old.resolve(), args.ftp.resolve(), args.project.resolve())
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Checked {report['image_refs_checked']} image references on {report['pages_checked']} generated pages.")
    print(f"Image issues: {len(report['issues'])}")
    for issue in report["issues"][:50]:
        exists = "exists in old" if issue["candidate_exists"] else "missing locally"
        print(f"- {issue['page']} {issue['kind']} {issue['value']} -> {issue['candidate_path']} ({exists})")
        if issue["old_matches"]:
            print(f"  old page refs: {', '.join(issue['old_matches'][:3])}")
    return 1 if report["issues"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
