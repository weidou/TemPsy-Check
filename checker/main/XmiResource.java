package lu.svv.offline.main;

import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;

public class XmiResource {

	protected ResourceSet resourceSet;
	
	protected XmiResource() {
		if (resourceSet == null) {
			resourceSet = new ResourceSetImpl();
			resourceSet.getResourceFactoryRegistry().getExtensionToFactoryMap().put("xmi", new XMIResourceFactoryImpl());
		}
	}
	
	public void register(String uri, Object obj) {
		resourceSet.getPackageRegistry().put(uri, obj);
	}
	
	public Object getContent(URI uri, boolean bool) {
		return resourceSet.getResource(uri, bool).getContents().get(0);
	}
}
