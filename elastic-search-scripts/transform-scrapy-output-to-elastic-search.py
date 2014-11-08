import sys

for line in open(sys.argv[1]):
    start = 0
    end = -2
    if line[start] == '[':
        start += 1
    if line[end] != ',':
        end += 1
    print '{"index":{}}'
    print line[start:end]
