import re
import sys
import os
# from matplotlib import pyplot as plt

ftracepath = '/home/kataworker/ftraceresult/'
trinitypath = '/home/kataworker/trinityresult/'

def parsing(file, file2):
    ft = ftracepath + file
    tr = trinitypath + file2
    f = open(file, 'r')
    f2 = open(file2, 'r')
    dict = {}
    p = 0
    m = [0,0,0]
    n = [0,0,0]
    mode = 0
    a = 0
    result = []
    dellist = []

    while(True):
        list = []
        list2 = []
        r = f.readline()

        if m[2] == 6:
            m[0] = 0
            m[1] = 0
            m[2] = 0
            r2 = f2.readline()
            result.append(r2.replace('\n',''))
            p = 1

        if n[2] == 6:
            n[0] = 0
            n[1] = 0
            n[2] = 0
            p = 0
            for key,value in dict.items():
                dict[key] -= 1
                if key == 'sys_write':
                    dict[key] -= 6
                elif key == 'sys_futex':
                    dict[key] -= 6
                elif key == 'sys_fdatasync':
                    dict[key] -= 6
                if dict[key] < 0:
                    dellist.append(key)
            for i in dellist:
                dict.pop(i,None)
            dellist = []
            result = result[:-18]
            result.append(dict)
            dict = {}
            result.append(' ')
            
        if r == '':break

        list = r.split()
        list = ' '.join(list[4:])

        for i in re.split('[:,() ]', list):
            if not i:
                continue
            list2.append(i)
        
        char = list2[0]

        for i,letter in enumerate(list2):
            if letter == "tracing_mark_write":
                if list2[i+8] == "start":
                    p = 2
                elif list2[i+8] == "end" and p == 1:
                    p = 0
                    result.append(' ')

        if mode == 1:
            if char == 'sys_futex':
                if m[2] == 2:
                    pass
                elif m[2] > 2:
                    m[2] -= 1

            elif char != 'sys_fsync':
                m[0] = 0
                m[1] = 0
                m[2] = 0
                mode = 0
        if char == 'sys_fsync' and p == 0:
            m[0] += 1
        elif m[0] > 1 and char == 'sys_write':
            m[1] += 1
        elif m[0] > 1 and m[1] > 1 and char == 'sys_futex':
            m[2] += 1
            if m[2] == 2:
                mode = 1
        else: 
            m[0] = 0
            m[1] = 0
            m[2] = 0

        if mode == 1:
            if char == 'sys_futex':
                if n[2] == 2:
                    pass
                elif n[2] > 2:
                    n[2] -= 1
            elif char != 'sys_fdatasync':
                n[0] = 0
                n[1] = 0
                n[2] = 0
                mode = 0
        if char == 'sys_fdatasync' and p == 1:
            n[0] += 1
        elif n[0] > 1 and char == 'sys_write':
            n[1] += 1
        elif n[0] > 1 and n[1] > 1 and char == 'sys_futex':
            n[2] += 1
            if n[2] == 2:
                mode = 1
        else:
            n[0] = 0
            n[1] = 0
            n[2] = 0

        if p == 1:
            result.append(list)
            if char in dict:
                dict[char] += 1
            else:
                dict[char] = 1
            m[0] = 0
            m[1] = 0
            m[2] = 0
        elif p == 2:
            r2 = f2.readline()
            result.append(r2)
            p = 1

    f.close()

    for i in result:
        print(i)

    PATH = '/home/kataworker/result/' + file
    f = open(PATH, 'w')

    for i in result:
        try:
            f.write(i + "\n")
        except:
            continue
    f.close()

ftracelist = os.listdir(ftracepath)
trinitylist = os.listdir(trinitypath)

for f, t in zip(ftracelist,trinitylist):
    parsing(f,t)
