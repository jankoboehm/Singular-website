#!/usr/bin/env bash
set -euo pipefail

PUBLIC_DIR="${1:-public}"

if [[ ! -d "$PUBLIC_DIR" ]]; then
  echo "ERROR: output directory not found: $PUBLIC_DIR" >&2
  exit 1
fi

echo "Checking production output in $PUBLIC_DIR"

# The live production pages must not carry staging/protection markers.
# The old archive is excluded because it is a frozen copy and may contain legacy metadata.
if grep -RInE 'noindex|nofollow|X-Robots-Tag|preview\.singular|localhost:1313|127\.0\.0\.1|WWW-Authenticate' "$PUBLIC_DIR" \
  --exclude-dir='archive' \
  --exclude-dir='.git' \
  --exclude='*.map'; then
  echo "ERROR: found staging/protection marker in generated production pages." >&2
  exit 1
fi

if [[ -f "$PUBLIC_DIR/robots.txt" ]] && grep -InE 'Disallow:[[:space:]]*/[[:space:]]*$' "$PUBLIC_DIR/robots.txt"; then
  echo "ERROR: robots.txt blocks the entire production site." >&2
  exit 1
fi

if grep -RInE 'rel="canonical"[^>]*(preview|localhost|127\.0\.0\.1)' "$PUBLIC_DIR" --exclude-dir='archive'; then
  echo "ERROR: found bad canonical URL." >&2
  exit 1
fi

echo "Production output checks passed."
