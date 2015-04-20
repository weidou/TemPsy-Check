#!/bin/bash
./trace_generator_after.py -s 'after A at most 5000 tu' -p 'eventually B' -i p21 -l 100000
./trace_generator_after.py -s 'after A' -p 'always B' -i p22 -l 100000
./trace_generator_after.py -s 'after 2 A exactly 5000 tu' -p 'eventually B' -i p23 -l 100000
./trace_generator_after.py -s 'after A' -p 'B responding at least 1000 tu C' -i p24 -l 100000
./trace_generator_after.py -s 'after A' -p 'B preceding at most 3000 tu C, D' -i p25 -l 100000
./trace_generator_after.py -s 'after A at most 1000 tu' -p 'eventually B' -i p26 -l 100000
./trace_generator_after.py -s 'after 2 A' -p 'never B' -i p27 -l 100000
./trace_generator_after.py -s 'after A at most 3000 tu' -p 'eventually B' -i p28 -l 100000
./trace_generator_after.py -s 'after A' -p 'B preceding exactly 1000 tu C, # exactly 6000 tu D' -i p29 -l 100000
./trace_generator_after.py -s 'after A' -p 'eventually at most 6 B' -i p30 -l 100000
./trace_generator_after.py -s 'after 2 A at least 5000 tu' -p 'eventually B' -i p31 -l 100000
