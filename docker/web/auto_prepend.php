<?php
/*
 * rename file_get_contents to an internal name
 * add a new reserved file_get_contents
 * within the new one, check if the first argument is http/https, if it is write to log, if it isnt then call int_file_get_contents
 */
runkit7_function_rename('file_get_contents', 'int_file_get_contents');
// TODO: add logic in separate file perhaps to load the correct code in, also make sure the arguments line up to pass to int_file_get_contents
runkit7_function_add('file_get_contents, 'echo "hello there";');
?>
