from .cleverbot import Cleverbot

c = Cleverbot()

if __name__ == "__main__":
    print("Start the conversation, press Ctrl-c to stop \n")
    try:
        while True:
            user_input = input(">> ")
            print("Bot: ", c.post_message(user_input))
    except KeyboardInterrupt:
        print("Exiting.")
