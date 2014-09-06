#!/bin/bash
./trace_generator_globally.py -s 'globally' -p 'always a' -i p1 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'never d' -i p2 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'eventually at least 2 a' -i p3 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'eventually at most 3 c' -i p4 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'd responding at most 1000 tu c' -i p5 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'b responding exactly 1000 tu a' -i p6 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'a preceding at most 6000 tu b' -i p7 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'c preceding at least 100 tu d' -i p8 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'a preceding exactly 100 tu b' -i p9 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'a, b preceding at least 1000 tu c, d' -i p10 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'd responding at least 1000 tu a, b' -i p11 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'b responding a' -i p12 -l 1000000