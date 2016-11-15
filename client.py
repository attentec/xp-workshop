class Client:

    def __init__(self, nick):
        self.nick = nick

    def on_connect(self):
        return [
            ("send", "NICK {0}".format(self.nick)),
            ("send", "USER {0} 0 * {0}".format(self.nick)),
            ("print", "Connecting as {0}".format(self.nick)),
        ]

    def on_keyboard(self, _):
        return [("send", "QUIT")]

    def on_network(self, line):
        if "375" in line:
            return [("send", "JOIN #xp")]
        words = line.split(" ", maxsplit=1)
        command = words[0]
        if command == "QUIT":
            return [("exit", )]
        elif command == "PING":
            return [("send", "PONG " + words[1])]
        else:
            return []
