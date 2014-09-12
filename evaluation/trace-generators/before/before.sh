#!/bin/bash
./trace_generator_before.py -s 'before b' -p 'eventually a' -i p13 -l 100000
./trace_generator_before.py -s 'before 3 b' -p 'eventually exactly 2 a' -i p14 -l 100000
./trace_generator_before.py -s 'before 2 b' -p 'never d' -i p15 -l 100000
./trace_generator_before.py -s 'before d' -p 'c responding at most 3000 tu a' -i p16 -l 100000
./trace_generator_before.py -s 'before c at least 1000 tu' -p 'a responding at least 1000 tu b' -i p17 -l 100000
./trace_generator_before.py -s 'before d' -p 'a, # at most 6000 tu b preceding c' -i p18 -l 100000
./trace_generator_before.py -s 'before 3 b' -p 'a, # at least 1000 tu c preceding d' -i p19 -l 100000
./trace_generator_before.py -s 'before d' -p 'a preceding b' -i p20 -l 100000
