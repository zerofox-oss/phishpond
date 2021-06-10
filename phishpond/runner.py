from rich import print
from rich.console import Console
from rich.table import Table
from .client import get_status, start_phishpond, stop_phishpond
from .configs import Configs


def start_stop():
    containers = get_status()
    running = [name for name, status in containers.items() if status == "running"]
    if not running:
        valid_config = Configs.validate_mounts()
        if not valid_config:
            print("Please fix config issues before running phishpond\n")
            return
        start_phishpond()
    else:
        stop_phishpond()

    return


def print_status():
    console = Console()
    status_table = Table()
    status_table.add_column("Module")
    status_table.add_column("State")
    status_table.add_column("URL")
    states = get_status()
    for state in states:
        url = "N/A"
        if state == "pp_mitmproxy":
            url = "http://localhost:8080"
        if state == "pp_webserver":
            url = "http://localhost:80"
        if state == "pp_browser":
            url = "http://localhost:5800"
        status_table.add_row(state, states[state], url)

    console.print(status_table)
    print("\n")
