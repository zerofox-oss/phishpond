"""
Add a new mitmproxy option.
Log intercepted PHP mail calls
author: @sysgoblin

Usage:

    mitmproxy -s mail-intercept.py
"""
from mitmproxy import ctx, http


class MailIntercept:

    def request(self, flow) -> None:
        if flow.request.pretty_url == "http://mail.capture.phishpond/":
            flow.response = http.HTTPResponse.make(
                200,  
                b"Mail data logged",  
                {"Content-Type": "text/html"}  
            )


addons = [
    MailIntercept()
]
