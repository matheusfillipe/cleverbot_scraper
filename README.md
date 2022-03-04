# Cleverbot Scraper

Simple free cleverbot library that doesn't require running a heavy ram wasting headless web browser to actually chat with the bot, only relying on the requests module. The api is wrapped by the `Cleverbot` class and you can use the `send` module to receive responses from cleverbot.

## Try it

Install and test with:
```bash
pip3 install cleverbot-scraper
python3 -m "cleverbot"
```
The last command will start a live session with the cleverbot(for testing purposes).


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
