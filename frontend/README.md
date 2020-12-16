# Phishpond Frontend

## Description

This frontend will allow you to upload phish kits for automated analysis. It will generate reports for additional pivoting.

## Dev

1. `docker-compose build frontend`
2. `docker-compose up frontend`
3. `Navigate to localhost:8080`

It should hot-reload if you make a change, as it uses docker compose volumes. 

If you need to install a new package, either install it in this directory via `npm`, or drop into a shell on the container then run the necessary installs. `bash ../get_shell.sh frontend` then `npm install`
