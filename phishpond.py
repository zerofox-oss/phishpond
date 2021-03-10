from os import path
from bullet import Check
import argparse
import docker
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()  # sys.stderr
console_handler.setLevel(
    logging.CRITICAL
)  # set later by set_log_level_from_verbose() in interactive sessions
console_handler.setFormatter(
    logging.Formatter("[%(levelname)s]: %(message)s")
)
logger.addHandler(console_handler)


def setup_args():
    parser = argparse.ArgumentParser(
        description="༼ つ ◕_◕ ༽つ [naughty telegram bots]", prog="phishpond.py"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        help="verbose level... repeat up to three times.",
    )
    sp = parser.add_subparsers(dest="cmd")
    ssp = sp.add_parser("setup")
    ssp.add_argument("-f", "--force", action="store_true")
    sp.add_parser("run")
    sp.add_parser("stop")
    return parser


def set_log_level_from_verbose(args):
    if not args.verbose:
        console_handler.setLevel("ERROR")
    elif args.verbose == 1:
        console_handler.setLevel("WARNING")
    elif args.verbose == 2:
        console_handler.setLevel("INFO")
    elif args.verbose >= 3:
        console_handler.setLevel("DEBUG")
    else:
        logger.critical("UNEXPLAINED NEGATIVE COUNT!")


def stop_all():
    client = docker.from_env()
    for module in ["mitmproxy", "db", "webserver", "browser"]:
        try:
            c = client.containers.get(f"pp_{module}")
            c.stop()
            c.remove()
            logger.info(f"Destroyed pp_{module}")
        except:
            continue


def main():
    p = setup_args()
    args = p.parse_args()
    set_log_level_from_verbose(args)

    if args.cmd == "setup":
        client = docker.from_env()
        logger.info("Building environment")

        if args.force:
            images = {
                "docker/mitmproxy": "pp_mitmproxy",
                "docker/db": "pp_db",
                "docker/web": "pp_webserver",
                "docker/browser": "pp_browser",
            }
            for image in images:
                logger.debug(f"Removing docker image: {images[image]}")
                client.images.remove(images[image])
                logger.info(f"Removed docker image: {images[image]}")
            logger.info("Docker images removed")

        # make network
        try:
            client.networks.get("pp_network")
        except docker.errors.NotFound:
            client.networks.create("pp_network", driver="bridge", check_duplicate=True)
            logger.info("Created docker bridge network: pp_network")
        else:
            logger.debug("Docker bridge network already exists: pp_network")
        logger.info("Docker network creation complete")

        # make volumes
        for vol in ["pp-mitm-volume", "pp-db-data", "pp-browser-volume"]:
            try:
                client.volumes.get(vol)
            except docker.errors.NotFound:
                client.volumes.create(vol)
                logger.info(f"Created docker volume: {vol}")
            else:
                logger.info(f"Docker volume already exists: {vol}")
        logger.info("Docker volume creation complete")

        # build images
        images = {
            "docker/mitmproxy": "pp_mitmproxy",
            "docker/db": "pp_db",
            "docker/web": "pp_webserver",
            "docker/browser": "pp_browser",
        }
        for image in images:
            try:
                client.images.get(images[image])
            except docker.errors.NotFound:
                logger.info(f"Building docker image: {images[image]}")
                client.images.build(path=image, tag=images[image])
                logger.info(f"Created docker image: {images[image]}")
            else:
                logger.info(f"Docker image already exists: {images[image]}")
        logger.info("Docker image creation complete")

    if args.cmd == "run":
        cli = Check(
            prompt="Choose additional modules (mitmproxy/webserver included by default)",
            choices=["db", "browser"],
        )
        result = cli.launch()

        stop_all()

        client = docker.from_env()
        logger.info("Running pp_mitmproxy")
        client.containers.run(
            "pp_mitmproxy",
            name="pp_mitmproxy",
            tty=True,
            network="phishpond_network",
            detach=True,
            auto_remove=True,
            ports={8081: 8080},
            volumes={
                "pp-mitm-volume": {
                    "bind": "/home/mitmproxy/.mitmproxy/",
                    "mode": "rw",
                },
                "/home/cb/repos/phishpond/configs/mitmproxy/config.yaml": {
                    "bind": "/home/mitmproxy/.mitmproxy/config.yaml",
                    "mode": "rw",
                },
            },
            command="mitmweb --web-host 0.0.0.0 --set confdir=/home/mitmproxy/.mitmproxy --set relax_http_form_validation --ignore-hosts '(mozilla\.com|mozilla\.net|detectportal\.firefox\.com)'",
        )

        logger.info("Running pp_webserver")
        client.containers.run(
            "pp_webserver",
            name="pp_webserver",
            network="phishpond_network",
            hostname="phishpond.local",
            detach=True,
            auto_remove=True,
            ports={80: 80, 443: 443},
            volumes={
                "pp-mitm-volume": {
                    "bind": "/usr/local/share/ca-certificates/extra/",
                    "mode": "rw",
                },
                "/home/cb/repos/phishpond/www": {"bind": "/var/www/html", "mode": "rw"},
                "/home/cb/repos/phishpond/configs/web/vhosts": {
                    "bind": "/etc/apache2/sites-enabled/",
                    "mode": "rw",
                },
                "/home/cb/repos/phishpond/configs/php/php.ini": {
                    "bind": "/usr/local/etc/php/php.ini",
                    "mode": "rw",
                },
                "/home/cb/repos/phishpond/configs/php/patch.php": {
                    "bind": "/usr/local/bin/patch.php",
                    "mode": "rw",
                },
                "/home/cb/repos/phishpond/configs/php/unpatch.php": {
                    "bind": "/usr/local/bin/unpatch.php",
                    "mode": "rw",
                },
                "/home/cb/repos/phishpond/logs": {"bind": "/var/log/phishpond/", "mode": "rw"},
            },
            command=[
                "bash", "-c", "cp /usr/local/share/ca-certificates/extra/mitmproxy-ca-cert.{pem,crt} && update-ca-certificates --verbose && chmod -R 777 /var/log/phishpond && apache2-foreground"
            ]
        )

        if "db" in result:
            client.containers.run(
                "pp_db",
                name="pp_db",
                tty=True,
                network="phishpond_network",
                detach=True,
                auto_remove=True,
                volumes={
                    "pp-db-data": {
                        "bind": "/var/lib/mysql",
                        "mode": "rw",
                    }
                }
            )

        logger.info("All containers running!")

        if "browser" in result:
            client.containers.run(
                "pp_browser",
                name="pp_browser",
                tty=True,
                network="phishpond_network",
                ports={5800: 5800},
                detach=True,
                auto_remove=True,
                volumes={
                    "pp-browser-data": {
                        "bind": "/config",
                        "mode": "rw",
                    },
                    "pp-mitm-volume": {
                        "bind": "/config/certs",
                        "mode": "rw",
                    }
                }
            )

    if args.cmd == "stop":
        stop_all()


if __name__ == "__main__":
    main()