import hackvm_codewriter
from hackvm_parser import *
import os
import re
import pathlib
import sys


def main(path_str):
    source_path = pathlib.Path(path_str)

    if not source_path.exists:
        raise ValueError(f'{str(source_path)} does not exist')

    if source_path.is_file():
        output_file = pathlib.Path(re.sub(r'.vm', '.asm', str(source_path)))
        code_writer = hackvm_codewriter.HackVMCodeWriter(output_file)
        code_writer.set_source_file_name(source_path)
        code_writer.write_init()
        transrate(code_writer, source_path)
    else:
        output_file = pathlib.Path(
            str(source_path) + '/' + os.path.split(source_path)[-1]+'.asm')
        code_writer = hackvm_codewriter.HackVMCodeWriter(output_file)
        code_writer.write_init()
        for source_file in source_path.glob('*.vm'):
            code_writer.set_source_file_name(source_file)
            transrate(code_writer, source_file)
    code_writer.close()


def transrate(code_writer, source_file):
    parser = HackVMParser(source_file)

    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == CommandType.C_ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1())
        elif parser.command_type() == CommandType.C_PUSH:
            code_writer.write_push_pop('push', parser.arg1(), parser.arg2())
        elif parser.command_type() == CommandType.C_POP:
            code_writer.write_push_pop('pop', parser.arg1(), parser.arg2())
        elif parser.command_type() == CommandType.C_LABEL:
            code_writer.write_label(parser.arg1())
        elif parser.command_type() == CommandType.C_GOTO:
            code_writer.write_goto(parser.arg1())
        elif parser.command_type() == CommandType.C_IF:
            code_writer.write_if(parser.arg1())
        elif parser.command_type() == CommandType.C_CALL:
            code_writer.write_call(parser.arg1(), parser.arg2())
        elif parser.command_type() == CommandType.C_FUNCTION:
            code_writer.write_function(parser.arg1(), parser.arg2())
        elif parser.command_type() == CommandType.C_RETURN:
            code_writer.write_return()


if __name__ == "__main__":
    args = sys.argv
    main(args[1])
