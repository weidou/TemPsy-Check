Welcome to OCLR-Check
==========

OCLR-Check is a toolset to perform offline checking of *OCLR* properties on system execution traces. The toolset has been developed by Wei Dou (http://people.svv.lu/dou), at the SVV lab (http://www.svv.lu) of the University of Luxembourg (http://wwwen.uni.lu). 
More information on OCLR-Check is available in this technical report:

Wei Dou, Domenico Bianculli, and Lionel Briand. __A model-based approach to trace checking of temporal properties with OCL__. Technical Report TR-SnT-2014-5, SnT Centre - University of Luxembourg, September 2014.  Available online at http://hdl.handle.net/10993/16112

*OCLR* is a temporal extension of OCL (Object Constraint Language, http://www.omg.org/spec/OCL) which allows users to express temporal properties using property specification patterns (http://patterns.projects.cis.ksu.edu). *OCLR* has been introduced in this paper: 

Wei Dou, Domenico Bianculli, and Lionel Briand. __OCLR: a more expressive, pattern-based temporal extension of OCL__. In Proceedings of the 2014 European Conference on Modelling Foundations and Applications (ECMFA 2014), York, United Kingdom, volume 8569 of Lecture Notes in Computer Science, pages 51-66. Springer, July 2014. Available online  at http://dx.doi.org/10.1007/978-3-319-09195-2_4

Requirements
---
* Mac OS X / Linux
* Xtext framework (http://xtext.org) 2.5.0+
* Java 1.6.0_65
* Eclipse OCL 4.1.0

Content of the distribution
---
The OCLR-Check distribution contains two modules:

###Checker (*checker* folder)
The offline trace checker is comprised of four parts: the OCLR-Check main programs, the models, the DSLs, and the mapping from *OCLR* to OCL.
  * In the *main* folder, *OfflineCheck.java* is the main program for checking *OCLR* properties. The other Java program *ConstraintFactory.java* is an auxiliary class for building OCL constraints and/or queries.
  * The *models* folder contains three Ecore models: a *trace* model, an *OCLR* meta model, and a *check* model. By using the three models, we generate the corresponding Java code and check the traces with our *checker* programs.
  * the *DSLs* folder contains  the Xtext definitions (*Trace.xtext* and *Oclr.xtext*) of the trace model and of the *OCLR* meta model. It also contains the programs for building XMI instances of the two models.
  * The *oclr2ocl* folder contains the definition of the  translation  that maps *OCLR* constraints into OCL constraints on the trace model.
  
###Evaluation
This module contains the artifacts used to perform the evaluation described in the aforementioned technical report:
*OCLR* properties, traces, and the trace generators used to generate the traces.

* #####Properties
We provide 38 *OCLR* properties, both as DSL specifications and as XMI instances conforming to the *OCLR* meta model. These XMI instances are generated from the DSL specifications by using the program: "/checker/DSLs/OCLRInstanceFactory.java".

* #####Traces
For each property to check, we provide several traces. These traces are grouped by property scopes - *globally* (p1-p12), *before* (p13-p20), *after* (p21-p31), *between-and* (p32-38).

* #####Trace Generators
Traces generator programs implement various generation strategies, depending on the type of property that one wants to check on the trace being generated. 
Generators are Python programs named after the type of property for which they generate traces;  e.g., *trace_generator_globally.py* is the trace generator to generate the trace for the properties with the *globally* scope. 
A trace generator needs 4 parameters: 1). scope. 2). pattern. 3). property id. 4). (maximum) trace length. For instance:
  ```./trace_generator_globally.py -s 'globally' -p  'always a' -i p1 -l 1000000```
  corresponds to generating traces for the property ```globally always a``` with various trace lengths: 100K, 200K, ..., 1M.
We also provide the shell scripts used to generate the traces for the 38 properties contained in the distribution. 

#Usage
To run the OCLR-Check main program, you have to build a Java project in Xtext, and generate Java code with the models. Once the project is ready, you need to add the *OCLR* translation and the main programs into the project, you may need to change the package names in these codes to adapt the new environment.

