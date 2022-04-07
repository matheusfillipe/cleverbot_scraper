# Cleverbot Scraper

Simple free cleverbot library that doesn't require running a heavy ram wasting headless web browser to actually chat with the bot, only relying on the requests module. The api is wrapped by the `Cleverbot` class and you can use the `send` module to receive responses from cleverbot.

## Try it

Install and test with:
```bash
pip3 install cleverbot-scraper
python3 -m cleverbot
```
The last command will start a live session with the cleverbot.

You can also make cleverbot chat with itself with:
```bash
python3 -m cleverbot auto
```

## Examples

### Chat with the bot

```python
from cleverbot import Cleverbot
bot = Cleverbot()
print("Start the conversation, press Ctrl-c to stop \n")
try:
    while True:
        print(bot.send(input(">> ")))
except KeyboardInterrupt:
    print("Exiting.")
```

### Make the bot chat with itself

```python
from cleverbot import Cleverbot
alice = Cleverbot()
bob = Cleverbot()
message = "Hi there! How are you doing?"
print("Press Ctrl-c to stop \n")
try:
    while True:
        print("Bob: ", message)
        message = alice.send(message)
        print("Alice: ", message)
        message = bob.send(message)
except KeyboardInterrupt:
    print("Exiting.")
```
### Use proxies

If cleverbot.com is returning 403 errors for you you might want to use a proxy:
```python

from cleverbot import Cleverbot
bot = Cleverbot(proxies={'http': 'http://x.x.x.x:yyyy', 'https': 'http://x.x.x.x:yyyy'})
while True: print(bot.send(input(">> ")))
```
You can also simply pass a list of `ip:port`:

```python
from cleverbot import Cleverbot
PROXIES = [
    None,
    "x.x.x.x:yyyy",
    "x.x.x.x:yyyy",
    "x.x.x.x:yyyy",
    "x.x.x.x:yyyy",
    "x.x.x.x:yyyy",
]
bot = Cleverbot(proxies=PROXIES)
while True: print(bot.send(input(">> ")))
```

### Use tor as a fallback

Requires [torpy](https://github.com/torpyorg/torpy) with requests extra:

`pip3 install torpy[requests]`

```python

from cleverbot import Cleverbot
bot = Cleverbot(use_tor_fallback = True)
while True: print(bot.send(input(">> ")))
```


