<?php
    ob_start();
    // Set default stream context if none specified
    $default_opts = array(
      'http'=>array(
	'proxy'=>'mitmproxy:8080'
      )
    );
    $default = stream_context_set_default($default_opts);

    // Hijack stream_context_create in case someone overrides our default
    uopz_set_return('stream_context_create', function(array $options) {
        $array = func_get_args();
        $array[0]['http']['proxy']='mitmproxy:8080';
        return stream_context_create($array[0]);
    }, 1);
?>

