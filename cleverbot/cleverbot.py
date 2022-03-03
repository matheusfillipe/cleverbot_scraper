import codecs
import hashlib
import re
from typing import List

import requests

from .constants import CLEVERBOT_URL, CLEVERBOT_API_URL

cookies = None
sessions = dict()

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
        print("[DEBUG] Message: ", message)
        _context = self.context[:]
        reverse_context = list(reversed(_context))

        for i in range(len(_context)):
            payload += f"vText{i + 2}={requests.utils.requote_uri(reverse_context[i])}&"

        self.context.append(message)
        
        payload += "cb_settings_scripting=no&islearning=1&icognoid=wsf&icognocheck="
        
        payload += hashlib.md5(payload[7:33].encode()).hexdigest()

        print("[DEBUG] Payload: ", payload)
        response = requests.post(
            CLEVERBOT_API_URL,
            cookies=cookies,
            data=payload,
        )

        print("[DEBUG] Response: ", response.content)
        print("[DEBUG] Context: ", self.context)
        response = re.split(r"\\r", str(response.content))[0]
        response = response[2:-1]

        self.context.append(response)
        return response
