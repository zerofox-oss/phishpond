import os
import configparser

cfg = configparser.ConfigParser()


# class to hold container configurations
class Configs:
    # TODO make these private
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "docker", "configs")
    )
    cfg.read(os.path.join(os.path.dirname(__file__), "config.ini"))

    @classmethod
    def validate_mounts(cls):
        valid = True
        mounts = list(cfg["MOUNTS"])
        for mount in mounts:
            setting = cfg["MOUNTS"][mount]
            if not os.path.exists(setting):
                valid = False
                print(f"[{mount}] - Invalid path!")

        return valid

    mitmproxy = {
        "name": "pp_mitmproxy",
        "network": "phishpond_network",
        "detach": True,
        "remove": True,
        # "auto_remove": True,
        "ports": {8081: 8080},
        "volumes": {
            "pp-mitm-volume": {
                "bind": "/home/mitmproxy/.mitmproxy/",
                "mode": "rw",
            },
            f"{config_path}/mitmproxy/config.yaml": {
                "bind": "/home/mitmproxy/.mitmproxy/config.yaml",
                "mode": "rw",
            },
        },
        "command": "mitmweb --web-host 0.0.0.0 --set confdir=/home/mitmproxy/.mitmproxy --set relax_http_form_validation --ignore-hosts '(mozilla\.com|mozilla\.net|detectportal\.firefox\.com)'",
    }

    webserver = {
        "name": "pp_webserver",
        "network": "phishpond_network",
        "hostname": "phishpond.local",
        "detach": True,
        "remove": True,
        # "auto_remove": True,
        "ports": {80: 80, 443: 443},
        "links": {"pp_mitmproxy": "pp_mitmproxy"},
        "volumes": {
            "pp-mitm-volume": {
                "bind": "/usr/local/share/ca-certificates/extra/",
                "mode": "rw",
            },
            cfg["MOUNTS"]["www"]: {
                "bind": "/var/www/html",
                "mode": "rw"
            },
            f"{config_path}/web/vhosts": {
                "bind": "/etc/apache2/sites-enabled/",
                "mode": "rw",
            },
            f"{config_path}/php/php.ini": {
                "bind": "/usr/local/etc/php/php.ini",
                "mode": "rw",
            },
            f"{config_path}/php/patch.php": {
                "bind": "/usr/local/bin/patch.php",
                "mode": "rw",
            },
            f"{config_path}/php/unpatch.php": {
                "bind": "/usr/local/bin/unpatch.php",
                "mode": "rw",
            },
            cfg["MOUNTS"]["logs"]: {
                "bind": "/var/log/phishpond/",
                "mode": "rw",
            },
        },
        "command": [
            "bash",
            "-c",
            "cp /usr/local/share/ca-certificates/extra/mitmproxy-ca-cert.{pem,crt} && update-ca-certificates --verbose && chmod -R 777 /var/log/phishpond && apache2-foreground",
        ],
    }

    mysql_db = {
        "name": "pp_mysql_db",
        "network": "phishpond_network",
        "detach": True,
        "remove": True,
        # "auto_remove": True,
        "volumes": {
            "pp-mysql-db-data": {
                "bind": "/var/lib/mysql",
                "mode": "rw",
            }
        },
        "environment": [
            f'MYSQL_ROOT_PASSWORD={cfg["MYSQL"]["mysql_root_password"]}',
            f'MYSQL_DATABASE={cfg["MYSQL"]["mysql_database"]}',
            f'MYSQL_USER={cfg["MYSQL"]["mysql_user"]}',
            f'MYSQL_PASSWORD={cfg["MYSQL"]["mysql_password"]}',
        ],
    }

    postgres_db = {
        "name": "pp_postgres_db",
        "network": "phishpond_network",
        "detach": True,
        "remove": True,
        # "auto_remove": True,
        "volumes": {
            "pp-postgres-db-data": {
                "bind": "/var/lib/postgresql/data",
                "mode": "rw",
            }
        },
        "environment": [
            f'POSTGRES_DB={cfg["POSTGRES"]["postgres_database"]}',
            f'POSTGRES_USER={cfg["POSTGRES"]["postgres_user"]}',
            f'POSTGRES_PASSWORD={cfg["POSTGRES"]["postgres_password"]}',
        ],
    }

    browser = {
        "name": "pp_browser",
        "network": "phishpond_network",
        "ports": {5800: 5800},
        "detach": True,
        "remove": True,
        # "auto_remove": True,
        "volumes": {
            "pp-browser-data": {
                "bind": "/config",
                "mode": "rw",
            },
            "pp-mitm-volume": {
                "bind": "/config/certs",
                "mode": "rw",
            },
        },
        "environment": [
            "FF_PREF_PROXY_TYPE=network.proxy.type=1",
            'FF_PREF_HTTP_PROXY=network.proxy.http="pp_mitmproxy"',
            "FF_PREF_HTTP_PROXY_PORT=network.proxy.http_port=8080",
            'FF_PREF_HTTPS_PROXY=network.proxy.ssl="pp_mitmproxy"',
            "FF_PREF_HTTPS_PROXY_PORT=network.proxy.ssl_port=8080",
            "FF_PREF_CAPTIVE_PORTAL=network.captive-portal-service.enabled=false",
            "DISPLAY_WIDTH=1280",
            "DISPLAY_HEIGHT=768",
        ],
    }
