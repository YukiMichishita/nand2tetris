import itertools
line_feed = '\n'


def init_command():
    return [command + line_feed for command in
            ['@261//init', 'D=A', '@SP', 'M=D']] +\
        goto_command('Sys.init_base_address')


def binary_operation_command(operation):
    def return_func(_):
        return [command + line_feed for command in
                [f'@SP//{operation}', 'M=M-1', 'A=M', 'D=M', 'M=0', '@SP', 'M=M-1', 'A=M', operation, '@SP', 'M=M+1']]
    return return_func


def unary_operation_command(operation):
    def return_func(_):
        return [command + line_feed for command in
                [f'@SP//{operation}', 'M=M-1', 'A=M', operation, '@SP', 'M=M+1']]
    return return_func


def compare_command(compare_str):
    def _compare(counter):
        return [command + line_feed for command in
                [f'@SP//{compare_str} {counter}', 'M=M-1', 'A=M', 'D=M', 'M=0', '@SP', 'M=M-1', 'A=M', 'D=M-D', f'@TRUE{counter}',
                 compare_str, '@SP', 'A=M', 'M=0', f'@FALSE{counter}', '0;JMP', f'(TRUE{counter})', '@SP',
                 'A=M', 'M=-1', f'(FALSE{counter})', '@SP', 'M=M+1']]
    return _compare


def constant_push_command(index, _):
    return [s + line_feed for s in [
        f'@{index}//constant {index}', 'D=A', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1', ]]


def arg_local_this_that_push_command(segment):
    def return_func(index, _):
        return [command + line_feed for command in
                [f'@{index}//push {segment} {index}', 'D=A', segment, 'A=M+D', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']]
    return return_func


def arg_local_that_this_pop_command(segment):
    def return_func(index, _):
        return [command + line_feed for command in
                [f'@{index}//pop {segment} {index}', 'D=A', segment, 'M=M+D', '@SP', 'M=M-1', 'A=M', 'D=M', segment, 'A=M',
                 'M=D', f'@{index}', 'D=A', segment, 'M=M-D']]
    return return_func


def pointer_temp_push_command(segment):
    def return_func(index, _):
        label = '@R' + str(int(segment)+int(index))
        return [command + line_feed for command in
                [f'{label}//{segment, index}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']]
    return return_func


def pointer_temp_pop_command(segment):
    def return_func(index, _):
        label = '@R' + str(int(segment)+int(index))
        return [command + line_feed for command in
                [f'@SP//{segment, index}', 'M=M-1', 'A=M', 'D=M', label, 'M=D', ]]
    return return_func


def static_push_command(index, file_name):
    return [command + line_feed for command in
            [f'@{file_name}.{index}', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1']]


def static_pop_command(index, file_name):
    return [command + line_feed for command in
            ['@SP//pop static', 'M=M-1', '@SP', 'A=M', 'D=M', f'@{file_name}.{index}', 'M=D', ]]


def label_command(label):
    return [command + line_feed for command in
            [f'({label})']]


def goto_command(label):
    return [command + line_feed for command in
            [f'@{label}//goto {label}', '0;JMP']]


def if_goto_command(label):
    return [command + line_feed for command in
            [f'@SP//if_goto{label}', 'M=M-1', 'A=M', 'D=M', f'@{label}', 'D;JNE']]


def call_command(function_name, num_args, counter):
    return constant_push_command(f'call_{function_name}_return_address{counter}', '') +\
        [command + line_feed for command in [
            '@LCL', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
            '@ARG', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
            '@THIS', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
            '@THAT', 'D=M', '@SP', 'A=M', 'M=D', '@SP', 'M=M+1',
        ]] +\
        [command + line_feed for command in
         [
             # ARG = SP - num_args - 5
             '@SP', 'D=M', f'@{int(num_args)+5}', 'D=D-A', '@ARG', 'M=D',
             # LCL = SP
             '@SP', 'D=M', '@LCL', 'M=D'
         ]] +\
        goto_command(f'{function_name}_base_address') +\
        label_command(f'call_{function_name}_return_address{counter}')


def return_command():
    return [command + line_feed for command in
            ['@LCL',  'D=M-1', 'D=D-1', 'D=D-1', 'D=D-1', 'D=D-1', 'A=D', 'D=M', '@R13', 'M=D']] +\
        arg_local_that_this_pop_command('@ARG')(0, '') +\
        [command + line_feed for command in
         [
             '@ARG',  'D=M+1', '@SP', 'M=D',
             '@LCL',  'D=M-1', 'A=D', 'D=M', '@THAT', 'M=D',
             '@LCL',  'D=M-1', 'D=D-1', 'A=D', 'D=M', '@THIS', 'M=D',
             '@LCL',  'D=M-1', 'D=D-1', 'D=D-1', 'A=D', 'D=M', '@ARG', 'M=D',
             '@LCL',  'D=M-1', 'D=D-1', 'D=D-1', 'D=D-1', 'A=D', 'D=M', '@LCL', 'M=D',
             '@R13',  'A=M',   '0;JMP']]


def function_command(function_name, num_locals):
    return label_command(f'{function_name}_base_address') +\
        list(itertools.chain.from_iterable([[command for command in constant_push_command(
            '0', '')] for _ in range(int(num_locals))]))


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
