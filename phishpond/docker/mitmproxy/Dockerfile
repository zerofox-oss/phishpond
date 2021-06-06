# Dockerfile pulled from sprintcube/docker-compose-lamp
FROM mitmproxy/mitmproxy:latest
RUN apk add bash vim
RUN mkdir /home/mitmproxy/logs
RUN chmod -R 777 /home/mitmproxy/.mitmproxy /home/mitmproxy/logs 
COPY addons /home/mitmproxy/addons/ 
COPY .bashrc /root/.bashrc

EXPOSE 8080:8081