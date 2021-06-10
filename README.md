<p align="center">
  <img src="https://i.imgur.com/ElaxFKN.png">
</p>

## What is phishpond?
It's a pre-built dockerised environment which allows you to quickly and easily spin up phishing kits for analysis. Out of the box you can host and browse kits, "mitm" web traffic, log mail and telegram calls to flat files, and debug PHP code.

## Installing
You can use phishpond either as a CLI package, or use the included `docker-compose.yml` to build and manage the containers manually.

### CLI
Clone the repository
```bash
git clone https://github.com/zerofox-oss/phishpond
```

Install the requirements
```bash
pip install -r requirements.txt
```

Install phishpond
```bash
pip install -e .
```

Run phishpond setup
```bash
phishpond --setup
```

Follow the prompts to build the required containers, volumes, networks, and set required variables.

### Compose
Clone the repository
```bash
git clone https://github.com/zerofox-oss/phishpond
```

Run docker-compose
```bash
docker-compose up
```

## How to use
1. `git clone https://github.com/zerofox-oss/phishpond.git`
2. `cd ./phishpond/`
3. Configure any db connection strings within `docker-compose.yml`
4. `docker-compose up -d`
5. Browse to `http://localhost:5800` for the virtual browser
6. Browse to `http://localhost:8080` for mitmproxy
7. Within the virtual browser navigate to `http://phishpond.local`

(First time setup)
1. Open preferences within the virtual browser
2. Search `cert`
3. Click `view certificates`
4. Click the authorities tab
5. Click Import
6. Import `/config/certs/mitmproxy-ca-cert.pem`
7. Tick `Trust this CA to identify websites`
8. OK

You will need to repeat these steps every time you remove the `browser-volume`
