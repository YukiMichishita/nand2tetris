import unittest
import pathlib
import hack_parser
import hack_code


parser = hack_parser.HackParser(pathlib.Path(
    '/Users/yuki/dev/nand2tetris/projects/06/hackassembler/Test.asm'))
code = hack_code.HackCode

while parser.has_more_commands():
    parser.advance()
    print(f'{parser.current_command}  {parser.command_type()}')

    if parser.command_type() in ('A_COMMAND', 'L_COMMAND'):
        print(parser.symbol())
    if parser.command_type() == 'C_COMMAND':
        print(f'c_command:{parser.dest()} {parser.comp()} {parser.jump()}')
        print(
            f'code:{code.dest(parser.dest())} {code.comp(parser.comp())} {code.jump(parser.jump())}')
