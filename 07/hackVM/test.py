import re
from enum import Enum, auto
from abc import ABCMeta, abstractmethod


class Command():
    def __init__(self, regex_pattern, arg_length):
        self.regex_pattern = re.compile(regex_pattern)
        self.arg_length = arg_length


class CommandType():
    C_ARITHMETIC = Command(r'(add|sub|neg|eq|gt|lt|and|or|not)', 0)
    C_PUSH = Command(
        fr'(push)\s*(argument|local|static|constant|this|that|pointer|temp)\s*\d+', 2)
    C_POP = Command(
        fr'(pop)\s*(argument|local|static|constant|this|that|pointer|temp)\s*\d+', 2)
    C_LABEL = Command(r'', 1)
    C_GOTO = Command(r'', 1)
    C_IF = Command(r'', 1)
    C_FUNCTION = Command(r'', 2)
    C_RETURN = Command(r'', 0)
    C_CALL = Command(r'', 2)
    COMMENT = Command(r'//.*', 0)


print(CommandType)
print(CommandType.COMMENT.regex_pattern)
