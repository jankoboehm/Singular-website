# Migration notes

## Converted pages

The following uploaded pages were converted to Hugo Markdown:

- `index.php.html` → `/`
- `news.html` → `/index.php/news.html`
- `publications.html` → `/index.php/publications.html`
- `links.html` → `/index.php/links.html`
- `jenksprize.html` → `/index.php/background/jenks-prize.html`
- `Singular-book.html` → `/index.php/singular-books.html`
- `GP_BOOK_EXAMPLES.html` → `/GP_BOOK_EXAMPLES.html`
- `history.html` → `/index.php/background/history.html` with a warning
- `zca.1.html` → `/zca.1.html`

## Static legacy material

The following folders are copied as static assets:

- `BOOK/`
- `BOOK_DL/`
- `GP_BOOK_EXAMPLES/`
- `Images/`
- `icons/`
- `ftp/`
- `gap-meeting-2012/`

The full input snapshot is also copied to `/archive/old-homepage/`.

## Additional generated placeholders

- 50 individual news detail placeholders were generated from the old news listing because the short snapshot contained the listing but not the detail pages.
- Compatibility placeholders were generated for old publication submission/search URLs and route users to the future dynamic publication database endpoints.

## Next content steps

1. Replace placeholder pages with content from the full old export.
2. Mount or copy the separately migrated documentation.
3. Decide the live publication database backend and route `/publications/search/`, `/publications/view/`, and `/publications/submit/` to it.
4. Keep `/forum/` routed to the old forum or a read-only export.
5. Review all AI-assisted Markdown before launch.
