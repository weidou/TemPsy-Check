package lu.svv.offline.main;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Map.Entry;

import lu.svv.offline.check.CheckPackage;
import lu.svv.offline.check.Monitor;
import lu.svv.offline.check.impl.CheckFactoryImpl;
import lu.svv.offline.tempsy.TemPsyBlock;
import lu.svv.offline.tempsy.TempsyPackage;
import lu.svv.offline.trace.Trace;
import lu.svv.offline.trace.TracePackage;
import org.eclipse.emf.ecore.EClassifier;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.impl.EPackageRegistryImpl;
import org.eclipse.ocl.OCL;
import org.eclipse.ocl.OCLInput;
import org.eclipse.ocl.ParserException;
import org.eclipse.ocl.ecore.Constraint;
import org.eclipse.ocl.ecore.EcoreEnvironmentFactory;
import org.eclipse.ocl.helper.OCLHelper;

public class TraceCheck {
	private Monitor monitor;
	public static final String oclOperationsFile = "lib/tempsy-check.ocl";
	private OCL<EPackage, EClassifier, ?, ?, ?, ?, ?, ?, ?, Constraint, ?, ?> ocl;
	private OCLHelper<EClassifier, ?, ?, Constraint> oclHelper;
	private ResourceLoader tempsyLoader;
	private ResourceLoader traceLoader;

	
	// load TemPsy properties (XMI) and trace instances (CSV)
	public void loadMonitor(String tempsyFilePath, String traceFilePath) {
		tempsyLoader = XmiTemPsyLoader.init();
		TemPsyBlock properties = (TemPsyBlock) tempsyLoader.load(tempsyFilePath);

		traceLoader = CsvTraceLoader.init();
		Trace trace = (Trace) traceLoader.load(traceFilePath);
		
		if (properties != null && trace != null) {
			Monitor monitor = new CheckFactoryImpl().createMonitor();
			monitor.setProperties(properties);
			monitor.setTrace(trace);
			this.monitor = monitor;
		}
	}
	
	public void resetMonitor() {
		this.monitor = null;
	}
	
	public void parseOCL() {
		// Copied from org.eclipse.ocl.ecore.tests.DocumentationExamples.java
		EPackage.Registry registry = new EPackageRegistryImpl();
		registry.put(CheckPackage.eNS_URI, CheckPackage.eINSTANCE);
		registry.put(TempsyPackage.eNS_URI, TempsyPackage.eINSTANCE);
		registry.put(TracePackage.eNS_URI, TracePackage.eINSTANCE);
		EcoreEnvironmentFactory environmentFactory = new EcoreEnvironmentFactory(registry);
		ocl = OCL.newInstance(environmentFactory);

		// get an OCL text file via some hypothetical API
		InputStream in = null;
		try {
			in = new FileInputStream(oclOperationsFile);
			in.skip(193);
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
		oclHelper = ocl.createOCLHelper();
		oclHelper.setContext(CheckPackage.Literals.MONITOR);
	}

	public void checkSingle() throws ParserException
	{
		ocl.check(this.monitor, oclHelper.createInvariant(ConstraintFactory.init().createInvariant(monitor.getProperties().getTemPsyExpressions().get(0))));
	}

	public void applyScopeSingle() throws ParserException
	{
		ocl.evaluate(this.monitor, oclHelper.createQuery(ConstraintFactory.init().createScopeQuery(monitor.getProperties().getTemPsyExpressions().get(0))));
	}
	
	public void check() throws ParserException
	{
		Map<String, String> constraintStringMap = ConstraintFactory.init().createInvariants(this.monitor);
		Map<String, Constraint> constraintMap = new HashMap<String, Constraint>();
		Iterator<Entry<String, String>> it1 = constraintStringMap.entrySet().iterator();
		while(it1.hasNext()) {
			Map.Entry<String, String> pairs = (Entry<String, String>)it1.next();
			constraintMap.put(pairs.getKey(), oclHelper.createInvariant(pairs.getValue()));
		}
		Iterator<Entry<String, Constraint>> it2 = constraintMap.entrySet().iterator();
		while(it2.hasNext()) {
			Entry<String, Constraint> pairs = (Entry<String, Constraint>)it2.next();
			ocl.check(this.monitor, pairs.getValue());
		}
	}
}
