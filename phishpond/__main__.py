from rich import print
from .build import setup, kill
from .menus import Menus as menus
from .runner import run, status
from .configs import Configs
from .client import attach


def main():
    try:
        print(menus.banner)
        while True:
            result = menus.launcher()

            if result == "Initial Setup":
                setup()
            if result == "Run":
                run()
            if result == "Stop":
                kill()
            # if result == "Attach":
            #     attach()
            if result == "Configure":
                Configs.configure()
            if result == "Status":
                status()
            if result == "Exit":
                return
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
