#!/bin/bash
./trace_generator_after.py -s 'after a at most 5000 tu' -p 'eventually b' -i p21 -l 100000
./trace_generator_after.py -s 'after d' -p 'always c' -i p22 -l 100000
./trace_generator_after.py -s 'after 2 b exactly 5000 tu' -p 'eventually d' -i p23 -l 100000
./trace_generator_after.py -s 'after a' -p 'd responding at least 1000 tu c' -i p24 -l 100000
./trace_generator_after.py -s 'after a' -p 'b preceding at most 3000 tu c, d' -i p25 -l 100000
./trace_generator_after.py -s 'after b at most 1000 tu' -p 'eventually d' -i p26 -l 100000
./trace_generator_after.py -s 'after 2 b' -p 'never c' -i p27 -l 100000
./trace_generator_after.py -s 'after c at most 3000 tu' -p 'eventually d' -i p28 -l 100000
#./trace_generator_after.py -s 'after b' -p 'd responding at most 6000 tu c' -i p28 -l 100000
./trace_generator_after.py -s 'after a' -p 'b preceding exactly 1000 tu c, # exactly 6000 tu d' -i p29 -l 100000
./trace_generator_after.py -s 'after b' -p 'eventually at most 6 d' -i p30 -l 100000
./trace_generator_after.py -s 'after 2 b at least 5000 tu' -p 'eventually d' -i p31 -l 100000
