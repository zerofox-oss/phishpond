#!/bin/bash
Help()
{
   # Display Help
   echo "Specify the container you want a shell for ya dingus."
   echo "Example: ./get_shell.sh webserver"
}

while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit;;
   esac
done
docker exec -t -i `docker ps | grep "$1" | cut -d " " -f 1` sh
