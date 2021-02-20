from typing import Any
from colorama import Fore, Style, init


# initialize colorama for make ansi codes works in Windows
init()


INFO = Fore.LIGHTWHITE_EX + Style.NORMAL
WARNING = Fore.YELLOW
CRITICAL = Fore.YELLOW + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
DEBUG = Fore.CYAN + Style.BRIGHT
TEST = Fore.MAGENTA + Style.BRIGHT
NOTIFICATION = Fore.BLUE + Style.BRIGHT


class Logger:
    @staticmethod
    def colorize_message(
            color: str,
            label: str,
            *messages: Any,
            separator: str = ' '
    ):
        return f'{color}{label}{Style.RESET_ALL} ' \
               f'{separator.join([f"{message}" for message in messages])}'

    @staticmethod
    def info(*messages: Any):
        print(Logger.colorize_message(INFO, '[INFO]', *messages))

    @staticmethod
    def warning(*messages: Any):
        print(Logger.colorize_message(WARNING, '[WARNING]', *messages))

    @staticmethod
    def critical(*messages: Any):
        print(Logger.colorize_message(CRITICAL, '[CRITICAL]', *messages))

    @staticmethod
    def error(*messages: Any):
        print(Logger.colorize_message(ERROR, '[ERROR]', *messages))

    @staticmethod
    def success(*messages: Any):
        print(Logger.colorize_message(SUCCESS, '[SUCCESS]', *messages))

    @staticmethod
    def debug(*messages: Any):
        print(Logger.colorize_message(DEBUG, '[DEBUG]', *messages))
