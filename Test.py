from TwitchIrcBot import TwitchIrcBot
import config


def add_chat_interaction(cls):
    def decorator(func):
        cls.chat_interactions.append(func)
        return func

    return decorator


if __name__ == '__main__':
    MyBot = TwitchIrcBot(config.CHANNEL, config.NICK, config.PASS)

     # Adding some chat interaction scenario
    @add_chat_interaction(MyBot)
    def check_user_subscription(chat_message):
        # After sending message 'Am i Subscriber?', bot will give you an answer
        if chat_message.message == "Am I Subscriber?":
            if chat_message.is_sub_message():
                return "@{} Yes, you are.".format(chat_message.username)
            else:
                return "@{} No, you're not".format(chat_message.username)


    # Starting bot
    MyBot.start()
