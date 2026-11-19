<?php
// The latest news of one team as an HTML list you can drop into a page.
//
// Usage:
//   export GOALISE_TOKEN=your_api_token
//   php news.php 404        # 404 = Cagliari
//
// Needs PHP 7.4+ with allow_url_fopen enabled and nothing else.

$teamId = $argv[1] ?? 404;
$query = http_build_query(['team_id' => $teamId]);

$context = stream_context_create(['http' => [
    'header' => "Authorization: Bearer " . getenv('GOALISE_TOKEN') . "\r\nAccept: application/json",
    'ignore_errors' => true, // read the JSON body of 4xx answers too
    'timeout' => 20,
]]);
$body = file_get_contents("https://api.goalise.com/api/v3/news-by-team?$query", false, $context);
$data = json_decode((string) $body, true);

if (($data['status'] ?? null) !== 'success') {
    $codes = array_column($data['errors'] ?? [], 'code');
    fwrite(fopen('php://stderr', 'w'), 'API error: ' . ($codes ? implode(', ', $codes) : 'no answer') . PHP_EOL);
    exit(1);
}

echo '<ul class="football-news">' . PHP_EOL;
foreach (array_slice($data['response'], 0, 10) as $article) {
    printf(
        '  <li><a href="%s" rel="noopener">%s</a> <time datetime="%s">%s</time></li>' . PHP_EOL,
        htmlspecialchars($article['original_url'] ?? '#'),
        htmlspecialchars($article['title'] ?? ''),
        gmdate('c', (int) ($article['timestamp'] ?? 0)),
        htmlspecialchars($article['published_at'] ?? '')
    );
}
echo '</ul>' . PHP_EOL;
