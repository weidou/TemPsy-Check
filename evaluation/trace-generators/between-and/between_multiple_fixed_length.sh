#!/bin/bash
./trace_generator_between_multiple_fixed_length_version2.py -s 'between a and b' -p 'always c' -i p32 -l 100000
./trace_generator_between_multiple_fixed_length_version2.py -s 'between a at least 1000 tu and b at least 1000 tu' -p 'never c' -i p33 -l 100000
./trace_generator_between_multiple_fixed_length_version2.py -s 'between a and b' -p 'd responding at least 1000 tu c' -i p34 -l 100000
./trace_generator_between_multiple_fixed_length_version2.py -s 'between c and d' -p 'never exactly 2 a' -i p35 -l 100000
