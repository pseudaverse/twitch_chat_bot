from IrcBot import SimpleIrcBot
from TwitchChat import parse_raw_response
from TwitchChat import mess
import utils
import config


class TwitchIrcBot(SimpleIrcBot):
    def __init__(self, channel, nickname, password):
        super().__init__(config.HOST, channel, nickname, password, config.PORT)


class CamilleBot(TwitchIrcBot):
    def __init__(self, channel, nickname, password):
        super().__init__(channel, nickname, password)

    def _start_requests(self):
        self.socket.send("PASS {}\r\n".format(self.password).encode("utf-8"))
        self.socket.send("NICK {}\r\n".format(self.nickname).encode("utf-8"))
        self.socket.send("JOIN #{}\r\n".format(self.channel).encode("utf-8"))

        self.socket.send("CAP REQ :{}\r\n".format(config.TAGS_HOST).encode("utf-8"))

    def _check_on_connected(self, response):
        if response:
            response = self.socket.recv(1024).decode("utf-8")
            return response.endswith(':tmi.twitch.tv CAP * ACK :{}\r\n'.format(config.TAGS_HOST))
        return False

    def _process_response(self, response):
        try:
            if config.DEBUG:
                print(response)

            chat_message = parse_raw_response(response)

            bot_message = self._get_bot_message(chat_message)
            if bot_message:
                mess(self.socket, bot_message, self.channel)

        except:
            print("Something went wrong with processing response : {}".format(response))

    def _get_bot_message(self, chat_message):
        # After sending message 'Am i Subscriber?', bot will give you an answer
        if chat_message.message == "Am I Subscriber?":
            if chat_message.is_sub_message():
                return "@{} Yes, you are.".format(chat_message.username)
            else:
                return "@{} No, you're not".format(chat_message.username)
        
