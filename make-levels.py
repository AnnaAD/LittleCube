#! /usr/bin/env python

fd = open('levels.txt')

all = {}

print '    if (level == -2) {'
print '    }', 


for line in fd:
    # print line,

    tmp = line.split();

    if len(tmp) > 0 and tmp[0] == 'LEVEL':
        t = ''
        for j in range(2,len(tmp)-1):
            t += tmp[j] + ' '
        t += tmp[len(tmp)-1]
        text  = t
        num   = int(tmp[1])
        boxes = []
    elif len(tmp) > 0 and tmp[0] == 'PRINT':
        print '    else if (level == %d) {' % num
        print '        levelTxt = \"%s\";' % text
        for b in boxes:
            print '        %s' % b
        print '     } ',
    elif len(tmp) > 0:
        boxes.append(line.strip())
    

fd.close()

