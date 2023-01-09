#!/usr/bin/env python
# coding: utf-8

import sys
import subprocess
import os

tool = str(sys.argv[1])
limit = int(sys.argv[2])
extension = str(sys.argv[3])


assert type(tool) == str, "1st argument must be a string (tool name)"
assert type(limit) == int, "2nd argument must be an integer (amount of keywords in single file) "
assert type(extension) == str, "3rd argument must be a string (extension - .csv of .txt) "


cwd = os.getcwd()
input_path = os.path.join(cwd,'input') 
tool_path = os.path.join(cwd,tool)


if os.path.exists(tool_path) is False:
    os.mkdir(tool_path)
elif os.path.exists(tool_path):
    rem = subprocess.run(['rm','-rf',tool_path])
    if rem.returncode == 0 :
        os.mkdir(tool_path)
        print(f'removed previous files for {tool}')
    else:
        print(f'Unexpected error when removing files in {tool} directory {tool_path}')
        print(f'please remove the {tool} directory on your own, and re-run the script')



list_files = subprocess.run(['ls',input_path], capture_output=True)
files = list_files.stdout.decode().split()



for file in files:
    single_file = os.path.join(input_path, file)
    fl = single_file.split('/')
    fl = fl[-1].replace('.txt','')
    len_cmd = subprocess.run(['wc','-l',single_file], capture_output=True)
    lines = len_cmd.stdout.decode().split()
    lines = int(lines[0])
    iterations = -(-lines//limit)

    offset = 0

    for i in range(iterations):
        if i == 0:
            cmd = f"head -n {limit} '{single_file}'"
            ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = ps.communicate()[0].decode().split('\n')
            output.pop()
            out_file = os.path.join(tool_path,f'{fl}-file-{i+1}{extension}')
            with open(out_file, 'a') as f:
                for e in output:
                    f.write(f'{e}\n')

        elif i == iterations-1:
            cmd = f"tail -n {lines-offset} '{single_file}'"
            ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = ps.communicate()[0].decode().split('\n')
            output.pop()
            out_file = os.path.join(tool_path,f'{fl}-file-{i+1}{extension}')
            with open(out_file, 'a') as f:
                for e in output:
                    f.write(f'{e}\n')

        else:
            cmd = f"tail -n {lines-offset} '{single_file}' | head -n {limit}"
            ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            output = ps.communicate()[0].decode().split('\n')
            output.pop()
            out_file = os.path.join(tool_path,f'{fl}-file-{i+1}{extension}')
            with open(out_file, 'a') as f:
                for e in output:
                    f.write(f'{e}\n')

        offset += limit

