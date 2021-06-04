from os import path
from bullet.client import Input
import docker
import docker.errors
from rich import print
from rich.prompt import Confirm
import os
import re
from .menus import Menus as menus
from rich.progress import Progress, TimeElapsedColumn, BarColumn
from bullet import Bullet, Check
import dockerpty
import subprocess



docker_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "docker"))

images = {
    "pp_mitmproxy": f"{docker_path}/mitmproxy",
    "pp_db": f"{docker_path}/db",
    "pp_webserver": f"{docker_path}/web",
    "pp_browser": f"{docker_path}/browser",
}

def get_status():
    states = {}
    client = docker.from_env()
    for image in images.keys():
        try:
            c = client.containers.get(image)
            states[image] = c.status
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
        prompt="Select a container\n",
        choices=[*running],
        bullet=">>",
        margin=2
    )
    selection = cli.launch()

    subprocess.Popen(f'docker exec -e \'TERM=xterm-256color\' -t -i {selection} /bin/bash')
    
    # client = docker.from_env()
    # c = client.containers.get(selection)

    # dockerpty.start(client.api, c.id)

    # while True:
    #     cli = Input(prompt="$> ")
    #     cmd = cli.launch()
    #     if cmd:
    #         r = c.exec_run(cmd)
    #         print(r.output.decode("utf-8"))
