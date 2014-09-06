Welcome to OCLr-check
==========

OCLr-check is a toolset to do offline check for OCLR properties on synthesized traces, which is developed by Wei Dou (http://people.svv.lu/dou) at the SVV lab (http://www.svv.lu) of the University of Luxembourg (http://wwwen.uni.lu).

*OCLR* is a temporal extension of OCL (Object Constraint Language, http://www.omg.org/spec/OCL) which allows users to express temporal properties using the state-of-the-art property specification patterns. (see http://link.springer.com/chapter/10.1007%2F978-3-319-09195-2_4).
Precondition
---
MacOS/Linux/Unix,
Xtext framework (http://xtext.org) 2.5.0+,
Java 1.6.0_65+,
Eclipse OCL 4.1.0

Usage
---

###Checker
The offline trace checker is comprised of three parts: the models (Trace model and OCLR meta model), the mapping from *OCLR* to OCL, and the check programs. To run the check program, you have to build a Java project in Xtext, and generate java codes with the models. Once you need to add the *OCLR* translation and the check programs into the project, you may need to change the package names in these codes to adapt the new environment.

The folder "./checker/DSLs/" contains those Xtext  codes for creating Ecore models of *trace* and *OCLR* and also 38 *OCLR* specifications with the DSL are attached.

###Test Cases
The test cases contain two sets of data: *OCLR* properties (instances of *OCLR* meta model) and traces (instances of the *Trace* model).

###Trace Generators
These are the programs which generate the traces in test cases. But each run of the programs can have different correct traces, so if you are interested for new test cases, please download them and generate your own traces.
You can either use the shell program in each subfolder or invoke the Python program one by one, like:

```
./trace_generator_globally.py --help
./trace_generator_globally.py -s 'globally' -p 'always a' -i p1 -l 1000000
```
The first line will tell you how to use this program.
