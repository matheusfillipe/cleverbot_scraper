import codecs
import hashlib
import re
import time
import requests
from typing import List

from .constants import CLEVERBOT_URL, CLEVERBOT_API_URL


class Cleverbot:
    def __init__(self, context: List[str] = []):
        self.cookies = None
        self.context = context

        self.get_cookies()

    def get_cookies(self):
        if self.cookies is None:
            response = requests.get(CLEVERBOT_URL)
            self.cookies = {"XVIS": re.search(r"\w+(?=;)", response.headers["Set-cookie"]).group()}
        
    def post_message(self, message: str) -> str:
        payload = f"stimulus={requests.utils.requote_uri(message)}&"
        _context = self.context[:]
        reverse_context = list(reversed(_context))

        # Clear context list to keep things short and fast
        self.clear_context()
        for i in range(len(_context)):
            payload += f"vText{i + 2}={requests.utils.requote_uri(reverse_context[i])}&"

        # Append message to the context for future messages
        self.context.append(message)
        
        payload += "cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="

        # Checksum
        payload += hashlib.md5(payload[7:33].encode()).hexdigest()

        response = requests.post(
            CLEVERBOT_API_URL,
            cookies=self.cookies,
            data=payload,
        )

        # If the request is not succesful, refresh cookies
        if response.status_code != 200:
            self.get_cookies()
            
        response = re.split(r"\\r", str(response.content))[0]
        response = response[2:-1]

        # Append bot's response to the context
        self.context.append(response)
        return codecs.escape_decode(bytes(response, "utf-8"))[0].decode("utf-8")

    def clear_context(self):
        if len(self.context) > 15:
            self.context.pop(0)
