# Dockerfile pulled from sprintcube/docker-compose-lamp
FROM mitmproxy/mitmproxy:latest
RUN apk add bash vim
RUN chmod -R 777 /home/mitmproxy/.mitmproxy 
COPY addons /home/mitmproxy/addons/ 
