<?php

$password = "kbhff2357";
$hashed_password = password_hash($password, PASSWORD_DEFAULT);
print($hashed_password);

?>
