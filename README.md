# Singular Hugo website

This repository is a Hugo-based conversion of the local `singular-www` copy.

The goal is to make the editable website transparent and Git-managed while keeping legacy URL paths wherever possible. Generated or bulky archives such as the manual and forum live in the root-level `old/` tree instead of becoming hand-edited Hugo content.

## What is included

- Hugo source for the new static homepage.
- Hugo content generated from the legacy Joomla article pages.
- A migration inventory in `data/migration_inventory.json`.
- A transferred publication database in `data/publications/publications.json`, with the raw legacy HTML preserved on each record.
- A working publication notice form at `/publications/submit/`.
- A copied compatibility tree in `old/`, served under `/old/`.
- A static-searchable forum archive in `old/forum/`.
- An empty root-level `ftp/` mount point. The real FTP archive should stay root-level and must not be copied into `old/`.
- Hugo-owned static assets in `static/`, limited to the new site assets, publication search/submit files, and shared fragments.
- Shared header/footer fragments in `static/_shared/` for a dynamic publication database frontend.
- GitHub Actions workflows for checking and manually deploying the production build.
- Production safety checks to fail the build if accidental `noindex`, preview-domain, localhost, or similar protection markers appear in generated public pages.

## Local preview

Install Hugo and run:

```bash
hugo server --disableFastRender
```

Then open the local URL printed by Hugo.

A production-like local build is:

```bash
hugo --environment production --minify --cleanDestinationDir
scripts/check-production-output.sh public
scripts/check-output-links.py public
python3 -m http.server --directory public 8080
```

Then browse:

```text
http://localhost:8080/
```

This serves the Hugo output only. To preview the complete production layout locally, serve the generated `public/` directory together with the root-level `old/` tree at `/old/` and the real FTP archive or empty `ftp/` mount point at `/ftp/`.

## URL policy

The important migrated pages use explicit Hugo front matter URLs, for example:

```yaml
url: "/index.php/news.html"
aliases:
  - "/news.html"
```

This means the canonical generated page is the legacy-style URL. Some simple aliases are generated to help with old static-export filenames.

To inspect the URL map:

```bash
scripts/list-legacy-urls.py
```

## Old Site Integration

The old source tree is copied into the Hugo project as:

```text
old/
```

Serve that directory under:

```text
/old/
```

New Hugo pages can then link to generated legacy assets through paths such as:

```text
/old/Manual/4-4/
/old/forum/
/old/DEMOS/
/old/dox/
```

Keep the FTP/download archive at root level, outside `old/`:

```text
/ftp/
```

This preserves old download URLs and external references. Hugo owns the editable website pages and structured publication data; `old/` owns the legacy site, manuals, forum archive, generated docs, demos, books, and historical assets. The FTP archive remains a separate root-level service.

## Publication database integration

The Hugo page at:

```text
/index.php/publications.html
```

contains entry points for publication search and submission. The transferred database is stored in:

```text
data/publications/publications.json
```

Each transferred record preserves `raw_legacy_html`, so the old publication database can be audited and rendered without information loss.

Search is generated as a static client-side page at:

```text
/publications/search/
```

New publication notices post to `/publications/submit/notice.php`. Configure the production server so that PHP runs for that handler, or replace it with an equivalent CGI/application endpoint. The handler stores JSON Lines in `SINGULAR_PUBLICATION_NOTICE_DIR` and can also mail notices to `SINGULAR_PUBLICATION_NOTICE_EMAIL`.

## Forum integration

New discussions go to GitHub Discussions. Keep `/old/forum/` routed to the copied read-only forum archive. `scripts/build_static_indexes.py` processes that archive so it looks less like a broken live phpBB instance: it rewrites query-style links to static filenames, injects an archive bar and stylesheet, hides login/posting controls, and builds `search.html` plus `search-index.json`.

## Regenerating migrated Markdown from legacy HTML

The migration scripts use the Python standard library:

```bash
python3 scripts/migrate_old_html.py /path/to/singular-www --project .
python3 scripts/extract_publications.py --project .
python3 scripts/build_static_indexes.py --project .
```

The conversion preserves legacy article HTML inside Hugo pages to avoid losing tables, forms, and publication details.

## Known caveats

- The old source tree remains a migration input and should not be deleted as part of this work.
- `old/` is large because it contains the manual, forum archive, generated docs, demos, books, and historical assets.
- `ftp/` is intentionally empty in this tree; wire `/ftp/` to the real root-level FTP archive in production.
- The PHP publication notice handler cannot be linted locally unless PHP is installed.

## GitHub Actions

`check.yml` refreshes the static indexes, builds the site, runs safety/link checks, and uploads the generated `public/` tree as a downloadable workflow artifact named `singular-site`. It runs on pushes to `master`, pull requests targeting `master`, and manual workflow dispatch. The artifact is retained for 30 days.

There is intentionally no workflow that logs into the production server. To publish, download the `singular-site` artifact from the GitHub Actions run, unpack it, and upload the contents to the webserver location used for the current Hugo site.

The server keeps the large historical trees outside the Hugo upload and maps `/old/`, `/ftp/`, and compatibility manual paths to those existing locations. The artifact intentionally does not contain the old website archive, the forum archive, manuals, or FTP tree.
