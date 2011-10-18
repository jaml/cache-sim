#!/usr/bin/env python

import sys

from tracefile import load_tracefile

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: trace.py TRACEFILE"
        sys.exit(1)
    
    filename = sys.argv[1]
    tracefile = load_tracefile(filename)
    tracefile.run()
