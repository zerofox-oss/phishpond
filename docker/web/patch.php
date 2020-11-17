<?php
    uopz_set_return('file_get_contents', function($filename, $use_include_path = FALSE, $resource = NULL, $offset = 0, $maxlen = 0) {
	echo "Number of arguments: " . func_num_args() . "\n";
	$arg_list = func_get_args();
	for ($i = 0; $i < func_num_args(); $i++) {
	    echo "Argument $i is: " . $arg_list[$i] . "\n";
	}
    }, 1);
?>

