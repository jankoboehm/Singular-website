<?php
declare(strict_types=1);

$publicationTypes = [
    '0' => 'publication referring to Singular',
    '1' => 'publication providing Singular examples',
    '2' => 'publication providing implemented algorithms',
    '3' => 'Singular manual / tutorial',
    '4' => 'overview articles',
    '5' => 'introductory textbooks',
    '6' => 'Singular presentation',
];

function field(string $name, int $maxLength = 2000): string
{
    $value = $_POST[$name] ?? '';
    if (is_array($value)) {
        $value = '';
    }
    $value = trim((string) $value);
    $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $value) ?? '';
    if (text_length($value) > $maxLength) {
        $value = text_substr($value, 0, $maxLength);
    }
    return $value;
}

function text_length(string $value): int
{
    return function_exists('mb_strlen') ? mb_strlen($value, 'UTF-8') : strlen($value);
}

function text_substr(string $value, int $start, int $length): string
{
    return function_exists('mb_substr') ? mb_substr($value, $start, $length, 'UTF-8') : substr($value, $start, $length);
}

function render_page(string $title, string $body, int $status = 200): never
{
    http_response_code($status);
    header('Content-Type: text/html; charset=utf-8');
    echo '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">';
    echo '<title>' . htmlspecialchars($title, ENT_QUOTES, 'UTF-8') . '</title>';
    echo '<style>body{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;margin:0;color:#152033;background:#f7f9fc;line-height:1.55}main{max-width:820px;margin:0 auto;padding:2rem 1rem 4rem}a{color:#0b4e8a}.box{background:white;border:1px solid #d9e1ec;border-radius:.5rem;padding:1rem}</style>';
    echo '</head><body><main><p><a href="/index.php/publications.html">Publications</a> / <a href="/publications/submit/">Give notice</a></p><div class="box">';
    echo $body;
    echo '</div></main></body></html>';
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: /publications/submit/', true, 303);
    exit;
}

if (field('website') !== '') {
    render_page('Publication notice received', '<h1>Thank you</h1><p>Your publication notice has been received.</p>');
}

$authors = [];
for ($i = 1; $i <= 6; $i++) {
    $first = field("author{$i}firstname", 200);
    $surname = field("author{$i}surname", 200);
    if ($first !== '' || $surname !== '') {
        $authors[] = trim($first . ' ' . $surname);
    }
}

$title = field('title', 1000);
$type = field('type', 2);
$link = field('link', 1000);

$errors = [];
if ($title === '') {
    $errors[] = 'Please provide a publication title.';
}
if (!$authors) {
    $errors[] = 'Please provide at least one author.';
}
if ($link !== '' && filter_var($link, FILTER_VALIDATE_URL) === false) {
    $errors[] = 'Please provide a valid link URL or leave the link field empty.';
}
if (!array_key_exists($type, $publicationTypes)) {
    $errors[] = 'Please choose a valid publication type.';
}
if ($errors) {
    $items = '';
    foreach ($errors as $error) {
        $items .= '<li>' . htmlspecialchars($error, ENT_QUOTES, 'UTF-8') . '</li>';
    }
    render_page('Publication notice problem', '<h1>Publication notice problem</h1><ul>' . $items . '</ul><p><a href="/publications/submit/">Return to the form</a></p>', 422);
}

$notice = [
    'submitted_at' => gmdate('c'),
    'authors' => $authors,
    'title' => $title,
    'journal' => field('journal', 1000),
    'volume' => field('volume', 200),
    'pages' => field('pages', 200),
    'year' => field('year', 80),
    'extra' => field('extra', 1000),
    'link' => $link,
    'type' => $type,
    'type_label' => $publicationTypes[$type],
    'remote_addr_hash' => hash('sha256', (string) ($_SERVER['REMOTE_ADDR'] ?? '')),
    'user_agent' => field_from_server('HTTP_USER_AGENT', 500),
];

$json = json_encode($notice, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
if ($json === false) {
    render_page('Publication notice problem', '<h1>Publication notice problem</h1><p>The submission could not be encoded.</p>', 500);
}

$stored = false;
$spoolDir = getenv('SINGULAR_PUBLICATION_NOTICE_DIR');
if ($spoolDir === false || $spoolDir === '') {
    $spoolDir = sys_get_temp_dir() . '/singular-publication-notices';
}
if (!is_dir($spoolDir)) {
    @mkdir($spoolDir, 0770, true);
}
if (is_dir($spoolDir) && is_writable($spoolDir)) {
    $file = rtrim($spoolDir, DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'publication-notices.jsonl';
    $stored = @file_put_contents($file, $json . PHP_EOL, FILE_APPEND | LOCK_EX) !== false;
}

$mailSent = false;
$to = getenv('SINGULAR_PUBLICATION_NOTICE_EMAIL');
if ($to === false || $to === '') {
    $to = 'singular@rptu.de';
}
if (filter_var($to, FILTER_VALIDATE_EMAIL) !== false) {
    $subject = 'Singular publication notice: ' . text_substr($title, 0, 120);
    $body = "A new Singular publication notice was submitted.\n\n" . json_encode($notice, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) . "\n";
    $headers = 'From: singular-publications@' . ($_SERVER['SERVER_NAME'] ?? 'localhost');
    $mailSent = @mail($to, $subject, $body, $headers);
}

if (!$stored && !$mailSent) {
    render_page(
        'Publication notice problem',
        '<h1>Publication notice problem</h1><p>The notice was valid, but the server could not store or mail it. Please configure <code>SINGULAR_PUBLICATION_NOTICE_DIR</code> or <code>SINGULAR_PUBLICATION_NOTICE_EMAIL</code>.</p>',
        500
    );
}

render_page(
    'Publication notice received',
    '<h1>Thank you</h1><p>Your publication notice has been received and can be reviewed before it is added to the publication database.</p><p><a href="/index.php/publications/singular-related-publications.html">Return to publications</a></p>'
);

function field_from_server(string $name, int $maxLength): string
{
    $value = $_SERVER[$name] ?? '';
    if (is_array($value)) {
        return '';
    }
    $value = trim((string) $value);
    if (text_length($value) > $maxLength) {
        return text_substr($value, 0, $maxLength);
    }
    return $value;
}
