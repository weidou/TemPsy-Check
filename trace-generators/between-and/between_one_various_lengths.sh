#!/bin/bash
./trace_generator_between_one_various_lengths.py -s 'between 3 a and b' -p 'always c' -i p36 -l 100000
./trace_generator_between_one_various_lengths.py -s 'between a at least 1000 tu and 2 b' -p 'c preceding at least 1000 tu d' -i p37 -l 100000
./trace_generator_between_one_various_lengths.py -s 'between 2 a and 2 b' -p 'eventually at most 10 c' -i p38 -l 100000
