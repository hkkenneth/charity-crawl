import sys
import codecs

outfile = codecs.open(sys.argv[2], 'w', 'utf-8')
for line in codecs.open(sys.argv[1], 'r', 'utf-8'):
    outfile.write('{"index":{}}\n')
    outfile.write(line)

outfile.close()

