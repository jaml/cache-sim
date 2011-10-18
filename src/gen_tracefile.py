#!/usr/bin/env python

import sys

def generate_header(block_count, word_length, cache_type):
    return "%s\n%s\n%s\n" % (block_count, word_length, cache_type)

def generate_unfused(block_count, word_length, cache_type, loop):
    output = open("unfused.trace", "w")
    header = generate_header(block_count, word_length, cache_type)

    output.write(header)
    
    a = 0
    b = (loop**2)
    c = (loop**2) * 2
    d = (loop**2) * 3

    for i in range(loop):
        output.write("l " + str(b+i) + "\n")
        output.write("l " + str(c+i) + "\n")
        output.write("s " + str(a+i) + "\n")

    for i in range(loop):
        output.write("l " + str(a+i) + "\n")
        output.write("l " + str(c+i) + "\n")
        output.write("s " + str(d+i) + "\n")

    output.write("h\n")
    output.close()

def generate_fused(block_count, word_length, cache_type, loop):
    output = open("fused.trace", "w")
    header = generate_header(block_count, word_length, cache_type)

    output.write(header)
    
    a = 0
    b = (loop**2)
    c = (loop**2) * 2
    d = (loop**2) * 3

    for i in range(loop):
        output.write("l " + str(b+i) + "\n")
        output.write("l " + str(c+i) + "\n")
        output.write("s " + str(a+i) + "\n")
        output.write("l " + str(a+i) + "\n")
        output.write("l " + str(c+i) + "\n")
        output.write("s " + str(d+i) + "\n")

    output.write("h\n")
    output.close()

def generate_files(block_count, word_length, cache_type, loop):
    generate_unfused(block_count, word_length, cache_type, loop)
    generate_fused(block_count, word_length, cache_type, loop)

if __name__ == '__main__':
    if len(sys.argv) != 5:
        print "Usage: gen_tracefile.py BLOCK-COUNT WORD-SIZE CACHE LOOP-SIZE"
        sys.exit(1)
    
    block_count = int(sys.argv[1])
    word_length = int(sys.argv[2])
    cache_type = sys.argv[3]
    loop = int(sys.argv[4])
    
    generate_files(block_count, word_length, cache_type, loop)
