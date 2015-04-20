#!/bin/bash
./trace_generator_globally.py -s 'globally' -p 'always A' -i p1 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'never B' -i p2 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'eventually at least 2 A' -i p3 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'eventually at most 3 A' -i p4 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'A responding at most 1000 tu B' -i p5 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'A responding exactly 1000 tu B' -i p6 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'A preceding at most 6000 tu B' -i p7 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'A preceding at least 100 tu B' -i p8 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'A preceding exactly 100 tu B' -i p9 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'A, B preceding at least 1000 tu C, D' -i p10 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'A responding at least 1000 tu B, C' -i p11 -l 1000000
./trace_generator_globally.py -s 'globally' -p 'A responding B' -i p12 -l 1000000