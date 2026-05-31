#!/usr/bin/env python3
"""Serve Hugo output together with root-level old/ and ftp/ mounts."""
from __future__ import annotations

import argparse
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit


class IntegratedPreviewHandler(SimpleHTTPRequestHandler):
    public_root: Path
    old_root: Path
    ftp_root: Path

    def translate_path(self, path: str) -> str:
        raw_path = unquote(urlsplit(path).path)
        root = self.public_root
        rel = raw_path.lstrip("/")

        if raw_path == "/old" or raw_path.startswith("/old/"):
            root = self.old_root
            rel = raw_path.removeprefix("/old").lstrip("/")
        elif raw_path == "/ftp" or raw_path.startswith("/ftp/"):
            root = self.ftp_root
            rel = raw_path.removeprefix("/ftp").lstrip("/")

        parts = [part for part in rel.split("/") if part not in {"", ".", ".."}]
        return str(root.joinpath(*parts))

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt: str, *args: object) -> None:
        print("%s - %s" % (self.log_date_time_string(), fmt % args), flush=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8090)
    parser.add_argument("--public", type=Path, default=Path("public"))
    parser.add_argument("--old", type=Path, default=Path("old"))
    parser.add_argument("--ftp", type=Path, default=Path("ftp"))
    args = parser.parse_args()

    handler = IntegratedPreviewHandler
    handler.public_root = args.public.resolve()
    handler.old_root = args.old.resolve()
    handler.ftp_root = args.ftp.resolve()

    for label, root in [("public", handler.public_root), ("old", handler.old_root), ("ftp", handler.ftp_root)]:
        if not root.exists():
            raise SystemExit(f"{label} root does not exist: {root}")

    os.chdir(handler.public_root)
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Serving integrated preview at http://{args.host}:{args.port}/", flush=True)
    print(f"  /     -> {handler.public_root}", flush=True)
    print(f"  /old/ -> {handler.old_root}", flush=True)
    print(f"  /ftp/ -> {handler.ftp_root}", flush=True)
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
