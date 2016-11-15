from random import randint
import os
import socket as socketlib
import sys
import threading

from client import Client


VERBOSE = True


def debug(message):
    if VERBOSE:
        print(message, flush=True)


def exit_all_threads(status):
    # Hack-ish way to stop all threads (does not cleanup). Is part of
    # the official API though.
    os._exit(status)  # pylint: disable=protected-access


def random_nick(nick_base):
    return "{}_{:06}".format(nick_base, randint(0, 999999))


def process_lines(name, socket, lock, lines, callback):
    debug("starting {} thread".format(name))
    for line in lines:
        line = line.strip()
        debug("{}   --> {}".format(name, line))
        with lock:
            actions = callback(line)
            perform(actions, socket)
    debug("stopping {} thread".format(name))
    exit_all_threads(0)


def perform(actions, socket):
    for action in actions:
        command = action[0]
        if command == "send":
            line = action[1]
            debug("net <--   {}".format(line))
            line = line.encode("utf-8", errors="replace") + b"\r\n"
            socket.sendall(line)
        elif command == "print":
            line = action[1]
            print(line, flush=True)
        elif command == "exit":
            exit_all_threads(0)
        else:
            raise ValueError(action)


def main():
    host = "irc.raek.se"
    port = 6667

    lock = threading.Lock()
    socket = socketlib.socket()
    socket.connect((host, port))

    nick = random_nick("xpguru")
    client = Client(nick=nick)
    actions = client.on_connect()
    perform(actions, socket)

    def network_main():
        lines = socket.makefile(encoding="utf-8", errors="replace")
        process_lines("net", socket, lock, lines, client.on_network)

    def keyboard_main():
        lines = sys.stdin
        process_lines("keyboard", socket, lock, lines, client.on_keyboard)

    threading.Thread(target=network_main).start()
    threading.Thread(target=keyboard_main).start()


if __name__ == '__main__':
    main()
