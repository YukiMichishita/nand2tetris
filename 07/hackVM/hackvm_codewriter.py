from hackvm_commands import *
import os


class HackVMCodeWriter:

    def __init__(self, output_file_path):
        self.output_file = open(output_file_path, 'w', newline='\n')
        self.command_counter = 0

    def setFileName(self, output_file_path):
        self.output_file.close()
        self.output_file = open(output_file_path, 'w', newline='\n')

    def writeArithmetic(self, command):
        self.output_file.write(f'//{command}\n')
        if command in arithmetic_commands.keys():
            self.output_file.writelines(
                arithmetic_commands[command](self.command_counter))
        else:
            raise ValueError(f'{str(command)} is not a HackVM command')
        self.command_counter += 1

    def writePushPop(self, command, segment, index):
        self.output_file.write(f'//{command} {segment} {index} \n')
        file_name_without_ext = os.path.splitext(
            os.path.basename(self.output_file.name))[0]
        if command == 'push':
            if segment in push_commands.keys():
                self.output_file.writelines(
                    push_commands[segment](index, file_name_without_ext))
            else:
                raise ValueError(f'{segment} is not a segment')
        if command == 'pop':
            if segment in pop_commands.keys():
                self.output_file.writelines(
                    pop_commands[segment](index, file_name_without_ext))
            else:
                raise ValueError(f'{segment} is not a segment')

    def close(self):
        self.output_file.writelines(end)
        self.output_file.close()
