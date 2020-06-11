from IrcBot import SimpleIrcBot
from TwitchChat import parse_raw_response
from TwitchChat import mess
import config


# Example of Bot which using Twitch Tags and can check if chat user is subscriber or not
class TwitchIrcBot(SimpleIrcBot):
    def __init__(self, channel, nickname, password):
        super().__init__(config.HOST, channel, nickname, password, config.PORT)
        self.chat_interactions = []

    def _start_requests(self):
        self.socket.send("PASS {}\r\n".format(self.password).encode("utf-8"))
        self.socket.send("NICK {}\r\n".format(self.nickname).encode("utf-8"))
        self.socket.send("JOIN #{}\r\n".format(self.channel).encode("utf-8"))

        # adding IRC V3 message twitch tags
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

            for f in self.chat_interactions:
                bot_message = f(chat_message)
                if bot_message:
                    mess(self.socket, bot_message, self.channel)
                    break

        except:
            print("Something went wrong with processing response : {}".format(response))
