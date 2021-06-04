from bullet import Bullet, Check
import textwrap
import sys


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
            prompt="Select a menu option from below.\n",
            choices=["Run", "Stop", "Status", "Configure", "Initial Setup", "Exit"],
            **cls.b_opts
        )
        selection = cli.launch()
        cls.delete_line(len(cli.choices) + 2)
        return selection

    @classmethod
    def module_prompt(cls):
        cli = Check(
            prompt="Choose additional modules (mitmproxy/webserver included by default)\n",
            choices=["db", "browser"],
            **cls.c_opts
        )
        selection = cli.launch()
        cls.delete_line(len(cli.choices) + 2)
        return selection
