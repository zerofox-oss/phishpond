<?php
echo '#####file_get_contents_rewrite.php<br>';

echo '# Does the phishpond rewrite of file_get_contents_rewrite.php exist? -> ';
echo function_exists('int_file_get_contents');
echo '<br>'
if (!function_exists('int_file_get_contents')) {
    runkit7_function_rename('file_get_contents', 'int_file_get_contents');
    echo '# Renamed to int_file_get_contents!<br>';
}
echo 'Function exists int_file_get_contents: ';
echo function_exists('int_file_get_contents');
echo "<br>";

if (function_exists('int_file_get_contents') && !function_exists('file_get_contents')) {
    runkit7_function_add(
	'file_get_contents', 
	function(string $filename, bool $use_include_path = FALSE, resource $context = NULL, int $offset = 0, int $maxlen = 0 ) {
	    echo "Filename is -> $filename\n";
    });
}
echo '#####END file_get_contents_rewrite.php<br>';
?>

