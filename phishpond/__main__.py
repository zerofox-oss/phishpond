from rich import print
from .menus import Menus as menus
from .runner import start_stop, print_status
from .client import attach, setup, configure
import argparse

def setup_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--setup',
        help='Perform setup or rebuild operations',
        action="store_true",
        required=False)
    return parser


def main():
    p = setup_args()
    args = p.parse_args()

    if args.setup:
        setup()
        return

    try:
        print(menus.banner)
        print("Feature requests and PR's welcome!\nhttps://github.com/zerofox-oss/phishpond\n")
        while True:
            result = menus.launcher()

            if result == "Start/Stop":
                start_stop()
            if result == "Attach":
                attach()
            if result == "Configure":
                configure()
            if result == "Status":
                print_status()
            if result == "Exit":
                return
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
