<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome!</title>
</head>
<body>
  <p align="center">
    <img align="center" src="./phishpondlogo.png">
  </p>
  
  
    <h1 align="center">Howdy! 🤠</h1>
    <p align="center">
    Welcome to PhishPond.
    <br>
    If you can see this message, it means you're up and running! Yeehaw!
    <br>
  </p>
<?php
$files = glob('./*');
foreach($files as $file)
{
    if (is_dir($file)) {
	echo "<br><a href=$file>".basename($file)."/</a>";
    } else {
	echo "<br><a href=$file>".basename($file)."</a>";
    }

}

?>
</body>
</html>