package lu.svv.offline.check;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Scanner;
import java.util.Set;

import lu.svv.offline.check.impl.CheckFactoryImpl;
import lu.svv.offline.oclr.BiScope;
import lu.svv.offline.oclr.EventChainElement;
import lu.svv.offline.oclr.OCLRConstraint;
import lu.svv.offline.oclr.OCLRExpression;
import lu.svv.offline.oclr.OccurrencePattern;
import lu.svv.offline.oclr.OclrPackage;
import lu.svv.offline.oclr.OrderPattern;
import lu.svv.offline.oclr.Pattern;
import lu.svv.offline.oclr.Scope;
import lu.svv.offline.oclr.UniScope;
import lu.svv.offline.trace.Event;
import lu.svv.offline.trace.TimeStamp;
import lu.svv.offline.trace.Trace;
import lu.svv.offline.trace.TraceElement;
import lu.svv.offline.trace.TraceFactory;
import lu.svv.offline.trace.TracePackage;
import lu.svv.offline.trace.impl.TraceFactoryImpl;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EClassifier;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.impl.EPackageRegistryImpl;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;
import org.eclipse.ocl.OCL;
import org.eclipse.ocl.OCLInput;
import org.eclipse.ocl.ParserException;
import org.eclipse.ocl.ecore.Constraint;
import org.eclipse.ocl.ecore.EcoreEnvironmentFactory;
import org.eclipse.ocl.expressions.OCLExpression;
import org.eclipse.ocl.helper.OCLHelper;

public class OfflineCheck {
	private Monitor monitor;
	public static final String oclOperationsFile = "../lu.svv.offline/lib/oclr.ocl";

	public static void main(String[] args) {
		//check_globally();
	}

	// This method is used for checking the OCLR properties p1-p12. Please change the lists if you only want to check subsets of the properties and traces
	public static void check_globally(){
		List<Integer> iList = Arrays.asList(100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000); // indexes of the traces: various trace lengths
		List<Integer> properties = Arrays.asList(1,2,3,4,5,6,7,8,9,10,11,12); // properties p1-p12
		Iterator<Integer> iterProperty = properties.iterator();
		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp = "../lu.svv.offline/instances/p%d_%d.xmi";
		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty.hasNext()){
			i=0;
			int propertyNo = iterProperty.next();
		    System.out.println("P"+propertyNo+":");
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					long startTime = System.currentTimeMillis();
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).check(); //check the property
					long stopTime = System.currentTimeMillis();
				    long elapsedTime = stopTime - startTime;
				    System.out.print(elapsedTime/1000.0);
				    System.out.print('\t');
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for checking the OCLR properties p13-p20. Please change the lists if you only want to check subsets of the properties and traces
	public static void check_before(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9,10); // indexes of the traces
		List<Integer> properties_before = Arrays.asList(13,14,15,16,17,18,19,20); // properties p13-p20
		Iterator<Integer> iterProperty_before = properties_before.iterator();
		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_before = "../lu.svv.offline/instances/p%d_100000_%d_before.xmi";
		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_before.hasNext()){
			i=0;
			int propertyNo = iterProperty_before.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					long startTime = System.currentTimeMillis();
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_before, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).check(); //check the property
					long stopTime = System.currentTimeMillis();
				    long elapsedTime = stopTime - startTime;
				    System.out.print(elapsedTime/1000.0);
				    System.out.print('\t');
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for checking the OCLR properties p21-p31. Please change the lists if you only want to check subsets of the properties and traces
	public static void check_after(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9); // indexes of the traces
		List<Integer> properties_after = Arrays.asList(21,22,23,24,25,26,27,28,29,30,31); // properties p21-p31
		Iterator<Integer> iterProperty_after = properties_after.iterator();
		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_after = "../lu.svv.offline/instances/p%d_100000_%d_after.xmi";
		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_after.hasNext()){
			i=0;
			int propertyNo = iterProperty_after.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_after, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).check(); //check the property
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for checking the OCLR properties p32-p35 on the 'between_mult_fixed_length' traces. Please change the lists if you only want to check subsets of the properties and traces
	public static void check_between_multiple_fixed_length(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9,10); // indexes of the traces
		List<Integer> properties_between = Arrays.asList(32,33,34,35); // properties p32-p35

		Iterator<Integer> iterProperty_between = properties_between.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_between = "../lu.svv.offline/instances/p%d_100000_%d_between_mult_fixed_length.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_between.hasNext()){
			i=0;
			int propertyNo = iterProperty_between.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_between, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).check(); //check the property
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for checking the OCLR properties p32-p35 on the 'between_mult_fixed_number' traces. Please change the lists if you only want to check subsets of the properties and traces
	public static void check_between_multiple_fixed_number(){
		List<Integer> iList = Arrays.asList(1,2,3,4); // indexes of the traces
		List<Integer> properties_between = Arrays.asList(32,33,34,35); // properties p32-p35

		Iterator<Integer> iterProperty_between = properties_between.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_between = "../lu.svv.offline/instances/p%d_100000_%d_between_mult_fixed_number.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_between.hasNext()){
			i=0;
			int propertyNo = iterProperty_between.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_between, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).check(); //check the property
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for checking the OCLR properties p36-p38 on the 'between_one_fixed_length' traces. Please change the lists if you only want to check subsets of the properties and traces
	public static void check_between_one_fixed_length(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9,10); // indexes of the traces
		List<Integer> properties_between = Arrays.asList(36,37,38); // properties p36-p38

		Iterator<Integer> iterProperty_between = properties_between.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_between = "../lu.svv.offline/instances/p%d_100000_%d_between_one_fixed_length.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_between.hasNext()){
			i=0;
			int propertyNo = iterProperty_between.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_between, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).check(); //check the property
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for checking the OCLR properties p36-p38 on the 'between_one_various_lengths' traces. Please change the lists if you only want to check subsets of the properties and traces
	public static void check_between_one_various_lengths(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9); // indexes of the traces
		List<Integer> properties_between = Arrays.asList(36,37,38); // properties p36-p38

		Iterator<Integer> iterProperty_between = properties_between.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_between = "../lu.svv.offline/instances/p%d_100000_%d_between_one_various_lengths.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_between.hasNext()){
			i=0;
			int propertyNo = iterProperty_between.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_between, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).check(); //check the property
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for applying the OCLR properties scopes of p13-p20. Please change the lists if you only want to check subsets of the properties and traces
	public static void apply_before(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9,10); // indexes of the traces
		List<Integer> properties_before = Arrays.asList(13,14,15,16,17,18,19,20); // properties p13-p20

		Iterator<Integer> iterProperty_before = properties_before.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_before = "../lu.svv.offline/instances/p%d_100000_%d_before.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();

		while(iterProperty_before.hasNext()){
			i=0;
			int propertyNo = iterProperty_before.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_before, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).evaluate_applyscope(); // apply the scope
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for applying the OCLR properties scopes of p21-p31. Please change the lists if you only want to check subsets of the properties and traces
	public static void apply_after(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9); // indexes of the traces
		List<Integer> properties_after = Arrays.asList(21,22,23,24,25,26,27,28,29,30,31); // properties p21-p31

		Iterator<Integer> iterProperty_after = properties_after.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_after = "../lu.svv.offline/instances/p%d_100000_%d_after.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();

		while(iterProperty_after.hasNext()){
			i=0;
			int propertyNo = iterProperty_after.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_after, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).evaluate_applyscope(); // apply the scope
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for applying the OCLR properties scopes of p32-p35 on the 'between_mult_fixed_length' traces. Please change the lists if you only want to check subsets of the properties and traces
	public static void apply_between_multiple_fixed_length(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9,10); // indexes of the traces
		List<Integer> properties_between = Arrays.asList(32,33,34,35); // properties p32-p35

		Iterator<Integer> iterProperty_between = properties_between.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_between = "../lu.svv.offline/instances/p%d_100000_%d_between_mult_fixed_length.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_between.hasNext()){
			i=0;
			int propertyNo = iterProperty_between.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_between, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).evaluate_applyscope(); // apply the scope
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for applying the OCLR properties scopes of p32-p35 on the 'between_mult_fixed_number' traces. Please change the lists if you only want to check subsets of the properties and traces
	public static void apply_between_multiple_fixed_number(){
		List<Integer> iList = Arrays.asList(1,2,3,4); // indexes of the traces
		List<Integer> properties_between = Arrays.asList(32,33,34,35); // properties p32-p35

		Iterator<Integer> iterProperty_between = properties_between.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_between = "../lu.svv.offline/instances/p%d_100000_%d_between_mult_fixed_number.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_between.hasNext()){
			i=0;
			int propertyNo = iterProperty_between.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_between, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).evaluate_applyscope(); // apply the scope
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for applying the OCLR properties scopes of p36-p38 on the 'between_one_fixed_length' traces. Please change the lists if you only want to check subsets of the properties and traces
	public static void apply_between_one_fixed_length(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9,10); // indexes of the traces
		List<Integer> properties_between = Arrays.asList(36,37,38); // properties p36-p38

		Iterator<Integer> iterProperty_between = properties_between.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_between = "../lu.svv.offline/instances/p%d_100000_%d_between_one_fixed_length.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_between.hasNext()){
			i=0;
			int propertyNo = iterProperty_between.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_between, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).evaluate_applyscope(); // apply the scope
				}
				i++;
			    System.out.println();
			}
		}
	}

	// This method is used for applying the OCLR properties scopes of p36-p38 on the 'between_one_various_lengths' traces. Please change the lists if you only want to check subsets of the properties and traces
	public static void apply_between_one_various_lengths(){
		List<Integer> iList = Arrays.asList(1,2,3,4,5,6,7,8,9); // indexes of the traces
		List<Integer> properties_between = Arrays.asList(36,37,38); // properties p36-p38

		Iterator<Integer> iterProperty_between = properties_between.iterator();

		String pPathTemp = "../lu.svv.offline/instances/p%d.xmi";
		String tPathTemp_between = "../lu.svv.offline/instances/p%d_100000_%d_between_one_various_lengths.xmi";

		int i = 0;
		OfflineCheck rc = new OfflineCheck();
		while(iterProperty_between.hasNext()){
			i=0;
			int propertyNo = iterProperty_between.next();
		    System.out.println("P"+propertyNo);
			while(i < 5){ // check each property 5 times
				Iterator<Integer> iter = iList.iterator();
				while(iter.hasNext()){
					String pPath = String.format(pPathTemp, propertyNo);
					String tPath = String.format(tPathTemp_between, propertyNo, iter.next());
					rc.loadMonitor(pPath, tPath).evaluate_applyscope(); // apply the scope
				}
				i++;
			    System.out.println();
			}
		}
	}

	// load XMI instances of OCLR properties and CSV trace instances
	public OfflineCheck loadMonitorFromCsv(String oclrFilePath, String traceFilePath)
	{
		ResourceSet resourceSet = new ResourceSetImpl();
		resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap().put(
					"xmi", new XMIResourceFactoryImpl());
		resourceSet.getPackageRegistry().put(OclrPackage.eNS_URI, OclrPackage.eINSTANCE);
		Resource oclrResource = resourceSet.getResource(URI.createURI(oclrFilePath), true);
		OCLRConstraint constraint = (OCLRConstraint) oclrResource.getContents().get(0);

		Monitor monitor = new CheckFactoryImpl().createMonitor();
		monitor.setConstraint(constraint);
		monitor.setTrace(loadTrace(traceFilePath));

		this.monitor = monitor;
		return this;
	}

	// load XMI instances of OCLR properties and trace instances
	public OfflineCheck loadMonitor(String oclrFilePath, String traceFilePath)
	{
		ResourceSet resourceSet = new ResourceSetImpl();
		resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap().put( "xmi", new XMIResourceFactoryImpl());
		resourceSet.getPackageRegistry().put(OclrPackage.eNS_URI, OclrPackage.eINSTANCE);
		Resource oclrResource = resourceSet.getResource(URI.createURI(oclrFilePath), true);
		OCLRConstraint constraint = (OCLRConstraint) oclrResource.getContents().get(0);

		resourceSet.getPackageRegistry().put(TracePackage.eNS_URI, TracePackage.eINSTANCE);
		Resource traceResource = resourceSet.getResource(URI.createURI(traceFilePath), true);
		Trace trace = (Trace) traceResource.getContents().get(0);

		Monitor monitor = new CheckFactoryImpl().createMonitor();
		//sanitize(trace, constraint);
		monitor.setConstraint(constraint);
		monitor.setTrace(trace);

		this.monitor = monitor;
		return this;
	}

	//load trace from a CSV file
	public static Trace loadTrace(String traceFilePath) {
		File traceFile = new File(traceFilePath);
		java.util.regex.Pattern csvDelimiter = java.util.regex.Pattern.compile("\\W+");
		TraceFactory traceFactory = TraceFactoryImpl.init();
		Trace trace = traceFactory.createTrace();
		Map<String, Event> events = new TreeMap<String, Event>();
		List<TraceElement> traceElements = new ArrayList<TraceElement>();
		int traceIndex = 0;
		int eventIndex = 0;
		try {
			Scanner traceInputStream = new Scanner(traceFile);
			traceInputStream.nextLine();
			while(traceInputStream.hasNext()){
				traceIndex++;
				String line = traceInputStream.nextLine();
				String[] values = csvDelimiter.split(line);
				String eventName = values[0];
				int timestampValue = Integer.parseInt(values[1]);
				TraceElement traceElement = traceFactory.createTraceElement();
				traceElement.setIndex(traceIndex);
				if (events.containsKey(eventName)) {
					traceElement.setEvent(events.get(eventName));
				} else {
					eventIndex++;
					Event newEvent = traceFactory.createEvent();
					newEvent.setId(eventIndex);
					newEvent.setName(eventName);
					traceElement.setEvent(newEvent);
					events.put(eventName, newEvent);
				}
				TimeStamp timestamp = traceFactory.createTimeStamp();
				timestamp.setValue(timestampValue);
				traceElement.setTimestamp(timestamp);
				traceElements.add(traceElement);
			}
			traceInputStream.close();
	     } catch(FileNotFoundException e){
	    	 	e.printStackTrace();
	     }
		trace.getTraceElements().addAll(traceElements);
		return trace;
	}

	public void check()
	{
		// Copied from org.eclipse.ocl.ecore.tests.DocumentationExamples.java
		EPackage.Registry registry = new EPackageRegistryImpl();
		registry.put(CheckPackage.eNS_URI, CheckPackage.eINSTANCE);
		registry.put(OclrPackage.eNS_URI, OclrPackage.eINSTANCE);
		registry.put(TracePackage.eNS_URI, TracePackage.eINSTANCE);
		EcoreEnvironmentFactory environmentFactory = new EcoreEnvironmentFactory(registry);
		OCL<EPackage, EClassifier, ?, ?, ?, ?, ?, ?, ?, Constraint, ?, ?> ocl = OCL.newInstance(environmentFactory);

		// get an OCL text file via some hypothetical API
		InputStream in = null;
		try {
			// parse the contents as an OCL document
			in = new FileInputStream(oclOperationsFile);
			in.skip(191);
			ocl.parse(new OCLInput(in));
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (ParserException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} finally {
		    try {
				in.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		OCLHelper<EClassifier, ?, ?, Constraint> helper = ocl.createOCLHelper();
		helper.setContext(CheckPackage.Literals.MONITOR);
		try {
			Map<String, String> constraintStringMap = ConstraintFactory.init().createConstraint(this.monitor);
			Map<String, Constraint> constraintMap = new HashMap<String, Constraint>();
			Iterator<Entry<String, String>> it1 = constraintStringMap.entrySet().iterator();
			while(it1.hasNext()) {
				Map.Entry<String, String> pairs = (Entry<String, String>)it1.next();
				constraintMap.put(pairs.getKey(), helper.createInvariant(pairs.getValue()));
			}
			Iterator<Entry<String, Constraint>> it2 = constraintMap.entrySet().iterator();
			while(it2.hasNext()) {
				Entry<String, Constraint> pairs = (Entry<String, Constraint>)it2.next();
				// check the property
				long startTime = System.currentTimeMillis();
				//ocl.check(this.monitor, pairs.getValue());
				System.out.println(ocl.check(this.monitor, pairs.getValue()));
				long stopTime = System.currentTimeMillis();
			    long elapsedTime = stopTime - startTime;
			    System.out.print(elapsedTime);
			    System.out.print('\t');
			}
		} catch (ParserException e) {
			e.printStackTrace();
		}
	}

	public void evaluate_applyscope()
	{
		// Copied from org.eclipse.ocl.ecore.tests.DocumentationExamples.java
		EPackage.Registry registry = new EPackageRegistryImpl();
		registry.put(CheckPackage.eNS_URI, CheckPackage.eINSTANCE);
		registry.put(OclrPackage.eNS_URI, OclrPackage.eINSTANCE);
		registry.put(TracePackage.eNS_URI, TracePackage.eINSTANCE);
		EcoreEnvironmentFactory environmentFactory = new EcoreEnvironmentFactory(registry);
		OCL<EPackage, EClassifier, ?, ?, ?, ?, ?, ?, ?, Constraint, ?, ?> ocl = OCL.newInstance(environmentFactory);

		InputStream in = null;
		try {
			in = new FileInputStream(oclOperationsFile);
			in.skip(191);
			ocl.parse(new OCLInput(in));
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (ParserException e) {
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally {
		    try {
				in.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		OCLHelper<EClassifier, ?, ?, Constraint> helper = ocl.createOCLHelper();
		helper.setContext(CheckPackage.Literals.MONITOR);
		try {
			Map<String, String> scopeQueryStringMap = ConstraintFactory.init().createScopeQuery(this.monitor);
			Map<String, OCLExpression<EClassifier>> queryMap = new HashMap<String, OCLExpression<EClassifier>>();
			Iterator<Entry<String, String>> it1 = scopeQueryStringMap.entrySet().iterator();
			while(it1.hasNext()) {
				Map.Entry<String, String> pairs = (Entry<String, String>)it1.next();
				queryMap.put(pairs.getKey(), helper.createQuery(pairs.getValue()));
			}
			Iterator<Entry<String, OCLExpression<EClassifier>>> it2 = queryMap.entrySet().iterator();
			while(it2.hasNext()) {
				Entry<String, OCLExpression<EClassifier>> pairs = (Entry<String, OCLExpression<EClassifier>>)it2.next();
				long startTime = System.currentTimeMillis();
				System.out.println(ocl.evaluate(this.monitor, pairs.getValue()));
				long stopTime = System.currentTimeMillis();
			    long elapsedTime = stopTime - startTime;
			    System.out.print(elapsedTime);
			    System.out.print('\t');
			}
		} catch (ParserException e) {
			e.printStackTrace();
		}
	}
}
