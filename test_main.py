import random
import unittest


import main


class RandomNickTest(unittest.TestCase):

    def setUp(self):
        random.seed(12345)

    def test_nick_starts_with_base(self):
        nick = main.random_nick("base")
        self.assertTrue(nick.startswith("base"))

    def test_nick_unique_among_20(self):
        nicks = [main.random_nick("base") for _ in range(20)]
        self.assertEqual(len(nicks), len(set(nicks)))


if __name__ == '__main__':
    unittest.main()
