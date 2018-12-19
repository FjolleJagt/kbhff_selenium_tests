<?php

$password = $argv[1];
$hashed_password = password_hash($password, PASSWORD_DEFAULT);
print($hashed_password);

?>
