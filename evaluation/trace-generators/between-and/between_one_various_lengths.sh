#!/bin/bash
./trace_generator_between_one_various_lengths.py -s 'between 3 A and B' -p 'always C' -i p36 -l 100000
./trace_generator_between_one_various_lengths.py -s 'between A at least 1000 tu and 2 B' -p 'C preceding at least 1000 tu D' -i p37 -l 100000
./trace_generator_between_one_various_lengths.py -s 'between 2 A and 2 B' -p 'eventually at most 10 C' -i p38 -l 100000
