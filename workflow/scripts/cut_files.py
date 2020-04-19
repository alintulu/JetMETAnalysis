import os
import argparse

parser = argparse.ArgumentParser(description='Change the option prefix characters', prefix_chars='+/')
parser.add_argument("+i", "++input", type=str, nargs='?')
parser.add_argument("+o", "++output", type=str, nargs='?')
parser.add_argument("+n", "++nfiles", type=int, nargs='?')
args = parser.parse_args()

f = None
g = None
try:
    f = open(args.input, 'r')
    g = open(args.output, 'w+')
    for i, line in enumerate(f):
        if args.nfiles > 0 and i >= args.nfiles:
            print 'hep'
            break
        g.write(line)
finally:
    if f is not None:
        f.close()
    if g is not None:
        g.close()