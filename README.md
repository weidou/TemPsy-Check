Welcome to OCLR-Check
==========

OCLR-Check is a toolset to perform offline checking of *OCLR* properties on system execution traces. The tools have been developed by Wei Dou (http://people.svv.lu/dou) and maintained by Wei and Domenico Bianculli (http://people.svv.lu/bianculli) at the SVV lab (http://www.svv.lu) of the University of Luxembourg (http://wwwen.uni.lu). More introduction  can be found in this technical report: "Wei Dou, Domenico Bianculli, and Lionel Briand. __A model-based approach to trace checking of temporal properties with OCL__. Technical Report TR-SnT-2014-5, SnT Centre - University of Luxembourg, September 2014. [Online]. Available: http://hdl.handle.net/10993/16112"

*OCLR* is a temporal extension of OCL (Object Constraint Language, http://www.omg.org/spec/OCL) which allows users to express temporal properties using property specification patterns (http://patterns.projects.cis.ksu.edu). The syntax and semantics of *OCLR* have been introduced in this paper: "Wei Dou, Domenico Bianculli, and Lionel Briand. __OCLR: a more expressive, pattern-based temporal extension of OCL__. In Proceedings of the 2014 European Conference on Modelling Foundations and Applications (ECMFA 2014), York, United Kingdom, volume 8569 of Lecture Notes in Computer Science, pages 51-66. Springer, July 2014."

Requirements
---
* Mac OS X/Linux
* Xtext framework (http://xtext.org) 2.5.0+
* Java 1.6.0_65
* Eclipse OCL 4.1.0

Content of the bundle
---
The OCLR-Check distribution contains two modules:

###Checker
The offline trace checker is comprised of three parts: the models (Trace model and OCLR meta model), the mapping from *OCLR* to OCL, and the check programs. To run the check program, you have to build a Java project in Xtext, and generate java codes with the models. Once you need to add the *OCLR* translation and the check programs into the project, you may need to change the package names in these codes to adapt the new environment.

The folder "./checker/DSLs/" contains those Xtext  codes for creating Ecore models of *trace* and *OCLR*.

###Evaluation
This module contains *OCLR* properties, traces and trace generators that generate those traces.

* #####Properties
We provide 38 *OCLR* properties with both their DSL specifications and XMI instances with respect to the *OCLR* meta model. In fact, those XMI instances are generated from the DSL specifications by using the program: "/checker/DSLs/OCLRInstanceFactory.java".

* #####Traces
To check different properties, different traces are generated. They are grouped by property scopes - *globally* (p1-p12), *before* (p13-p20), *after* (p21-p31), *between-and* (p32-38).

* #####Trace Generators
For different scopes, the trace generators are implemented with different generation strategies. We will not explain again the details about the strategies (they can be found in the evaluation section of the technical report), but we will briefly introduce how to use the scripts (\*.py and \*.sh)..
  * Each Python program (\*.py) is actually a trace generator which can be distinguished by its name, e.g., *trace_generator_globally.py* is the trace generator to generate the trace for the properties with the *globally* scope. A trace generator needs 4 parameters: 1). scope. 2). pattern. 3). property id. 4). (maximum) trace length. For instance:
  ```./trace_generator_globally.py -s 'globally' -p  'always a' -i p1 -l 1000000```
  * A Shell script (\*.sh) is used to generate traces automatically for each strategy by invoking the same Python program with different parameters.
