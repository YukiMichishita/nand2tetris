print(f'    Or(a=in[{0}], b=in[{1}], out=or1);')

for i in range(1, 6):
    print(f'    Or(a=or{i}, b=in[{i+1}], out=or{i+1});')

print(f'    Or(a=or{6}, b=in[{7}], out=out);')
