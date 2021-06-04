import os
import configparser
from bullet import Bullet, Check, Input
from .menus import Menus


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
    def configure(cls):
        # get section
        cli = Bullet(
            prompt="Select a section\n",
            choices=[*cfg.sections(), "Exit"]
        )
        s_selection = cli.launch()
        Menus.delete_line(len(cfg.sections()) + 3)
        if s_selection == "Exit":
            return

        # get setting
        cli = Bullet(
            prompt="Select a setting to edit\n",
            choices=[*list(cfg[s_selection]), "Exit"]
        )
        k_selection = cli.launch()
        Menus.delete_line(len(list(cfg[s_selection])) + 3)
        if k_selection == "Exit":
            return

        cli = Input(
            prompt="Current value: " + cfg[s_selection][k_selection] + "\nEnter a new value:",
            strip=True
        )
        v = cli.launch()
        cfg.set(s_selection, k_selection, v)
        with open(os.path.join(os.path.dirname(__file__), "config.ini"), "w") as ini:
            cfg.write(ini)

    mitmproxy = {
        "name": "pp_mitmproxy",
        "tty": True,
        "stdin_open": True,
        "network": "phishpond_network",
        "detach": True,
        "auto_remove": True,
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
        "tty": True,
        "stdin_open": True,
        "network": "phishpond_network",
        "hostname": "phishpond.local",
        "detach": True,
        "auto_remove": True,
        "ports": {80: 80, 443: 443},
        "volumes": {
            "pp-mitm-volume": {
                "bind": "/usr/local/share/ca-certificates/extra/",
                "mode": "rw",
            },
            cfg["MOUNTS"]["www"]: {"bind": "/var/www/html", "mode": "rw"},
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

    db = {
        "name": "pp_db",
        "tty": True,
        "stdin_open": True,
        "network": "phishpond_network",
        "detach": True,
        "auto_remove": True,
        "volumes": {
            "pp-db-data": {
                "bind": "/var/lib/mysql",
                "mode": "rw",
            }
        },
        "environment": [
            f'MYSQL_ROOT_PASSWORD={cfg["MYSQL"]["MYSQL_ROOT_PASSWORD"]}',
            f'MYSQL_DATABASE={cfg["MYSQL"]["MYSQL_DATABASE"]}',
            f'MYSQL_USER={cfg["MYSQL"]["MYSQL_USER"]}',
            f'MYSQL_PASSWORD={cfg["MYSQL"]["MYSQL_PASSWORD"]}',
        ],
    }

    browser = {
        "name": "pp_browser",
        "tty": True,
        "stdin_open": True,
        "network": "phishpond_network",
        "ports": {5800: 5800},
        "detach": True,
        "auto_remove": True,
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
