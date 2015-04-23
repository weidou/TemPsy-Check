#!/bin/bash
./trace_generator_between_multiple_fixed_number.py -s 'between A and B' -p 'always C' -i p32 -l 100000
./trace_generator_between_multiple_fixed_number.py -s 'between A at least 1000 tu and B at least 500 tu' -p 'never C' -i p33 -l 100000
./trace_generator_between_multiple_fixed_number.py -s 'between A and B' -p 'C responding at least 1000 tu D' -i p34 -l 100000
./trace_generator_between_multiple_fixed_number.py -s 'between A and B' -p 'never exactly 2 C' -i p35 -l 100000
