import re
import sys

def parsing(file):
    list = []
    f = open(file, 'r')
    r = f.read()

    for i in re.split('[:,() ]', r):
        if not i:
            continue
        list.append(i)

    return list

def splitresult(list):
    p = 0
    l = []
    result = []

    for i, letter in enumerate(list):
        #Start check
        if letter == "tracing_mark_write":
            if list[i+5] == "start":
                p = 1
        elif letter == "sys_fsync":
            if (list[i+67] == "sys_fsync" and list[i+126] == "sys_fsync"):
                p = 1
        
        #End check
        if letter == "tracing_mark_write":
            if list[i+5] == "end" and p == 1:
                result.append(' '.join(l))
                l = []
                p = 0
            elif list[i+5] == "end" and p == 0:
                print("error: start tracing marker disappear")
                sys.exit()
        elif letter == "sys_fdatasync":
            print(f'{p} {i} {letter} {list[i+67]} {list[i+126]}')
            if (list[i+67] == "sys_fdatasync" and list[i+126] == "sys_fdatasync" and p == 1):
                result.append(' '.join(l))
                l = []
                p = 0
            # elif (list[i+67] == "sys_fdatasync" and list[i+126] == "sys_fdatasync" and p == 0):
            #     print("error: fsync disappear")
            #     sys.exit()
        
        if p == 1:
            l.append(letter)

    return result

#trinitylist = parsing('')
ftracelist = parsing('/home/kataworker/test2.txt')
ftracelist = splitresult(ftracelist)

for i in ftracelist:
    print(i)
#ftracelist = splitresult(ftracelist)
