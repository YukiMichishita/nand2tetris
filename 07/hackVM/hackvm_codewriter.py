def binary_operation_command(operation):
    return ['@SP',
            'M=M-1',
            'A=M',
            'D=M',
            'M=0',
            '@SP',
            'M=M-1',
            'A=M',
            operation,
            '@SP',
            'M=M+1'
            ]


def unary_operation_command(operation):
    return ['@SP',
            'M=M-1',
            'A=M',
            operation,
            '@SP',
            'M=M+1'
            ]


def compare_commands(counter, compare_str):
    return ['@SP',
            'M=M-1',
            'A=M',
            'D=M',
            'M=0',
            '@SP',
            'M=M-1',
            'A=M',
            'D=M-D',
            f'@TRUE{counter}',
            compare_str,
            '@SP',
            'A=M',
            'M=0',
            f'@FALSE{counter}',
            '0;JMP',
            f'(TRUE{counter})',
            '@SP',
            'A=M',
            'M=-1',
            f'(FALSE{counter})',
            '@SP',
            'M=M+1'
            ]


arithmetic_commands = {'binary_operation': {'add': 'M=M+D',
                                            'sub': 'M=M-D',
                                            'and': 'M=M&D',
                                            'or': 'M=M|D', },
                       'unary_operation': {'neg': 'M=-M',
                                           'not': 'M=!M', },
                       'compare': {'eq': 'D;JEQ',
                                   'gt': 'D;JGT',
                                   'lt': 'D;JLT', }
                       }

push_pop_commands = {'push_constant': [
    # 定数
    'D=A',
    '@SP',
    'A=M',
    'M=D',
    '@SP',
    'M=M+1',
]}

end = ['(END)', '@END', '0;JMP']


class HackVMCodeWriter:

    def __init__(self, output_file_path):
        self.output_file = open(output_file_path, 'w', newline='\n')
        self.command_counter = 0

    def setFileName(self, output_file_path):
        self.output_file.close()
        self.output_file = open(output_file_path, 'w', newline='\n')

    def writeArithmetic(self, command):
        self.output_file.write(f'//{command}\n')
        if command in arithmetic_commands['binary_operation'].keys():
            for s in binary_operation_command(arithmetic_commands['binary_operation'][command]):
                self.output_file.write(s+'\n')
        elif command in arithmetic_commands['unary_operation'].keys():
            for s in unary_operation_command(arithmetic_commands['unary_operation'][command]):
                self.output_file.write(s+'\n')
        elif command in arithmetic_commands['compare'].keys():
            for s in compare_commands(self.command_counter, arithmetic_commands['compare'][command]):
                self.output_file.write(s+'\n')
        else:
            raise ValueError(f'{str(command)} is not a HackVM command')

        self.command_counter += 1

    def writePushPop(self, command, segment, index):
        self.output_file.write(f'//{command} {segment} {index} \n')
        if command == 'push':
            if segment == 'constant':
                for s in [f'@{index}']+push_pop_commands['push_constant']:
                    self.output_file.write(s+'\n')

    def close(self):
        for s in end:
            self.output_file.write(s+'\n')
        self.output_file.close()
