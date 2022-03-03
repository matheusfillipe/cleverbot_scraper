from .cleverbot import Cleverbot

alice = Cleverbot()
bob = Cleverbot()

message = "Hello there, bitch"

if __name__ == "__main__":
    print("Start the conversation, press Ctrl-c to stop \n")
    try:
        while True:
            message = alice.post_message(message)
            print("Alice: ", message)
            message = bob.post_message(message)
            print("Bob: ", message)
    except KeyboardInterrupt:
        print("Exiting.")
