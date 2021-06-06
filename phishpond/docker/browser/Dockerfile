# Dockerfile pulled from sprintcube/docker-compose-lamp
FROM jlesage/firefox:v1.17.0

ENV FF_PREF_PROXY_TYPE=network.proxy.type=1
ENV FF_PREF_HTTP_PROXY=network.proxy.http="mitmproxy"
ENV FF_PREF_HTTP_PROXY_PORT=network.proxy.http_port=8080
ENV FF_PREF_HTTPS_PROXY=network.proxy.ssl="mitmproxy"
ENV FF_PREF_HTTPS_PROXY_PORT=network.proxy.ssl_port=8080
ENV FF_PREF_CAPTIVE_PORTAL=network.captive-portal-service.enabled=false
ENV DISPLAY_WIDTH=1280
ENV DISPLAY_HEIGHT=768

COPY .bashrc /root/.bashrc