from bullet import Bullet, Check, Input
import textwrap
import sys
from .configs import cfg


class Menus(object):
    b_opts = {"bullet": ">>", "margin": 2}
    c_opts = {"check": ">>", "margin": 2}
    banner = textwrap.dedent(
        (
            """
        ██▓███   ██░ ██  ██▓  ██████  ██░ ██  ██▓███   ▒█████   ███▄    █ ▓█████▄
        ▓██░  ██▒▓██░ ██▒▓██▒▒██    ▒ ▓██░ ██▒▓██░  ██▒▒██▒  ██▒ ██ ▀█   █ ▒██▀ ██▌
        ▓██░ ██▓▒▒██▀▀██░▒██▒░ ▓██▄   ▒██▀▀██░▓██░ ██▓▒▒██░  ██▒▓██  ▀█ ██▒░██   █▌
        ▒██▄█▓▒ ▒░▓█ ░██ ░██░  ▒   ██▒░▓█ ░██ ▒██▄█▓▒ ▒▒██   ██░▓██▒  ▐▌██▒░▓█▄   ▌
        ▒██▒ ░  ░░▓█▒░██▓░██░▒██████▒▒░▓█▒░██▓▒██▒ ░  ░░ ████▓▒░▒██░   ▓██░░▒████▓
        ▒▓▒░ ░  ░ ▒ ░░▒░▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒  ▒▒▓  ▒
        ░▒ ░      ▒ ░▒░ ░ ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░░▒ ░       ░ ▒ ▒░ ░ ░░   ░ ▒░ ░ ▒  ▒
        ░░        ░  ░░ ░ ▒ ░░  ░  ░   ░  ░░ ░░░       ░ ░ ░ ▒     ░   ░ ░  ░ ░  ░
                ░  ░  ░ ░        ░   ░  ░  ░             ░ ░           ░    ░
                                                                            ░
    """
        )
    )

    def delete_line(count):
        for i in range(count):
            sys.stdout.write("\x1b[1A")
            sys.stdout.write("\x1b[2K")

    @classmethod
    def launcher(cls):
        cli = Bullet(
            # prompt="Select a menu option from below.\n",
            choices=["Start/Stop", "Status", "Attach", "Configure", "Exit"],
            **cls.b_opts
        )
        selection = cli.launch()
        cls.delete_line(len(cli.choices))
        return selection

    @classmethod
    def module_prompt(cls):
        cli = Check(
            prompt="Choose additional modules (mitmproxy/webserver included by default)\n",
            choices=["pp_browser", "pp_mysql_db", "pp_postgres_db"],
            **cls.c_opts
        )
        selection = cli.launch()
        cls.delete_line(len(cli.choices) + 2)
        return selection

    @classmethod
    def volume_prompt(cls):
        vols = ["pp-mitm-volume", "pp-mysql-db-data", "pp-postgres-db-data", "pp-browser-volume"]
        cli = Check(
            prompt="Choose volumes to rebuild or press ENTER to leave all existing data\n",
            choices=vols,
            **cls.c_opts
        )
        selection = cli.launch()
        cls.delete_line(len(cli.choices) + 2)
        return selection

    @classmethod
    def config_sections(cls):
        # get section
        cli = Bullet(
            prompt="Select a section\n", choices=[*cfg.sections(), "Exit"], **cls.b_opts
        )
        selection = cli.launch()
        cls.delete_line(len(cfg.sections()) + 3)
        return selection

    @classmethod
    def config_key(cls, section):
        cli = Bullet(
            prompt="Select a setting to edit\n",
            choices=[*list(cfg[section]), "Exit"],
            **cls.b_opts
        )
        selection = cli.launch()
        cls.delete_line(len(list(cfg[section])) + 3)
        return selection

    @classmethod
    def config_input(cls, section, key):
        cli = Input(
            prompt="Update value or press ENTER to keep existing value\n",
            default=cfg[section][key],
        )
        v = cli.launch()
        return v
