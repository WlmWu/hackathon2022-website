<?php 
$command = escapeshellcmd('python showAllDB.py');
$output = shell_exec($command);
echo $output;
?>