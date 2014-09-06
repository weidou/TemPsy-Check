package lu.svv.offline.oclr;

import java.io.IOException;
import java.util.Collections;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;

import lu.svv.offline.oclr.oclr.OclrPackage;

import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;
import org.eclipse.xtext.resource.XtextResource;
import org.eclipse.xtext.resource.XtextResourceSet;

import com.google.inject.Injector;

public class OCLRInstanceFactory {
	public static void main(String[] args) {
		try {
			List<Integer> iList = range(1,38);
			Iterator<Integer> iter = iList.iterator();
			String pPathTemp = "../lu.svv.offline.oclr/instance/p%d.oclr";
			String instPathTemp = "../lu.svv.offline.oclr/instance/p%d.xmi";
			while(iter.hasNext()){
				int index = iter.next();
				String pPath = String.format(pPathTemp, index);
				String instPath = String.format(instPathTemp, index);
				buildOclr(loadOclrInstance(pPath), instPath);
			}
			System.out.println("done");
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

    public static List<Integer> range(int min, int max) {
        List<Integer> list = new LinkedList<Integer>();
        for (int i = min; i <= max; i++) {
            list.add(i);
        }
        return list;
    }

	public static EObject loadOclrInstance(String instanceURI) {
		Injector injector = new OclrStandaloneSetup().createInjectorAndDoEMFRegistration();
		XtextResourceSet resourceSet = injector.getInstance(XtextResourceSet.class);
		resourceSet.addLoadOption(XtextResource.OPTION_RESOLVE_ALL, Boolean.TRUE);
		Resource resource = resourceSet.getResource(URI.createURI(instanceURI), true);
		return resource.getContents().get(0);
	}
	
	public static void buildOclr(EObject constraint, String instPath) throws IOException {
		ResourceSet resourceSet = new ResourceSetImpl();
		resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap().put(
			    "xmi", new XMIResourceFactoryImpl());
		resourceSet.getPackageRegistry().put(OclrPackage.eNS_URI, OclrPackage.eINSTANCE);
		Resource resource = resourceSet.createResource(URI.createURI(instPath));
		resource.getContents().add(constraint);
		resource.save(Collections.EMPTY_MAP);
	}
}
