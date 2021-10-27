import hackvm_codewriter
from hackvm_parser import *
import re
import pathlib
import sys


def main():
    args = sys.argv
    source_path = pathlib.Path(args[1])

    if not source_path.exists:
        raise ValueError(f'{str(source_path)} does not exist')

    if source_path.is_file():
        transrate(source_path)
    else:
        for source_file in source_path.glob('*.vm'):
            transrate(source_file)


def transrate(source_file):
    parser = HackVMParser(source_file)
    new_file = pathlib.Path(re.sub(r'.vm', '.asm', str(source_file)))
    code_writer = hackvm_codewriter.HackVMCodeWriter(new_file)

    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == CommandType.C_ARITHMETIC:
            code_writer.writeArithmetic(parser.arg1())
        elif parser.command_type() == CommandType.C_PUSH:
            code_writer.writePushPop('push', parser.arg1(), parser.arg2())

    code_writer.close()


if __name__ == "__main__":
    main()
