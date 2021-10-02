from hack_parser import *
import hack_code
import hack_symbol_table
import pathlib
import re

number_pattern = re.compile(r'[0-9]+')


def main():
    path = pathlib.Path(input())
    new_path = pathlib.Path(str(path).rstrip('asm')+'hack')
    parser = HackParser(path)
    symbol_table = hack_symbol_table.SymbolTable()

    current_rom_address = 0

    # 1回目のパス
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == L_COMMAND:
            symbol_table.add_entry(parser.symbol(), current_rom_address)
        elif parser.command_type() == C_COMMAND or parser.command_type() == A_COMMAND:
            current_rom_address += 1

    parser = HackParser(pathlib.Path(path))
    current_ram_address = 16
    line_count = 1
    binary_format = '015b'

    # 2回目のパス
    with open(new_path, mode='w', newline='\n') as f:
        while parser.has_more_commands():
            parser.advance()

            if parser.command_type() == A_COMMAND:
                if number_pattern.match(parser.symbol()):
                    f.write(f'0{format(int(parser.symbol()),binary_format)}\n')
                else:
                    if symbol_table.contains(parser.symbol()):
                        f.write(
                            f'0{format(int(symbol_table.get_address(parser.symbol())),binary_format)}\n')
                    else:
                        symbol_table.add_entry(
                            parser.symbol, current_ram_address)
                        current_ram_address += 1

            if parser.command_type() == C_COMMAND:
                comp = hack_code.HackCode.comp(parser.comp())
                dest = hack_code.HackCode.dest(parser.dest())
                jump = hack_code.HackCode.jump(parser.jump())
                f.write(f'111{comp}{dest}{jump}\n')

            if parser.command_type == NOT_A_HACK_ASSEMBLY_COMMAND:
                raise Exception(f'syntax error at line {line_count}')
            line_count += 1


if __name__ == '__main__':
    main()
