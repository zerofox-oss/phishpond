import docker
import docker.errors
import os
from .menus import Menus as menus
from rich.progress import Progress, TimeElapsedColumn, BarColumn
from bullet import Bullet
import re
from rich.prompt import Confirm
from rich import print
from .configs import Configs, cfg
import time


docker_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "docker"))

images = {
    "pp_mitmproxy": {"path": f"{docker_path}/mitmproxy", "config": Configs.mitmproxy},
    "pp_mysql_db": {"path": f"{docker_path}/mysql_db", "config": Configs.mysql_db},
    "pp_postgres_db": {
        "path": f"{docker_path}/postgres_db",
        "config": Configs.postgres_db,
    },
    "pp_webserver": {"path": f"{docker_path}/web", "config": Configs.webserver},
    "pp_browser": {"path": f"{docker_path}/browser", "config": Configs.browser},
}


def get_status():
    states = {}
    client = docker.from_env()
    for image in images.keys():
        try:
            c = client.containers.get(image)
            if c.status == "running":
                states[image] = c.status
            else:
                states[image] = "not_running"
        except docker.errors.NotFound:
            states[image] = "not_running"
    return states


def attach():
    containers = get_status()
    running = [name for name, status in containers.items() if status == "running"]
    if not running:
        print("No containers currently running")
        return

    cli = Bullet(
        prompt="Select a container\n", choices=[*running], bullet=">>", margin=2
    )
    selection = cli.launch()

    print("\n")
    os.system(f"docker exec -e 'TERM=xterm-256color' -it {selection} /bin/bash")
    print("\n")


def setup():
    client = docker.from_env()

    existing = {}
    for image in images:
        try:
            client.images.get(image)
            existing[image] = images[image]
        except docker.errors.ImageNotFound:
            continue

    if len(existing) > 0:
        choice = Confirm.ask("\nLooks like some modules are already built. Rebuild?")
        if choice is False:
            # menus.delete_line(len(existing) + 2)
            return

        # stop and remove images
        stop_phishpond()
        for image in images:
            try:
                client.images.remove(image, force=True)
            except docker.errors.NotFound:
                continue

    # make volumes
    v_choice = menus.volume_prompt()
    for vol in v_choice:
        try:
            v = client.volumes.get(vol)
            v.remove()
        except docker.errors.NotFound:
            pass
        client.volumes.create(vol)
        print(f"Created docker volume: {vol}")
    print("Docker volume creation complete\n")

    # make network
    try:
        n = client.networks.get("pp_network")
        n.remove()
    except docker.errors.NotFound:
        pass
    client.networks.create("pp_network", driver="bridge", check_duplicate=True)
    print("Created docker bridge network: pp_network\n")

    # validate config
    valid_config = Configs.validate_mounts()
    while not valid_config:
        print("\nSet required mount paths")
        key = menus.config_key("MOUNTS")
        if key == "Exit":
            return

        value = menus.config_input("MOUNTS", key)
        value = value.strip()

        if not value or cfg["MOUNTS"][key] == value:
            pass
        else:
            cfg.set("MOUNTS", key, value)
            with open(os.path.join(os.path.dirname(__file__), "config.ini"), "w") as ini:
                cfg.write(ini)
        valid_config = Configs.validate_mounts()

    # build images
    client = docker.APIClient(base_url="unix://var/run/docker.sock")
    i = 0
    for image in images:
        i += 1
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task(
                f"[{i}/{len(images)}] Building {image}", total=100, start=True
            )
            streamer = client.build(
                decode=True, path=images[image]["path"], tag=image, rm=True
            )
            for chunk in streamer:
                if "stream" in chunk:
                    for line in chunk["stream"].splitlines():
                        if re.match(r"^Step \d{1,2}\/\d{1,2} :", line):
                            stat = (
                                re.findall(r" \d{1,2}\/\d{1,2} ", line)[0]
                                .strip()
                                .split("/")
                            )
                            progress.update(task, total=int(stat[1]), advance=1)
                        # print(line)

    print("Docker image creation complete")
    return


def kill(module):
    client = docker.from_env()
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(f"Stopping {module}", total=100, start=True)
        try:
            c = client.containers.get(module)
            c.stop(timeout=10)
        except docker.errors.NotFound:
            pass
        progress.update(task, total=1, advance=1)


def stop_phishpond():
    containers = get_status()
    running = [name for name, status in containers.items() if status == "running"]
    for module in running:
        kill(module)
    print("\n")

    return


def run(module):
    client = docker.from_env()
    with Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeElapsedColumn(),
    ) as progress:
        task = progress.add_task(f"Starting {module}", total=1, start=True)
        try:
            state = "not_running"
            while state != "running":
                client.containers.run(module, **images[module]["config"])
                time.sleep(3)  # give a few seconds for it to wake up
                state = client.containers.get(module)  # check status
        except docker.errors.APIError as e:
            if e.response.status_code == 409:
                pass  # already running
            else:
                print(e)
        progress.update(task, total=1, advance=1)


def start_phishpond():
    result = menus.module_prompt()
    result = ["pp_mitmproxy", "pp_webserver"] + result

    for module in result:
        run(module)
    print("\n")

    print("mitmweb:\thttp://localhost:8080")
    print("webserver:\thttp://localhost:80")
    if "pp_browser" in result:
        print("browser:\thttp://localhost:5800")
    print("\n")


def configure():
    section = menus.config_sections()
    if section == "Exit":
        return
    key = menus.config_key(section)
    if key == "Exit":
        return
    value = menus.config_input(section, key)

    if not value or cfg[section][key] == value:
        return

    value = value.strip()
    cfg.set(section, key, value)
    with open(os.path.join(os.path.dirname(__file__), "config.ini"), "w") as ini:
        cfg.write(ini)

    containers = get_status()
    running = [name for name, status in containers.items() if status == "running"]

    if section == "MOUNTS" and "pp_webserver" in running:
        kill("pp_webserver")
        run("pp_webserver")

    if section == "MYSQL" and "pp_mysql_db" in running:
        kill("pp_mysql_db")
        run("pp_mysql_db")
        print("You will need to rebuild the pp-mysql-db volume for new credentials to take effect")

    if section == "POSTGRES" and "pp_postgres_db" in running:
        kill("pp_postgres_db")
        run("pp_postgres_db")
        print("You will need to rebuild the pp-postgres-db volume for new credentials to take effect")

    print("\n")
    return
