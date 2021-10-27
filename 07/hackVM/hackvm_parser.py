import re
from enum import Enum, auto


class Command():
    def __init__(self, regex_pattern, arg_length):
        self.regex_pattern = re.compile(regex_pattern)
        self.arg_length = arg_length


class CommandType(Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()
    COMMENT = auto()


Commands = {
    CommandType.C_ARITHMETIC: Command(r'(add|sub|neg|eq|gt|lt|and|or|not)', 0),
    CommandType.C_PUSH:  Command(
        fr'(push)\s*(argument|local|static|constant|this|that|pointer|temp)\s*\d+', 2),
    CommandType.C_POP: Command(
        fr'(pop)\s*(argument|local|static|constant|this|that|pointer|temp)\s*\d+', 2),
    CommandType.C_LABEL: Command(r'', 1),
    CommandType.C_GOTO: Command(r'', 1),
    CommandType.C_IF: Command(r'', 1),
    CommandType.C_FUNCTION: Command(r'', 2),
    CommandType.C_RETURN: Command(r'', 0),
    CommandType.C_CALL: Command(r'', 2),
    CommandType.COMMENT: Command(r'//.*', 0)}


class HackVMParser:
    file_contents = []
    row_counter = -1
    current_line = ''
    current_command = ''

    def __init__(self, path):
        self.row_counter = -1
        self.current_line = ''
        self.current_command = ''
        with path.open() as file:
            self.file_contents = [s for s in file.readlines()]

    def has_more_commands(self):
        return self.row_counter < len(self.file_contents)-1

    def advance(self):
        self.row_counter += 1
        self.current_line = self.file_contents[self.row_counter]
        self.current_command = re.sub(
            Commands[CommandType.COMMENT].regex_pattern, '', self.current_line).strip()

    def command_type(self):
        for type_ in CommandType:
            if Commands[type_].regex_pattern.match(self.current_command):
                return type_

        return 'NOT_A_HACK_VM_COMMAND'

    def arg1(self):
        if self.command_type() == CommandType.C_ARITHMETIC:
            return Commands[CommandType.C_ARITHMETIC].regex_pattern.match(self.current_command).group()

        for type_ in CommandType:
            if type_ == self.command_type() and Commands[type_].arg_length > 0:
                return Commands[type_].regex_pattern.match(self.current_command).group().split()[1]

        return ''

    def arg2(self):
        for type_ in CommandType:
            if type_ == self.command_type() and Commands[type_].arg_length > 1:
                return Commands[type_].regex_pattern.match(self.current_command).group().split()[2]
