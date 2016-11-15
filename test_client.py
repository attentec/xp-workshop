import unittest

import client


class ClientTest(unittest.TestCase):

    def setUp(self):
        self.client = client.Client(nick="xpguru")

    def test_type_quit(self):
        actions = self.client.on_keyboard("/quit")
        self.assertEqual(actions, [("send", "QUIT")])

    def test_receive_quit(self):
        actions = self.client.on_network("QUIT")
        self.assertEqual(actions, [("exit", )])

    def test_receive_ping(self):
        actions = self.client.on_network("PING abc")
        self.assertEqual(actions, [("send", "PONG abc")])

    def test_receive_unknown(self):
        actions = self.client.on_network("NONSENSE")
        self.assertEqual(actions, [])

    def test_send_nick_on_connect(self):
        actions = self.client.on_connect()
        self.assertEqual(actions, [
            ("send", "NICK xpguru"),
            ("send", "USER xpguru 0 * xpguru"),
            ("print", "Connecting as xpguru"),
        ])

    def test_autojoin_xp_channel(self):
        line = ":example.com 375 :server message of the day"
        actions = self.client.on_network(line)
        self.assertEqual(actions, [("send", "JOIN #xp")])

if __name__ == '__main__':
    unittest.main()
