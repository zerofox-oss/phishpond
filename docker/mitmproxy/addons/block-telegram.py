"""
Add a new mitmproxy option.
Block outgoing Telegram API messages, and log
author: @teachemtechy

Usage:

    mitmproxy -s block-telegram.py
"""
from mitmproxy import ctx, http


class BlockTelegram:
    def __init__(self):
        self.num = 0

    def load(self, loader):
        loader.add_option(
            name = "block_telegram",
            typespec = bool,
            default = True,
            help = "Block and log outgoing Telegram API calls",
        )

    def response(self, flow):
        telegram_api_domain = 'api.telegram.org'
        if flow.request.pretty_host.endswith(telegram_api_domain):
            flow.response = http.HTTPResponse.make(
                201,
                b"Logged Telegram Data!",
                {"Content-Type": "text/html"}
            )


addons = [
    BlockTelegram()
]
