<?php
    uopz_set_return('stream_context_create', function(array $options) {
        $array = func_get_args();
        $array[0]["http"]['proxy']='mitmproxy:8080';
        return stream_context_create($array[0]);
    }, 1);
?>

