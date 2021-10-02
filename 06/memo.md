# 作業記録

2021/09/25 開始
2021/10/2 終了

実作業時間は 7~10h ぐらいか

#　メモ
C 命令は、
comp:省略不可
dest:省略可能
jump:省略可能
なので以下の 4 パターンがある

・(comp)
=> e.g. D

・(dest)=(comp)
=> e.g. M=M+D

・(comp)(jump)
=> e.g. D;JGT

・(dest)=(comp)(jump)
=> e.g. D=A;JLE
