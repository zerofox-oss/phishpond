"""
Add a new mitmproxy option.
Block outgoing Telegram API messages, and log
author: @teachemtechy

Usage:

    mitmproxy -s block-telegram.py
"""
from mitmproxy import http
import json


class BlockTelegram:
    def __init__(self):
        self.outfile = "/home/mitmproxy/logs/telegram.log"

    def load(self, loader):
        loader.add_option(
            name="block_telegram",
            typespec=bool,
            default=True,
            help="Block and log outgoing Telegram API calls",
        )

    def response(self, flow):
        telegram_api_domain = "api.telegram.org"
        if flow.request.pretty_host.endswith(telegram_api_domain):
            data = {}
            data["payload"] = flow.request.get_text()
            data["headers"] = {
                key: value for (key, value) in flow.request.headers.items()
            }
            data["url"] = flow.request.pretty_url
            with open(self.outfile, "a") as fd:
                json.dump(data, fd)
                fd.write("\n")

            flow.response = http.HTTPResponse.make(
                201, b"Logged data to logs/telegram.log", {"Content-Type": "text/html"}
            )


addons = [BlockTelegram()]
