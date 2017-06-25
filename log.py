import sys


# Colors
RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD = "\033[;1m"
REVERSE = "\033[;7m"

INFO = 'info'
DEBUG = 'debug'
IMPORTANT = 'important'
FINAL = 'final'

NEWLINE = True


class Log:
    def __init__(self, debug=False):
        self.debug = debug

    def log(self, message_type, message, new_line=False):
        if message_type == INFO and self.debug:
            sys.stdout.write(CYAN)
            print("[INFO]: %s" % message)
        if message_type == DEBUG and self.debug:
            sys.stdout.write(GREEN)
            print("[DEBUG]: %s" % message)
        if message_type == IMPORTANT and self.debug:
            sys.stdout.write(RED)
            print("[IMPORTANT]: %s" % message)
        if message_type == FINAL:
            sys.stdout.write(BLUE)
            print("[FINAL]: %s" % message)
        if new_line:
            print("########################### ~~ ###########################")
        sys.stdout.write(RESET)
