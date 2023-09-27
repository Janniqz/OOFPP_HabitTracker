from enum import Enum


class TerminalColor(Enum):
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


class TerminalFormat(Enum):
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
