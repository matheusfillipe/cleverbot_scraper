import codecs
import hashlib
import re
from typing import List

import requests

from .constants import CLEVERBOT_API_URL, CLEVERBOT_URL


class Cleverbot:
    """
    Cleverbot api wrapper

    Attributes
    ----------
    cookies : dict
        Cookies to be used in the requests.
    context : list
        List of strings to be used as the initial chat messages with the bot.

    Methods
    ----------
    send(message)
        Sends a message to Cleverbot and returns the response as a string.
    """

    def __init__(self, context: List[str] = []):
        """__init__.

        :param context: List of strings to be used as the initial chat messages with the bot.
        :type context: List[str]
        """
        self.cookies = None
        self.context = context

        self._get_cookies()

    def _get_cookies(self):
        """_get_cookies."""
        if self.cookies is None:
            response = requests.get(CLEVERBOT_URL)
            self.cookies = {
                "XVIS": re.search(r"\w+(?=;)", response.headers["Set-cookie"]).group()
            }

    def send(self, message: str) -> str:
        """Sends a message to Cleverbot and returns the response as a string.

        :param message: The message to send to Cleverbot.
        :type message: str
        :rtype: str
        """
        payload = f"stimulus={requests.utils.requote_uri(message)}&"
        _context = self.context[:]
        reverse_context = list(reversed(_context))

        # Clear context list to keep things short and fast
        self._clear_context()
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
            self._get_cookies()

        response = re.split(r"\\r", str(response.content))[0]
        response = response[2:-1]

        # Append bot's response to the context
        self.context.append(response)
        return codecs.escape_decode(bytes(response, "utf-8"))[0].decode("utf-8")

    def _clear_context(self):
        """_clear_context."""
        if len(self.context) > 15:
            self.context.pop(0)
