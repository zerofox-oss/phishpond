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
    states = get_status()
    for state in states:
        status_table.add_row(state, states[state])

    console.print(status_table)
    print("\n")
