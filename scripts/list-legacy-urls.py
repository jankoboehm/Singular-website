#!/usr/bin/env python3
"""Print the explicit Hugo URLs and aliases from Markdown front matter."""
from __future__ import annotations
import re
from pathlib import Path

for path in sorted(Path("content").rglob("*.md")):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        continue
    fm = text.split("---", 2)[1]
    title = re.search(r'^title:\s*"(.*)"', fm, re.M)
    url = re.search(r'^url:\s*"(.*)"', fm, re.M)
    aliases = re.findall(r'^\s*-\s*"(.*)"', fm, re.M)
    if url:
        print(f"{url.group(1):45s} {path}  {title.group(1) if title else ''}")
    for alias in aliases:
        print(f"{'alias: ' + alias:45s} {path}")
