<p align="center">
  <img src="https://i.imgur.com/rA2SUEg.png">
</p>

## What is phishpond?
It's a pre-built docker environment which allows you to quickly, easily and safely spin up phishing kits for analysis. Out of the box you can browse, "mitm" web traffic, log mail calls to flat files and debug PHP code remotely.

## How to use
1. `git clone https://github.com/zerofox-oss/phishpond.git`
2. `cd ./phishpond/`
3. `docker-compose up -d`
4. Browse to `http://localhost:5800`
5. Browse to `http://localhost:8080` for mitmproxy
6. Within the virtual browser navigate to `http://phishpond.local`

(First time setup)
7. Navigate to `mitm.it`
8. Download the certificate for linux
9. Import the cert to the virtual browser
10.  Open preferences
11.  Search `proxy`
12.  Set the proxy for http/s to: `mitmproxy` with port `8080`
