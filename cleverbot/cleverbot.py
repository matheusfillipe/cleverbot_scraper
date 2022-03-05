import codecs
import hashlib
import logging
import re
import time
from typing import List, Union

import requests

from .constants import (CLEVERBOT_API_URL, CLEVERBOT_URL, DEBOUNCE_TIME,
                        MAX_ATTEPTS, MAX_CONTEXT_LENGTH, MAX_DEBOUNCE_ATTEMPS)


class Cleverbot:
    """
    Cleverbot api wrapper

    Attributes
    ----------
    cookies : dict
        Cookies to be used in the requests.
    context : list
        List of messages representing the context of the conversation.
    proxies :
        Proxy to be used or proxies to rotate through.
    debounce: bool
        Whether to try to debounce the requests or not. If set to False it will try to use proxies immediately upon failure.

    Methods
    ----------
    send(message)
        Sends a message to Cleverbot and returns the response as a string.
    """

    def __init__(
        self,
        context: List[str] = [],
        proxies: Union[dict, List[dict], List[str]] = None,
        debounce: bool = True,
    ):
        """
        Cleverbot Constructor

        :param context List[str]:List of strings to be used as the initial chat messages with the bot.
        :param proxies dict: Must have keys "http" and "https" and values of the proxies address:port to be used on the requests library format. You can also pass a list of proxies to rotate through. If an element of the list is None, it means not to use any proxy.
        :param debounce bool: Whether to try to debounce the requests or not. If set to False it will try to use proxies immediately upon failure.
        """
        self.cookies = None
        self.context = context
        self.proxies = proxies
        self.debounce = debounce

        if proxies is None:
            self.proxies = [None]
        elif isinstance(proxies, dict):
            self.proxies = [proxies]
        elif isinstance(proxies, list):
            self.proxies = []
            for proxy in proxies:
                if isinstance(proxy, dict):
                    self.proxies.append(proxy)
                elif isinstance(proxy, str):
                    self.proxies.append({"http": proxy, "https": proxy})
                else:
                    raise ValueError(
                        "Invalid proxy format. Must be a dict, a list of dicts or a list of strings."
                    )
        else:
            raise ValueError(
                "Invalid proxy format. Must be a dict, a list of dicts or a list of strings."
            )

        self._proxy_index = 0
        self._debounce_attempts = 0
        self._proxy = self.proxies[0]
        self._attempts = 0

        self._refresh_cookies()

    def _refresh_cookies(self):
        """Refresh the cookies"""
        response = requests.get(CLEVERBOT_URL, proxies=self._proxy)
        self.cookies = {
            "XVIS": re.search(r"\w+(?=;)", response.headers["Set-cookie"]).group()
        }

    def send(self, message: str) -> str:
        """
        Sends a message to Cleverbot and returns the response as a string.

        :param message str: The message to send to Cleverbot.
        :rtype str: Message received from Cleverbot.
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
            proxies=self._proxy,
        )

        # If the request is not succesful, refresh cookies, debounce, try a new proxy
        if response.status_code != 200:
            if self._attempts > len(self.proxies) + MAX_ATTEPTS:
                logging.error(
                    f"Cleverbot failed to respond after {self._attempts} attempts. Giving up."
                )
                self._attempts = 0
                # TODO: Raise exception? Return None? idk
                return ""

            self._refresh_cookies()
            if self._debounce_attempts >= MAX_DEBOUNCE_ATTEMPS or not self.debounce:
                self._debounce_attempts = 0
                self._proxy_index += 1
                if self._proxy_index >= len(self.proxies):
                    self._proxy_index = 0
                logging.info(
                    f"Cleverbot failed to respond. Trying proxy {self.proxies[self._proxy_index]}"
                )
                self._proxy = self.proxies[self._proxy_index]

            elif self.debounce:
                self._debounce_attempts += 1
                logging.info(
                    f"Cleverbot failed to respond. Trying again in {DEBOUNCE_TIME * self._debounce_attempts} seconds."
                )
                time.sleep(DEBOUNCE_TIME * self._debounce_attempts)

            self.context.pop()
            self._attempts += 1
            return self.send(message)

        response = re.split(r"\\r", str(response.content))[0]
        response = response[2:-1]
        self._attempts = 0

        # Append bot's response to the context
        self.context.append(response)
        return codecs.escape_decode(bytes(response, "utf-8"))[0].decode("utf-8")

    def _clear_context(self):
        """_clear_context."""
        if len(self.context) >= MAX_CONTEXT_LENGTH:
            self.context.pop(0)
