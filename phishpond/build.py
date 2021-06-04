from os import path
import docker
import docker.errors
from rich import print
from rich.prompt import Confirm
import os
import re
from .menus import Menus as menus
from rich.progress import Progress, TimeElapsedColumn, BarColumn


docker_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "docker"))

images = {
    "pp_mitmproxy": f"{docker_path}/mitmproxy",
    "pp_db": f"{docker_path}/db",
    "pp_webserver": f"{docker_path}/web",
    "pp_browser": f"{docker_path}/browser",
}


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
            menus.delete_line(len(existing) + 2)
            return

        # stop and remove images
        kill()
        for image in images:
            try:
                client.images.remove(image, force=True)
            except docker.errors.NotFound as e:
                continue

    # make volumes
    v_choice = None
    for vol in ["pp-mitm-volume", "pp-db-data", "pp-browser-volume"]:
        try:
            v = client.volumes.get(vol)
            if v_choice is None:
                v_choice = Confirm.ask(
                    "Delete existing volumes?\n[bold]This will erase all database data and browser configuration"
                )
            if v_choice is True:
                v.remove()
            else:
                continue
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

    # build images
    client = docker.APIClient(base_url="unix://var/run/docker.sock")
    for image in images:
        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeElapsedColumn(),
        ) as progress:
            task = progress.add_task(f"Building {image}", total=100, start=True)
            streamer = client.build(decode=True, path=images[image], tag=image, rm=True)
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
                        print(line)

    print("Docker image creation complete")
    return


def kill():
    client = docker.from_env()
    for module in images.keys():
        try:
            c = client.containers.get(module)
            print(f"Stopping {module}")
            c.stop(timeout=3)
        except docker.errors.NotFound:
            # print(type(e).__name__) < get exception type name
            continue
