<?php

$encodedUrl = "aHR0cHM6Ly9zdHJlYW1lZC5zdS9hcGkvbWF0Y2hlcy9hbGw=";
$jsonUrl = base64_decode($encodedUrl);
$defaultPoster = 'https://raw.githubusercontent.com/WaroenkTV/m3u8/refs/heads/main/LiveSports.png';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $jsonUrl);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept: application/json",
    "Accept-Language: en-US,en;q=0.5"
]);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$jsonData = curl_exec($ch);
if ($jsonData === false) {
    die('cURL Error: ' . curl_error($ch));
}
curl_close($ch);

$data = json_decode($jsonData, true);
if ($data === null) {
    die('Failed to decode JSON data');
}

function shouldSkipEvent($eventDate, $currentDateTime) {
    if ($eventDate == 0) {
        return false;
    }
    $eventDateTime = new DateTime("@".($eventDate / 1000));
    $interval = $eventDateTime->getTimestamp() - $currentDateTime->getTimestamp();
    $hoursDiff = $interval / 3600;
    return $hoursDiff < -4 || $hoursDiff > 8;
}

$currentDateTime = new DateTime("now", new DateTimeZone('Asia/Bangkok'));

$m3u8Content = "#EXTM3U\n\n";

foreach ($data as $match) {
    if (shouldSkipEvent($match['date'], $currentDateTime)) {
        continue;
    }

    $poster = isset($match['poster']) ? 'https://streamed.su' . $match['poster'] : $defaultPoster;
    $category = ($match['date'] == 0) ? "24/7 Live" : $match['category'];
    $categoryFormatted = ($category === "24/7 Live") ? "24/7 Live" : ucwords(str_replace('-', ' ', $category));

    foreach ($match['sources'] as $source) {
        $sourceName = ucwords(strtolower($source['source']));
        $id = $source['id'];
        $dateTime = new DateTime("@".($match['date'] / 1000));
        $dateTime->setTimezone(new DateTimeZone('Asia/Bangkok'));
        // Change this line to use 24-hour format
        $formattedTime = $dateTime->format('H:i');
        $formattedDate = $dateTime->format('d/m/Y');

        if ($category === "24/7 Live") {
            $m3u8Content .= "#EXTINF:-1 tvg-name=\"{$match['title']}\" tvg-logo=\"{$poster}\" group-title=\"{$categoryFormatted}\",{$match['title']}\n";
        } else {
            $matchName = "{$formattedTime} - {$match['title']} [{$sourceName}] - ({$formattedDate})";
            $m3u8Content .= "#EXTINF:-1 tvg-name=\"{$match['title']}\" tvg-logo=\"{$poster}\" group-title=\"{$categoryFormatted}\",{$matchName}\n";
        }

        $m3u8Content .= "https://rr.vipstreams.in/{$sourceName}/js/{$id}/1/playlist.m3u8\n";
    }
}

file_put_contents('streamedsu.m3u8', $m3u8Content);

echo "M3U8 file has been saved as streamedsu.m3u8.\n";

?>
