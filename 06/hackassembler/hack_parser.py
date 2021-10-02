import re

# 命令の種類
A_COMMAND = 'A_COMMAND'
C_COMMAND = 'C_COMMAND'
L_COMMAND = 'L_COMMAND'
COMMENT = 'COMMENT'
NOT_A_HACK_ASSEMBLY_COMMAND = 'NOT_A_HACK_ASSEMBLY_COMMAND'

# 命令の正規表現
A_COMMAND_PATTERN = r'@.+'
C_COMMAND_COMP_PATTERN = r'([AMD01]|-1|-M|-D|-A|!M|!D|!A)([\+\-\&\|]([ADM01]))?'
C_COMMAND_DEST_PATTERN = r'([ADM]{1,3}=)'
C_COMMAND_JUMP_PATTERN = r'(;J(GT|EQ|GE|LT|NE|LE|MP))'
L_COMMAND_PATTERN = r'\(.+\)'
COMMENT_PATTERN = r'//.*'

# A命令にマッチ
a_command_pattern = re.compile(A_COMMAND_PATTERN)
# 全てのC命令にマッチ
c_command_pattern = re.compile(
    C_COMMAND_DEST_PATTERN+'?'+C_COMMAND_COMP_PATTERN+C_COMMAND_JUMP_PATTERN+'?')
# L命令にマッチ
l_command_pattern = re.compile(L_COMMAND_PATTERN)
# コメントのみの行にマッチ
comment_pattern = re.compile(COMMENT_PATTERN)

# C 命令は、
# comp:省略不可
# dest:省略可能
# jump:省略可能
# なので4パターンある。パターンによって処理を変えたいので、それぞれにマッチする正規表現を用意する。
# comp領域のみからなるC命令にマッチ(e.g. "D")
c_command_comp_pattern = re.compile('^'+C_COMMAND_COMP_PATTERN+'$')
# comp領域とdest領域からなるC命令にマッチ(e.g. "MD=M+D")
c_command_comp_dest_pattern = re.compile(
    '^'+C_COMMAND_DEST_PATTERN + C_COMMAND_COMP_PATTERN+'$')
# comp領域とjump領域からなるC命令にマッチ(e.g. "D;JGT")
c_command_comp_jump_pattern = re.compile(
    '^'+C_COMMAND_COMP_PATTERN + C_COMMAND_JUMP_PATTERN+'$')
# comp領域とdest領域とjump領域からなるC命令にマッチ(e.g. "D=D+1;JMP")
c_command_comp_dest_jump_pattern = re.compile(
    '^'+C_COMMAND_DEST_PATTERN+C_COMMAND_COMP_PATTERN+C_COMMAND_JUMP_PATTERN+'$')


class HackParser:
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
            comment_pattern, '', self.current_line).strip()

    def command_type(self):
        if comment_pattern.match(self.current_command):
            return COMMENT
        if a_command_pattern.match(self.current_command):
            return A_COMMAND
        if c_command_pattern.match(self.current_command):
            return C_COMMAND
        if l_command_pattern.match(self.current_command):
            return L_COMMAND

        return NOT_A_HACK_ASSEMBLY_COMMAND

    def symbol(self):
        a_command = a_command_pattern.match(self.current_command)
        l_command = l_command_pattern.match(self.current_command)

        if a_command:
            return a_command.group().lstrip('@')
        if l_command:
            return l_command.group().lstrip('(').rstrip(')')

        return ''

    def dest(self):
        # dest領域にマッチ(e.g. "D=")
        dest_pattern = re.compile(C_COMMAND_DEST_PATTERN)
        if c_command_comp_dest_pattern.match(self.current_command) or c_command_comp_dest_jump_pattern.match(self.current_command):
            return dest_pattern.match(self.current_command).group().rstrip('=')

        return 'null'

    def comp(self):
        equal_index = self.current_command.find('=')
        semicolon_index = self.current_command.find(';')

        if c_command_comp_pattern.match(self.current_command):
            return self.current_command

        if c_command_comp_dest_pattern.match(self.current_command):
            return self.current_command[equal_index+1:]

        if c_command_comp_jump_pattern.match(self.current_command):
            return self.current_command[:semicolon_index]

        if c_command_comp_dest_jump_pattern.match(self.current_command):
            return self.current_command[equal_index+1:semicolon_index]

        return ''

    def jump(self):
        semicolon_index = self.current_command.find(';')

        if semicolon_index > 0:
            return self.current_command[semicolon_index+1:]

        return 'null'
