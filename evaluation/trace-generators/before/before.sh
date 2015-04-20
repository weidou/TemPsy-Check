#!/bin/bash
./trace_generator_before.py -s 'before A' -p 'eventually B' -i p13 -l 100000
./trace_generator_before.py -s 'before 3 A' -p 'eventually exactly 2 B' -i p14 -l 100000
./trace_generator_before.py -s 'before 2 A' -p 'never B' -i p15 -l 100000
./trace_generator_before.py -s 'before A' -p 'B responding at most 3000 tu C' -i p16 -l 100000
./trace_generator_before.py -s 'before A at least 1000 tu' -p 'B responding at least 1000 tu C' -i p17 -l 100000
./trace_generator_before.py -s 'before A' -p 'B, # at most 6000 tu C preceding D' -i p18 -l 100000
./trace_generator_before.py -s 'before 3 A' -p 'B, # at least 1000 tu C preceding D' -i p19 -l 100000
./trace_generator_before.py -s 'before A' -p 'B preceding C' -i p20 -l 100000
