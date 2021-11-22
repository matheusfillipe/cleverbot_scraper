# Cleverbot Scrapper Lib

Simple free cleverbot library that doesn't require running a heavy ram wasting headless web browser to actually chat with the bot, all that it uses is the requests module. Also supports simultaneously different sessions, which means, different parallel conversations.

## Try it


Install and test with:
```bash
pip3 install cleverbot-scrapper
python3 -m "cleverbot"
```
The last command will start a live session with the cleverbot(for testing purposes).


## Example
```python
from cleverbot import cleverbot
# With context and session
# An ongoing conversation with the first question as "How are you?"
print("How are you?")
print(cleverbot(input(">>"), ["hi.", "How are you?"], "How are you?"))
while True:
    print(cleverbot(input(">>"), session="How are you?"))

```
