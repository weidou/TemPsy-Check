There are two runnable scripts: *prepare.py* and *run.py*.

If this is your first time to run the two scripts,
please use parameter '-h' after the script's name for help.

Before running the scripts, please upload your properties and traces
respectively into the directories *properties* and *traces*.

The former one should be run before the later, since it helps preparing
necessary artifacts (i.e., XMI instances properties and traces).

The script *prepare.py* is responsible for transforming
properties (in OCLR formact) and traces (in CSV format) into XMI format.
The script needs two parameters - the directory that contains OCLR properties
and the directory that contains CSV traces. For more details, please use
parameter '-h' to check out the usage.
After running script prepare.py, a folder named *artifacts* will be created
and it will contain all the XMI files of properties and traces.

The script *run.py* then checks a OCLR property over a trace.
So you need to provide a property file name (with or without file extension,
e.g., 'test.oclr' or 'test') and a trace file name (with or without file extension). For more details, please use parameter '-h' to check out the usage.
