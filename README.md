Welcome to TemPsy-Check
==========

TemPsy-Check is a toolset to perform offline checking of *TemPsy* properties on system execution traces. The toolset has been developed by [Wei Dou](http://people.svv.lu/dou), at the [SVV lab](http://www.svv.lu) of the [University of Luxembourg](http://wwwen.uni.lu).
More information on TemPsy-Check is available in this technical report:

> Wei Dou, Domenico Bianculli, and Lionel Briand. __A model-based approach to offline trace checking of temporal properties with OCL__. Technical Report TR-SnT-2014-5, SnT Centre - University of Luxembourg, March 2014.  Available online at http://hdl.handle.net/10993/16112

*TemPsy* (**Tem**poral **P**roperty Made Ea**sy**) is a domain specific language based on [OCL](http://www.omg.org/spec/OCL) (Object Constraint Language) which allows users to express temporal properties using [property specification patterns](http://patterns.projects.cis.ksu.edu). *TemPsy* is a revised language of *OCLR*, which has been introduced in this paper:

> Wei Dou, Domenico Bianculli, and Lionel Briand. __OCLR: a more expressive, pattern-based temporal extension of OCL__. In Proceedings of the 2014 European Conference on Modelling Foundations and Applications (ECMFA 2014), York, United Kingdom, volume 8569 of Lecture Notes in Computer Science, pages 51-66. Springer, July 2014. Available online  at http://dx.doi.org/10.1007/978-3-319-09195-2_4


Requirements
---
* Mac OS X / Linux
* [Eclipse DSL Tools v. 4.6.0M3](http://www.eclipse.org/downloads/packages/eclipse-ide-java-and-dsl-developers/neonm3)+,
* Java 1.7+
* [Eclipse OCL 6.0.1](http://www.eclipse.org/modeling/mdt/downloads/?showAll=1&hlbuild=R201509081048&project=ocl#R201509081048)+
* [MonPoly 1.1.6](https://sourceforge.net/projects/monpoly/) (for comparison)
* Python 2.7 (for trace generation)

Content of the distribution
---
The TemPsy-Check distribution contains two modules:

###Checker (*checker* folder)
The offline trace checker is comprised of four parts: the TemPsy-Check main programs, the models, the DSL, and the mapping from *TemPsy* to OCL.
  * In the *main* folder, *Main.java* is the main program for doing the trace checking experiments presented in the evaluation section of the aforementioned technical report. The other Java programs provide auxiliary classes for executing the trace check (*TraceCheck.java*), building OCL constraints and/or queries (*ConstraintFactory.java*), and reading input files (the others).
  * The *models* folder contains three Ecore models: a *trace* model, an *TemPsy* meta model, and a *check* model. By using the three models, we generate the corresponding Java code and check the traces with our *checker* programs.
  * the *DSL* folder contains the Xtext definitions of the *TemPsy* meta model.
  * The *lib* folder contains the definition of the translation that maps *TemPsy* constraints into OCL constraints on the trace model.

###Evaluation
This module contains the artifacts used to perform the evaluation described in the aforementioned technical report:
the *TemPsy* properties and the trace generators used to generate the traces as well as the data for comparison.

* #####Properties
We provide 38 *TemPsy* properties, both as DSL specifications (under the *TemPsy-DSL-specifications* folder) and as XMI instances (under the *TemPsy-XMI-instances* folder) conforming to the *TemPsy* meta model. These XMI instances are generated from the DSL specifications using the jar file - [tempsy.jar](https://github.com/weidou/TemPsy-Check/releases/tag/v1.4-jars) - by feeding the two file names into tempsy.jar, e.g., ```java -jar tempsy.jar TemPsy-DSL-specifications/p1.tp TemPsy-XMI-instances/p1.xmi```. Notice that there is one more file under each folder, named *pm.tp* and *pm.xmi*, which contain ten properties derived from (ten) properties P3--P12. The file *pm.xmi* is used for the **batch check** performed by *TemPsy-Check*.

* #####Trace Generators
Traces generator programs implement various generation strategies, depending on the type of property that one wants to check on the trace being generated.
Generators are Python programs named after the type of property for which they generate traces;  e.g., *trace_generator_globally.py* is the trace generator to generate the trace for the properties with the ```globally``` scope.
A trace generator needs 4 parameters:
  1. scope (```--scope/-s SCOPE```);
  2. pattern (```--pattern/-p PATTERN```);
  3. property id (```--id/-i ID```);
  4. (maximum) trace length (```--length/-l LENGTH```).
  For instance:
  ```./trace_generator_globally.py -s 'globally' -p  'always a' -i p1 -l 1000000```
  corresponds to generating traces with various trace lengths - 100K, 200K, ..., 1M (determined by the given maximum trace length) for the property with id ```p1``` which has the scope ```globally``` and the pattern ```always a```.
We also provide the shell scripts used to generate the traces for the 38 properties contained in the releases. Notice that the 10 traces for the **batch check** are not directly generated by the scripts but derived from the 100 traces generated for P3--P12.

* #####Comparison
TemPsy-Check is compared with the state-of-the-art trace checking tool MonPoly (v. 1.1.6).
The results proves that TemPsy-Check is competitive in terms of scalability.
More detail about the data for evaluating MonPoly can be found in the [README](evaluation/comparison/MonPoly/README-MonPoly.txt) file under the *comparison* folder.

* #####Traces
For each property to check by TemPsy-Check, we provide several (the number of traces depends on the requirement of each experiment) traces in CSV. The CSV traces were generated by the trace generators introduced above. To keep the size of the repository small, we provide the traces in a separate release (https://github.com/weidou/TemPsy-Check/releases/tag/v1.4-csv).
In addition, the traces used to perform the evaluation of MonPoly described in the report are available in the seperated release (https://github.com/weidou/TemPsy-Check/releases/tag/v1.4-monpoly-data)

#Usage
Please read the [usage guide on the Wiki](https://github.com/weidou/TemPsy-Check/wiki/Usage).
