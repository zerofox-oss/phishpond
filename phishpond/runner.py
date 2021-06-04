#!/usr/bin/env python3

import docker
import docker.errors
from rich import print
from rich.console import Console
from rich.table import Table

from .configs import Configs
from .menus import Menus as menus


def run():
    result = menus.module_prompt()
    client = docker.from_env()

    # TODO tidy this up
    try:
        client.containers.run("pp_mitmproxy", **Configs.mitmproxy)
        print("Running pp_mitmproxy")
    except docker.errors.APIError as e:
        if e.response.status_code == 409:
            print("pp_mitmproxy already running")

    try:
        client.containers.run("pp_webserver", **Configs.webserver)
        print("Running pp_webserver")
    except docker.errors.APIError as e:
        if e.response.status_code == 409:
            print("pp_webserver already running")

    try:
        if "db" in result:
            client.containers.run("pp_db", **Configs.db)
            print("Running pp_db")
    except docker.errors.APIError as e:
        if e.response.status_code == 409:
            print("pp_db already running")

    try:
        if "browser" in result:
            client.containers.run("pp_browser", **Configs.browser)
            print("Running pp_browser")
    except docker.errors.APIError as e:
        if e.response.status_code == 409:
            print("pp_browser already running")

    print("All containers running!\n")

    print("mitmweb:\thttp://localhost:8080")
    if "browser" in result:
        print("browser:\thttp://localhost:5800")
    print("\n")


def status():
    console = Console()
    status_table = Table()
    status_table.add_column("Module")
    status_table.add_column("State")
    client = docker.from_env()
    for module in ["pp_mitmproxy", "pp_db", "pp_webserver", "pp_browser"]:
        try:
            client.containers.get(module)
            status_table.add_row(module, "Running")
        except docker.errors.NotFound:
            status_table.add_row(module, "Not running")

    console.print(status_table)
