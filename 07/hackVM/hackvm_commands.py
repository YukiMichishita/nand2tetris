line_feed = '\n'


def binary_operation_command(operation):
    def return_func(_):
        return [command + line_feed for command in
                ['@SP', 'M=M-1', 'A=M', 'D=M', 'M=0', '@SP', 'M=M-1', 'A=M', operation, '@SP', 'M=M+1']]
    return return_func


def unary_operation_command(operation):
    def return_func(_):
        return [command + line_feed for command in
                ['@SP', 'M=M-1', 'A=M', operation, '@SP', 'M=M+1']]
    return return_func


def compare_command(compare_str):
    def _compare(counter):
        return [command + line_feed for command in
                ['@SP', 'M=M-1', 'A=M', 'D=M', 'M=0', '@SP', 'M=M-1', 'A=M', 'D=M-D', f'@TRUE{counter}',
                 compare_str, '@SP', 'A=M', 'M=0', f'@FALSE{counter}', '0;JMP', f'(TRUE{counter})', '@SP',
                 'A=M', 'M=-1', f'(FALSE{counter})', '@SP', 'M=M+1']]
    return _compare


def constant_push_command(index, _):
    return [s + line_feed for s in [
        f'@{index}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', ]]


def arg_local_this_that_push_command(segment):
    def return_func(index, _):
        return [command + line_feed for command in
                [f'@{index}', 'D=A', segment, 'A=M+D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']]
    return return_func


def arg_local_that_this_pop_command(segment):
    def return_func(index, _):
        return [command + line_feed for command in
                [f'@{index}', 'D=A', segment, 'M=M+D', '@SP', 'M=M-1', 'A=M', 'D=M', segment, 'A=M',
                 'M=D', f'@{index}', 'D=A', segment, 'M=M-D']]
    return return_func


def pointer_temp_push_command(segment):
    def return_func(index, _):
        label = '@R' + str(int(segment)+int(index))
        return [command + line_feed for command in
                [label, 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']]
    return return_func


def pointer_temp_pop_command(segment):
    def return_func(index, _):
        label = '@R' + str(int(segment)+int(index))
        return [command + line_feed for command in
                ['@SP', 'M=M-1', 'A=M', 'D=M', label, 'M=D', ]]
    return return_func


def static_push_command(index, file_name):
    return [command + line_feed for command in
            [f'@{file_name}.{index}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']]


def static_pop_command(index, file_name):
    return [command + line_feed for command in
            ['@SP', 'M=M-1', '@SP', 'A=M', 'D=M', f'@{file_name}.{index}', 'M=D', ]]


arithmetic_commands = {
    'add': binary_operation_command('M=M+D'),
    'sub': binary_operation_command('M=M-D'),
    'and': binary_operation_command('M=M&D'),
    'or':  binary_operation_command('M=M|D'),
    'neg': unary_operation_command('M=-M'),
    'not': unary_operation_command('M=!M'),
    'eq': compare_command('D;JEQ'),
    'gt': compare_command('D;JGT'),
    'lt': compare_command('D;JLT'),
}

push_commands = {
    'constant': constant_push_command,
    'argument': arg_local_this_that_push_command('@ARG'),
    'local': arg_local_this_that_push_command('@LCL'),
    'this': arg_local_this_that_push_command('@THIS'),
    'that': arg_local_this_that_push_command('@THAT'),
    'pointer': pointer_temp_push_command('3'),
    'temp': pointer_temp_push_command('5'),
    'static': static_push_command}

pop_commands = {
    'argument': arg_local_that_this_pop_command('@ARG'),
    'local': arg_local_that_this_pop_command('@LCL'),
    'this': arg_local_that_this_pop_command('@THIS'),
    'that': arg_local_that_this_pop_command('@THAT'),
    'pointer': pointer_temp_pop_command('3'),
    'temp': pointer_temp_pop_command('5'),
    'static': static_pop_command}

end = [s + line_feed for s in ['(END)', '@END', '0;JMP']]
