from hackvm_commands import *
import os


class HackVMCodeWriter:

    def __init__(self, output_file_path):
        self.output_file = open(output_file_path, 'w', newline='\n')
        self.command_counter = 0

    def set_file_name(self, output_file_path):
        self.output_file.close()
        self.output_file = open(output_file_path, 'w', newline='\n')

    def set_source_file_name(self, source_file_name):
        self.souce_file = source_file_name

    def write_init(self):
        # print()
        # self.output_file.write('//init\n')
        self.output_file.writelines(init_command())

    def write_arithmetic(self, command):
        # self.output_file.write(f'//{command}\n')
        if command in arithmetic_commands.keys():
            self.output_file.writelines(
                arithmetic_commands[command](self.command_counter))
        else:
            raise ValueError(f'{str(command)} is not a HackVM command')
        self.command_counter += 1

    def write_push_pop(self, command, segment, index):
        # self.output_file.write(f'//{command} {segment} {index} \n')
        file_name_without_ext = os.path.splitext(
            os.path.basename(str(self.souce_file)))[0]
        if command == 'push':
            if segment in push_commands.keys():
                self.output_file.writelines(
                    push_commands[segment](index, file_name_without_ext))
                return
        if command == 'pop':
            if segment in pop_commands.keys():
                self.output_file.writelines(
                    pop_commands[segment](index, file_name_without_ext))
                return
        raise ValueError(f'syntax error')

    def write_label(self, label):
        # self.output_file.write(f'//label {label} \n')
        self.output_file.writelines(label_command(label))

    def write_goto(self, label):
        # self.output_file.write(f'//goto {label}\n')
        self.output_file.writelines(goto_command(label))

    def write_if(self, label):
        # self.output_file.write(f'//if-goto {label}\n')
        self.output_file.writelines(if_goto_command(label))

    def write_call(self, function_name, num_args):
        # self.output_file.write(f'//call {function_name} {num_args}\n')
        self.output_file.writelines(call_command(
            function_name, num_args, self.command_counter))
        self.command_counter += 1

    def write_return(self):
        # self.output_file.write(f'//return \n')
        self.output_file.writelines(return_command())

    def write_function(self, function_name, num_locals):
        # self.output_file.write(f'//function {function_name} {num_locals}\n')
        self.output_file.writelines(
            function_command(function_name, num_locals))

    def close(self):
        self.output_file.close()
