<?php

$proxy = getenv('http_proxy');

if (!empty($proxy)) {

    $proxy = str_replace('http://', 'tcp://', $proxy);

    echo "Found a proxy " . $proxy . PHP_EOL;

    $context = array(
        'http' => array(
            'proxy' => $proxy,
            'request_fulluri' => true,
            'verify_peer'      => false,
            'verify_peer_name' => false,
        ),
        "ssl"=>array(
        "verify_peer"=>false,
        "verify_peer_name"=>false
        )
    );

    stream_context_set_default($context);
} else {
    echo "Proxy not found" . PHP_EOL;
}
?>
