package lu.svv.offline.trace;

import java.io.IOException;
import java.util.Collections;

import lu.svv.offline.trace.trace.TracePackage;
import lu.svv.offline.trace.TraceStandaloneSetup;

import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;
import org.eclipse.xtext.resource.XtextResource;
import org.eclipse.xtext.resource.XtextResourceSet;

import com.google.inject.Injector;

public class TraceInstanceFactory {

	public static void main(String[] args) {
		try {
			buildTrace(loadTraceInstance("../lu.svv.offline.trace/instance/p1.trace"));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static EObject loadTraceInstance(String instanceURI) {
		Injector injector = new TraceStandaloneSetup().createInjectorAndDoEMFRegistration();
		XtextResourceSet resourceSet = injector.getInstance(XtextResourceSet.class);
		resourceSet.addLoadOption(XtextResource.OPTION_RESOLVE_ALL, Boolean.TRUE);
		Resource resource = resourceSet.getResource(
		    URI.createURI(instanceURI), true);
		return resource.getContents().get(0);
	}
	
	public static void buildTrace(EObject constraint) throws IOException {
		ResourceSet resourceSet = new ResourceSetImpl();
		resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap().put(
			    "xmi", new XMIResourceFactoryImpl());
		resourceSet.getPackageRegistry().put(TracePackage.eNS_URI, TracePackage.eINSTANCE);
		Resource resource = resourceSet.createResource(URI.createURI("../lu.svv.offline.trace/instance/p1.xmi"));
		resource.getContents().add(constraint);
		resource.save(Collections.EMPTY_MAP);
	}
	
}
